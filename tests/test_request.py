from airflow.dags.src import Request


def test_request_get_successful():
    """
    Test case to verify a successful GET request using the Request class.

    It sends a GET request to the specified URL with the given headers and
    checks if the response is not None and if it is successful (status code 200).

    """
    url = "https://example.com"
    headers = {"Content-Type": "application/json"}
    request = Request(headers=headers)

    response = request.get(url)

    assert response is not None
    assert response.ok


def test_request_get_failed():
    """
    Test case for the 'get' method of the Request class when the URL is invalid.
    """
    url = 123
    request = Request()

    response = request.get(url)

    assert response is None


def test_request_post_successful():
    """
    Test the successful POST request using the Request class.

    This function tests the functionality of the `post` method of the Request class.
    It sends a POST request to the specified URL with the provided data and checks
    if the response is not None and if it is successful (status code 200).

    """
    url = "https://example.com"
    data = {"key": "value"}
    request = Request()

    response = request.post(url, data=data)

    assert response is not None
    assert response.ok


def test_request_post_error():
    """
    Test case for the 'post' method of the Request class when an error occurs.

    This test verifies that the 'post' method returns None when an invalid URL is provided.
    """
    url = 123
    request = Request()

    response = request.post(url)

    assert response is None
