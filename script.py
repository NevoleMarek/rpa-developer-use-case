import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

def scrape_table(URL):
    """
    Scrape first table from 'URL' website and return it
    as pandas.DataFrame.

    Parameters
    ----------
    URL : str
        URL string of scraped website.

    Returns
    -------
    pd.DataFrame
        DataFrame of first table element on scrapped website.
    """
    with webdriver.Chrome('chromedriver.exe') as driver:
        driver.get(URL)
        table = driver.find_element(By.XPATH, '//table[1]')
        df = pd.read_html(
            table.get_attribute('outerHTML'),
            header=0,
            parse_dates=['OrderDate']
        )[0]
    return df

def calculate_discount():
    pass

def create_database_from_dataframe():
    pass

def main():
    URL = 'https://www.contextures.com/xlsampledata01.html'

    df = scrape_table(URL)

if __name__ == '__main__':
    main()
