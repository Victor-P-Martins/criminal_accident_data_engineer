import traceback

import requests
from requests.adapters import HTTPAdapter, Retry


class Request:
    """
    A class for making HTTP requests with retry functionality.

    Args:
        headers (dict): Optional. Headers to be included in the requests.

    Attributes:
        headers (dict): Headers to be included in the requests.
        session (requests.Session): Session object for making requests.
    """

    def __init__(self, headers: dict = None):
        retries = Retry(total=5, backoff_factor=2)
        self.headers = headers
        self.session = requests.Session()
        self.session.mount("https://", HTTPAdapter(max_retries=retries))

    def __verify_response(self, response: object) -> object:
        """
        Verifies the response of the request and handles errors.

        Args:
            response (object): The response object returned by the request.

        Returns:
            object: The response object if it is successful, otherwise None.
        """

        if response.ok:
            return response

        print(f"Erro na requisição: {response}")
        return response

    def get(self, url: str, payload: dict = None, files: list = None) -> object:
        """
        Sends a GET request to the specified URL.

        Args:
            url (str): The URL to send the request to.
            payload: Optional. The payload to include in the request.

        Returns:
            object: The response object if the request is successful, otherwise None.
        """
        try:
            response = self.session.request(
                "GET", url, headers=self.headers, params=payload, files=files
            )

        except requests.exceptions.RequestException:
            print(f"{traceback.format_exc()}")
            return None

        return self.__verify_response(response)

    def post(self, url: str, data: dict = None, json: dict = None) -> object:
        """
        Sends a POST request to the specified URL.

        Args:
            url (str): The URL to send the request to.
            data: Optional. The data to include in the request.
            json: Optional. The JSON payload to include in the request.

        Returns:
            object: The response object if the request is successful, otherwise None.
        """
        try:
            response = self.session.request(
                "POST", url, headers=self.headers, data=data, json=json
            )

        except requests.exceptions.RequestException:
            print(f"{traceback.format_exc()}")
            return None

        return self.__verify_response(response)


if __name__ == "__main__":
    request = Request()
    request.get("https://www.google.com")
