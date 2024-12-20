
name = ['jebucher']

from bs4 import BeautifulSoup
import urllib.request as url
import pandas as pd

def worldbankimport(countries: list, indicators: list):
    """
    Utilizes the World Bank API to access national data for certain indicators

    Args:
        - countries: a list of countries (list of strings, each string is a country code)
        - indicators: a list of indicators (list of strings, each string is an indicator code)

    Returns:
        - a Pandas Dataframe with all of the data
    """

    wbdf = pd.DataFrame(columns = ["indicator id", "indicator value", "country id", "country value",
               "countryiso3code", "date", "value", "unit", "obs_status", "decimal"])
    
    countries = ";".join(countries)
    indicators = ";".join(indicators)
    
    urlstring = f"https://api.worldbank.org/v2/country/{countries}/indicator/{indicators}?source=2"
    req = url.Request(urlstring)
    file = url.urlopen(req)
    soup = BeautifulSoup(file, "xml")
    pages = soup.contents[0]['pages']


    tag_columns = ["indicator value", "country value",
               "countryiso3code", "date", "value", "unit", "obs_status", "decimal"]

    for page in range(1, int(pages) + 1):
        urlstring = f"https://api.worldbank.org/v2/country/{countries}/indicator/{indicators}?source=2&page={page}"
        req = url.Request(urlstring)
        file = url.urlopen(req)
        soup = BeautifulSoup(file, "xml")
        catalog = soup.find_all(True, recursive = False)[0]

        for i in range(len(catalog.find_all(True, recursive = False))):

            row = catalog.find_all(True, recursive = False)[i]
            cells = row.find_all(True, recursive = False)
            row_dict = {}

            # accessng the id attributes for indicator and country
            row_dict['indicator id'] = cells[0]['id']
            row_dict['country id'] = cells[1]['id']

            # iterates of the total number of columns
            for j in range(len(cells)):
                row_dict[tag_columns[j]] = cells[j].string
            wbdf = pd.concat([wbdf, pd.DataFrame(row_dict, index = pd.Index([0]))], ignore_index = True)

    return wbdf
   
df = worldbankimport(["CHN", "USA"], ["EG.ELC.ACCS.RU.ZS"])
print(df[:5])


    