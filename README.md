# RPA Developer Use Case

## Description

Task was to scrape Office Supply Sales table from this [website](https://www.contextures.com/xlsampledata01.html) and calculate **Final price** and **Total discount** with given discount conditions. Final step was to insert these data with current datetime to database.

## How to run

Make sure you have `pipenv` installed.

```powershell
git clone https://github.com/NevoleMarek/rpa_developer_use_case.git
cd .\rpa_developer_use_case\
pipenv install
```

I used **chromedriver** as `webdriver` for `Selenium`.

Download **chromedriver** for your version of google chrome : [here](https://chromedriver.storage.googleapis.com/index.html)

Move **chromedriver** to same directory as **script.py**.

To run the script in pipenv venv type:

```powershell
pipenv run python .\script.py
```

If executed correctly the script should output `database.db` sqlite3 database file and print query from this database to standard output.

## Example Output

![stdout](C:\Users\mnkh\Desktop\foxconn\rpa_developer_use_case\stdout.png)

![sqlite](C:\Users\mnkh\Desktop\foxconn\rpa_developer_use_case\sqlite.png)



## Todo

- [x] Description
- [x] How to run
- [x] Example Output

