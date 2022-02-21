"""Equipment data stored in Parquet files on S3.

(organized by Equipment Unique Type Group by Date)
"""

from dataclasses import dataclass
from functools import cached_property, lru_cache
import os
from typing import Literal, Optional
from typing import List   # Py3.9+: use built-ins

from pandas import DataFrame

from ai_utils.data_proc import S3ParquetDataFeeder


_EQUIPMENT_DATA_S3_PARENT_DIR_PATH: str = \
    os.environ['H1ST_PMFP_EQUIPMENT_DATA_S3_PARENT_DIR_PATH']
_EQUIPMENT_DATA_TIMEZONE: str = os.environ['H1ST_PMFP_EQUIPMENT_DATA_TIMEZONE']


EQUIPMENT_INSTANCE_ID_COL: str = 'equipment_instance_id'
DATE_COL: str = 'date'
DATE_TIME_COL: str = 'date_time'


@dataclass(init=True,
           repr=True,
           eq=True,
           order=True,
           unsafe_hash=False,
           frozen=True)   # frozen=True needed for __hash__()
class EquipmentParquetDataSet:
    """Equipment Unique Type Group Parquet Data Set."""

    general_type: Literal['refrig', 'disp_case']
    unique_type_group: str

    @cached_property
    def name(self) -> str:
        """Name data set."""
        return f'{self.general_type.upper()}---{self.unique_type_group}'

    @cached_property
    def url(self) -> str:
        """Get URL of data set."""
        return f'{_EQUIPMENT_DATA_S3_PARENT_DIR_PATH}/{self.name}.parquet'

    def __repr__(self) -> str:
        """Return string representation."""
        return f'{self.unique_type_group.upper()} data @ {self.url}'

    @lru_cache(maxsize=None, typed=False)
    def load(self) -> S3ParquetDataFeeder:
        """Load as a Parquet Data Feeder."""
        return S3ParquetDataFeeder(
            path=self.url,
            awsRegion='ap-northeast-1',   # default is location-dependent
            iCol=EQUIPMENT_INSTANCE_ID_COL, tCol=DATE_TIME_COL
        ).castType(**{EQUIPMENT_INSTANCE_ID_COL: str})

    @lru_cache(maxsize=None, typed=False)
    def get_equipment_instance_ids_by_date(
            self,
            date: Optional[str] = None, to_date: Optional[str] = None) \
            -> List[str]:
        """Get equipment instance IDs by date(s)."""
        s3_parquet_df: S3ParquetDataFeeder = self.load()

        if date:
            try:
                s3_parquet_df: S3ParquetDataFeeder = \
                    s3_parquet_df.filterByPartitionKeys((DATE_COL, date, to_date)   # noqa: E501
                                                        if to_date
                                                        else (DATE_COL, date))

            except Exception as err:   # pylint: disable=broad-except
                print(f'*** {err} ***')
                return []

        return [str(i) for i in
                sorted(s3_parquet_df.collect(EQUIPMENT_INSTANCE_ID_COL)
                       [EQUIPMENT_INSTANCE_ID_COL].unique())]

    def load_by_date(self,
                     date: str, to_date: Optional[str] = None,
                     equipment_instance_id: Optional[str] = None) \
            -> S3ParquetDataFeeder:
        """Load equipment data by date(s)."""
        s3_parquet_df: S3ParquetDataFeeder = self.load()

        try:
            s3_parquet_df: S3ParquetDataFeeder = \
                s3_parquet_df.filterByPartitionKeys((DATE_COL, date, to_date)
                                                    if to_date
                                                    else (DATE_COL, date))

        except Exception as err:   # pylint: disable=broad-except
            S3ParquetDataFeeder.classStdOutLogger().error(msg=str(err))

        if equipment_instance_id:
            s3_parquet_df: S3ParquetDataFeeder = \
                s3_parquet_df.filter(f'{EQUIPMENT_INSTANCE_ID_COL} == '
                                     f'"{equipment_instance_id}"')

        return s3_parquet_df

    def load_by_equipment_instance_id_by_date(
            self,
            equipment_instance_id: str,
            date: str, to_date: Optional[str] = None) -> DataFrame:
        """Load equipment data by equipment instance ID and date(s)."""
        s3_parquet_df: S3ParquetDataFeeder = \
            self.load().filter(f'{EQUIPMENT_INSTANCE_ID_COL} == '
                               f'"{equipment_instance_id}"')

        if date:
            s3_parquet_df: S3ParquetDataFeeder = \
                s3_parquet_df.filterByPartitionKeys((DATE_COL, date, to_date)
                                                    if to_date
                                                    else (DATE_COL, date))

        return (s3_parquet_df.collect()
                .drop(columns=[EQUIPMENT_INSTANCE_ID_COL, DATE_COL],
                      inplace=False,
                      errors='raise')
                .sort_values(by=DATE_TIME_COL,
                             axis='index',
                             ascending=True,
                             inplace=False,
                             kind='quicksort',
                             na_position='last')
                .set_index(keys=DATE_TIME_COL,
                           drop=True,
                           append=False,
                           inplace=False,
                           verify_integrity=True)
                .tz_localize('UTC')
                .tz_convert(_EQUIPMENT_DATA_TIMEZONE)
                .tz_localize(None))
