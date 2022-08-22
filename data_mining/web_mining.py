"""
program to collect news data from mediastack news api and store in mongodb 
"""

## imports
import sys

sys.path.append("/workspaces/Event-Extraction")
import os
import requests
from mongodb.config import db
from dotenv import load_dotenv

# loads environment variables from .env file
load_dotenv()
ACCESS_KEY = os.getenv("ACCESS_KEY")


## initialize mongodb
news_collection = db["kashmir_news"]


def leap_year(year):
    """
    Returns True if the year is a leap year.

    Parameters:
    year(int) - the year to check

    Returns:
    bool - True if the year is a leap year, False otherwise
    """
    if year % 400 == 0:
        return True
    if year % 100 == 0:
        return False
    if year % 4 == 0:
        return True
    return False


def days_in_month(month, year):
    """
    Returns the number of days in a month.

    Parameters:
    month(int) - the month to check
    year(int) - the year to check

    Returns:
    int - the number of days in the month
    """
    if month == 2:
        if leap_year(year):
            return 29
        return 28
    if month in [4, 6, 9, 11]:
        return 30
    return 31
    if month in {1, 3, 5, 7, 8, 10, 12}:
        return 31
    if month == 2:
        if leap_year(year):
            return 29
        return 28
    return 30


def get_parameters(month, year):
    """
    Returns the parameters for the API call.

    Parameters:
    month(int) - the month to check
    year(int) - the year to check

    Returns:
    dict - the parameters for the API call
    """
    end_day = str(days_in_month(month, year))
    month = "0" + str(month) if month < 10 else str(month)
    year = str(year)
    parameters = {
        "access_key": ACCESS_KEY,
        "date": f"{year}-{month}-1,{year}-{month}-{end_day}",
        "countries": "in",
        "limit": "100",
        "categories": "general",
        "keywords": "kashmir",
    }
    return parameters


### get data for the required years and months
for year in [2022]:
    for i in range(1, 7):
        print("---processing month {} year {}---".format(i, year))
        parameters = get_parameters(i, year)
        try:
            # get data from api
            response = requests.get(
                "http://api.mediastack.com/v1/news", params=parameters
            )
            json_response = response.json()
            data = json_response["data"]
            print("articles_found", len(data))

            # insert data into mongodb
            if len(data) > 0:
                x = news_collection.insert_many(data)

        except Exception as e:
            print("error", e)
