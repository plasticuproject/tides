"""test_api.py"""
import unittest
import json
from unittest import mock
from typing import Optional
import requests
from api.__main__ import app
from api.scraper.tide_scraper import low_tides_information


class MockResponse:  # pylint: disable=too-few-public-methods
    """Mock API responses."""

    def __init__(self, response_data: Optional[str], status_code: int) -> None:
        self.response_data = response_data
        self.status_code = status_code
        self.text = response_data


# pylint: disable=unused-argument
def mocked_requests_get(*args: str, **kwargs: str) -> MockResponse:
    """This method will be used by the mock to replace requests.get."""
    if args[0] == ("https://www.tide-forecast.com/locations/" +
                   "Huntington-Beach/tides/latest"):
        with open("./test/test.html", "r", encoding="utf-8") as infile:
            data = infile.read()
        return MockResponse(data, 200)
    return MockResponse(None, 404)


class ApiTests(unittest.TestCase):
    """Test endpoints and low tide scraper."""

    def setUp(self) -> None:
        """Set up flask app for testing."""
        app.config["DEBUG"] = False
        self.app = app.test_client()
        self.assertEqual(app.debug, False)

    def tearDown(self) -> None:
        """Tear down."""
        pass

    def test_live_site(self) -> None:
        """Test that tide-forecast site is live."""
        response = self.app.get("/api/v1/Huntington-Beach",
                                follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_index(self) -> None:
        """Test index/landing page."""
        with open("./test/index.html", "r", encoding="utf-8") as infile:
            index_page = infile.read()
        response = self.app.get("/")
        self.assertEqual(response.text, index_page)

    def test_redirect(self) -> None:
        """Test the web server is redirecting to the
        index page when given invalid endpoints."""
        with open("./test/index.html", "r", encoding="utf-8") as infile:
            index_page = infile.read()
        response_one = self.app.get("fart", follow_redirects=True)
        response_two = self.app.get("/api/v1/fart", follow_redirects=True)
        self.assertEqual(response_one.text, index_page)
        self.assertEqual(response_two.text, index_page)

    @mock.patch("api.scraper.tide_scraper.requests.get",
                side_effect=mocked_requests_get)
    def test_low_tides_infomation(self, mock_get: mock.MagicMock) -> None:
        """Test that the low_tides_information function
        returns the proper data given a mock request."""
        with open("./test/test.json", "r", encoding="utf-8") as infile:
            json_data = json.loads(infile.read())
        response = low_tides_information("Huntington-Beach")
        self.assertEqual(response, json_data)

    @mock.patch("requests.get", side_effect=mocked_requests_get)
    def test_request_mock_404(self, mock_get: mock.MagicMock) -> None:
        """Test that the request mock fails correctly."""
        response = requests.get("fart", timeout=60)
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
