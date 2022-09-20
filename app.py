"""app.py"""
from typing import Dict, List, Union
from flask import Flask
from werkzeug.exceptions import NotFound
import tide_scraper

app = Flask(__name__)

ENDPOINTS = [
    "half-moon-bay-california", "huntington-beach", "providence-rhode-island",
    "wrightsville-beach-north-carolina"
]


@app.errorhandler(404)
def not_found(error: NotFound) -> str:  # pylint: disable=unused-argument
    """Redirect all 404 errors to index."""
    return index()


@app.route("/")
def index() -> str:
    """List out valid api endpoints."""
    return 'Valid Endpoints:<br />\
    <a href="/api/v1/Half-Moon-Bay-California">\
    /api/v1/Half-Moon-Bay-California</a><br />\
    <a href="/api/v1/Huntington-Beach">\
    /api/v1/Huntington-Beach</a><br />\
    <a href="/api/v1/Providence-Rhode-Island">\
    /api/v1/Providence-Rhode-Island</a><br />\
    <a href="/api/v1/Wrightsville-Beach-North-Carolina">\
    /api/v1/Wrightsville-Beach-North-Carolina</a>'


@app.route("/api/v1/<string:location>/")
def low_tides(location: str) -> Union[str, Dict[str, List[Dict[str, str]]]]:
    """Returns the time and height for each daylight low tide
    for a ~28 day forcast from https://www.tide-forecast.com
    for a specified location."""
    if location.lower() in ENDPOINTS:
        return tide_scraper.low_tides_information(location)
    return index()


if __name__ == "__main__":
    app.run()
