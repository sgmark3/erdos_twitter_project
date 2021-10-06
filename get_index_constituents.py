import pandas as pd
import requests
from bs4 import BeautifulSoup
# There are 2 tables on the Wikipedia page
# we want the first table
snp500_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
dow_url = "https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average"
table_class="wikitable sortable jquery-tablesorter"

def get_df(name=""):
    if name is None: return
    if name == "snp500":
        url = snp500_url
    elif name == "dow":
        url = dow_url
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    dfs = pd.read_html(page.text)

    for df in dfs:
        print(df)


if __name__=="__main__":
    get_df("dow")