import datetime
import sqlite3

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

def total_discount(row):
    region_unit_discount = 0.23 if row['Region'] == 'Central' else 0.12
    discount = row['Units'] * region_unit_discount
    if row['Units'] > 50:
        discount += 7.2
    return discount

def calculate_discount(df):
    """
    Add TotalDiscount and FinalPrice columns to dataframe passed as 'df'.

    Parameters
    ----------
    df : pd.DataFrame
    """
    df['TotalDiscount'] = df.apply(total_discount, axis=1)
    df['FinalPrice'] = df['Total'] - df['TotalDiscount']

def create_connection():
    try:
        return sqlite3.connect(
            'database.db',
            detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES
        )
    except Exception as e:
        raise e

def create_table(cur):
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS 'office_supply_sales'(
            Region TEXT,
            Rep TEXT,
            Item TEXT,
            Units INTEGER,
            [Total discount] REAL,
            [Final Price] REAL,
            [Creation date] timestamp,
            OrderDate date
        )
        """
    )

def create_tuple_from_row(row):
    return (
        row.Region,
        row.Rep,
        row.Item,
        row.Units,
        row.TotalDiscount,
        row.FinalPrice,
        datetime.datetime.now(),
        row.OrderDate.date()
    )

def dataframe_to_qmark(df):
    return [create_tuple_from_row(row) for row in df.itertuples(index=False)]

def insert_dataframe(cur, df):
    insert_query = "INSERT INTO 'office_supply_sales' VALUES (?, ?, ?, ?, ?, ?, ?, ?);"
    qmark_list = dataframe_to_qmark(df)
    cur.executemany(insert_query, qmark_list)

def create_database_from_dataframe(df):
    """
    Create database and table. Fill the table with data from 'df' dataframe.

    Parameters
    ----------
    df : pd.DataFrame

    Returns
    -------
    sqlite3.Connection
        Connection object of SQLite3 database.
    """
    conn = create_connection()
    cur = conn.cursor()
    create_table(cur)
    insert_dataframe(cur, df)
    conn.commit()
    cur.close()
    return conn

def main():
    URL = 'https://www.contextures.com/xlsampledata01.html'

    df = scrape_table(URL)
    calculate_discount(df)
    conn = create_database_from_dataframe(df)

    # Example query
    cur = conn.cursor()
    cur.execute("SELECT * FROM 'office_supply_sales'")
    for row in cur.fetchall():
        print(row)

    cur.close()
    conn.close()

if __name__ == '__main__':
    main()
