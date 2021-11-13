import bs4 as bs
import pickle
import pandas as pd
import requests
import pandas as pd

def save_sp500_tickers():
    """
    This function gets SnP500 table from wikipedia and saves into a csv file
    """
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    df=pd.read_html(str(table))
    # convert list to dataframe
    df=pd.DataFrame(df[0])
    print(df.head())
    df.to_csv('data/Stock_indices/snp500_list.csv', index=False)

def get_companylist():
    """
    This function gets SnP500 table from wikipedia and saves into a csv file
    """
    resp = requests.get('https://topforeignstocks.com/indices/components-of-the-sp-500-index/')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'tablepress'})
    df=pd.read_html(str(table))
    #print(df)
    # convert list to dataframe
    df=pd.DataFrame(df[0])
    print(df.head())
    df.to_csv('data/Stock_indices/snp500_list_v2.csv', index=False)

if __name__=="__main__":
  #save_sp500_tickers()
  get_companylist()
