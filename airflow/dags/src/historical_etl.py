import os
from typing import Literal

import polars as pl
import numpy as np
import json
from polars import DataFrame
from dotenv import load_dotenv
from .request import Request
from .database import PostgresDB
from sqlalchemy.types import JSON
from typing import Union


load_dotenv(".env")


class HistoricalExtract:
    """
    Class for extracting historical data from an API.

    Attributes:
        request (Request): An instance of the Request class for making API requests.
        endpoint (str): The API endpoint URL.
        app_token (str): The application token for accessing the API.
    methods:
        ___records_to_dataframe: Transform a list of records into a DataFrame.
        get_data: Get historical data from the API.
    """

    def __init__(self):
        self.request = Request()
        self.endpoint = "https://data.sfgov.org/resource/wg3w-h783.json"
        self.app_token = os.getenv("app_token")

    def ___records_to_dataframe(self, records: list[dict]) -> DataFrame:
        """
        Transform a list of records into a DataFrame.

        Args:
            records (list[dict]): The list of records to be transformed.

        Returns:
            DataFrame: The transformed DataFrame.
        """
        return pl.from_records(records, infer_schema_length=50000)

    def __transform_array_to_list(
        self, dictionary_str: str, key_array: str
    ) -> Union[dict, None]:
        if dictionary_str[key_array] is not None and isinstance(
            dictionary_str[key_array], np.ndarray
        ):
            dictionary_str[key_array] = dictionary_str[key_array].tolist()
            return json.dumps(dictionary_str)
        else:
            return None

    def get_data(self, chunk_size: int = 500000, offset: int = 0) -> DataFrame:
        """
        Get historical data from the API. Write a Parquet file with the data.

        Args:
            chunk_size (int): The number of records to retrieve per API request. Default is 500000.
            offset (int): The offset value for pagination. Default is 0.

        Returns:
            None
        """

        dataframe_list = [
            self.___records_to_dataframe(
                self.request.get(
                    f"{self.endpoint}?$order=incident_datetime&$limit={chunk_size}&$offset={offset}"
                ).json()
            )
        ]

        response_records = dataframe_list[0]

        while True:
            offset += chunk_size
            response_records = self.request.get(
                f"{self.endpoint}?$order=incident_datetime&$limit={chunk_size}&$offset={offset}"
            ).json()

            if response_records == []:
                break

            dataframe_list.append(self.___records_to_dataframe(response_records))

        dataframe = pl.concat(
            [df.select(dataframe_list[0].columns) for df in dataframe_list]
        )

        return dataframe

    def persist_data(
        self,
        dataframe: DataFrame,
        database: str,
        db_user: str,
        db_pass: str,
        db_host: str,
        db_port: str,
    ) -> None:
        """
        Persist the historical data to a database.

        Args:
            data (DataFrame): The historical data to persist.
            path (str): The file path to which the data will be persisted.

        Returns:
            None
        """
        try:
            conn = PostgresDB(
                host=db_host,
                user=db_user,
                password=db_pass,
                port=db_port,
                database=database,
            ).create_engine_conn()
        except Exception as e:
            raise ConnectionError("Error creating connection to database", e)
        try:
            pd_dataframe = dataframe.to_pandas()

            pd_dataframe["point"] = pd_dataframe["point"].apply(
                lambda x: (self.__transform_array_to_list(dict(x), "coordinates"))
            )

            pd_dataframe.to_sql(
                "criminal_observations",
                conn,
                if_exists="replace",
                dtype={"point": JSON},
                index=False,
            )
        except Exception as e:
            raise ValueError("Error writing to database", e)


if __name__ == "__main__":
    historical_etl = HistoricalExtract()
    historical_data = historical_etl.get_data()
