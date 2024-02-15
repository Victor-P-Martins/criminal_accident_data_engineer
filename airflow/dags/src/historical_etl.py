import os

import polars as pl
from polars import DataFrame
from dotenv import load_dotenv
from .request import Request


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

    def get_data(self, chunk_size: int = 500000, offset: int = 0) -> DataFrame:
        """
        Get historical data from the API.

        Args:
            chunk_size (int): The number of records to retrieve per API request. Default is 500000.
            offset (int): The offset value for pagination. Default is 0.

        Returns:
            DataFrame: Historical data.
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

        return pl.concat(dataframe_list)


if __name__ == "__main__":
    historical_etl = HistoricalExtract()
    historical_data = historical_etl.get_data()
