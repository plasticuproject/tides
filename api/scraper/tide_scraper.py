"""tide_scraper.py"""
import re
from typing import List, Dict
import requests
from dateutil.parser import parse

# # LOCATIONS TO BE TESTED # #
# Half-Moon-Bay-California
# Huntington-Beach
# Providence-Rhode-Island
# Wrightsville-Beach-North-Carolina


def _regex_search(start: str, end: str, text: str) -> List[str]:
    """Returns a list of strings from text parameter
    found in between the start and end parameters.

    Parameters
    ----------
    arg1 : str
        string start search parameter

    arg2 : str
        string end search parameter

    arg3 : str
        text string to be searched

    Returns
    -------
    list of str
        List of strings that are found between
        the start and end parameters

    Example
    -------
    >>> test_string = "1 hello world 2 1 hello again 2"
    >>> test_result = _regex_search("1 ", " 2", test_string)
    >>> assert test_result == ["hello world", "hello again"]
    """
    return re.findall(fr'(?:{start})([\r\s\S]*?)(?:{end})', text)


# pylint: disable=too-many-locals
def low_tides_information(location: str) -> Dict[str, Dict[str, str]]:
    """Returns the time and height for each daylight low tide
    for a ~28 day forcast from https://www.tide-forecast.com
    for a specified location.

    Parameters
    ----------
    arg1 : str
        Location for tide data

    Returns
    -------
    Dict[str, Dict[str, str]]]
        Dictionary of data of low tide information
    """

    # Retrieve webpage text with tide information for a specific location
    url = "https://www.tide-forecast.com/"
    latest = "tides/latest"
    response = requests.get(f"{url}locations/{location}/{latest}", timeout=60)
    text = response.text

    # Dictionary to store our low tide data
    data: Dict[str, Dict[str, str]] = {}

    # Table containing tide forecasts
    table_start = '<div class="tide_flex_start">'
    table_end = '</section>'

    # All tide data for individual days
    tides_start = '<div class="tide-day">'
    tides_end = '<p class="watermark">'

    # Full date string for day
    title_start = ': '
    title_end = '</h4>'

    # Contains low tide information for a single day
    low_tide_start = '<td>Low Tide</td><td><b>'
    low_tide_end = '</b> <span class="js-two-units-length-value__secondary'

    # Time of sunrise for day
    sunrise_start = 'Sunrise:<span class="tide-day__value"> '
    sunrise_end = '</span>'

    # Time of sunset for day
    sunset_start = 'Sunset:<span class="tide-day__value"> '
    sunset_end = '</span>'

    # Generate list of days with tide infomation
    tide_table = _regex_search(table_start, table_end, text)[0]
    days = _regex_search(tides_start, tides_end, tide_table)

    # Loop through list of day's tide information and extract
    # all dates with tide times and heights where the tide time
    # is between sunrise time and sunset time
    for i in days:
        sunrise = parse(_regex_search(sunrise_start, sunrise_end, i)[0])
        sunset = parse(_regex_search(sunset_start, sunset_end, i)[0])

        low_tides = {
            j[:8].strip(): j[-7:].strip(">")
            for j in _regex_search(low_tide_start, low_tide_end, i)
            if sunrise < parse(j[:8]) < sunset
        }

        data[(_regex_search(title_start, title_end, i)[0])] = low_tides

    return data
