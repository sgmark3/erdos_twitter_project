## Resurses:
#    * https://www.youtube.com/watch?v=WRGk8PBBf2o
#    * https://en.wikipedia.org/wiki/List_of_American_exchange-traded_funds#Stock_ETFs
#    * https://medium.datadriveninvestor.com/scraping-wikipedia-for-etf-names-3278e4557944



import requests
from bs4 import BeautifulSoup

url='https://en.wikipedia.org/wiki/List_of_American_exchange-traded_funds#Index-tracking_ETFs'
response = requests.get(url=url)
soup = BeautifulSoup(response.content).find(id="bodyContent")
ticklist=soup.find_all("li")
tick_txt_list=set() # we use set to keep the list unique 
for tick in ticklist:
  textstring=tick.text
  if "iShares" in textstring and "|" in textstring:
    tick_string = textstring[(textstring.find("|")):textstring.find(")")]
    tick_txt_list.add(tick_string[1:])

print(tick_txt_list)
print("Number or tickers pulled: "+str(len(tick_txt_list)))
ticklist=list(tick_txt_list)

# Now we can read the data from Yahoo
from pandas_datareader import data
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df = data.DataReader(ticklist[0:], 'yahoo', '2015-1-1', '2021-1-1') # this will read the data from Yahoo Finance
adj = df['Adj Close'] # we only intrested in the adjusted close price - to acount for dividends and intrest payments from bonds.
adj = adj.reindex(pd.date_range(start='2015-1-1',end='2021-1-1',freq='BM')).dropna(axis=1, how='all') #get a data point ones every month
adj = adj.loc[:,adj.iloc[-1,:].notna()].dropna(axis=0) # drop columes that dont have data
norm=adj.apply(lambda x: x/x[0], axis=0) # normlize all columes

# Lets plot what we pulled
plt.rcParams['figure.figsize'] = (15, 8)
sort=norm.T.sort_values(norm.index[-1], ascending=False).T
colormap = plt.cm.gist_ncar
sort.plot(color=plt.cm.gist_rainbow(np.linspace(0, 1,len(sort.T))))
plt.legend(ncol=10)

# Bar plot of return
endreturn_df=sort.iloc[-1,:]
ax = endreturn_df.plot.bar(color=plt.cm.gist_rainbow(np.linspace(0, 1,len(sort.T))))

# Now for calculating volatility  
month_ret=sort.pct_change()
etf_std=month_ret.std()
month_mean=month_ret.mean()
month_sharpe=(month_mean-0.01/12)/etf_std
outdata_df=df = pd.concat([month_mean, etf_std, month_sharpe], axis=1)
outdata_df.columns=['Mean','STD','Sharpe']
outdata_df=outdata_df.sort_values(by=['Sharpe'],ascending=False)

# plot bars of Sharpe
ax = outdata_df['Sharpe'].plot.bar(color=plt.cm.gist_rainbow(np.linspace(0, 1,len(outdata_df))))

# Corrolation matrix
pos_sharpe=outdata_df.index[(outdata_df['Sharpe'] > 0.1) & (outdata_df['Mean'] > 0.003)].tolist()
onlypossharpe=month_ret[month_ret.columns & pos_sharpe]
corrmat=onlypossharpe.corr()

# Plotting the corr-mat as a heat map
import seaborn as sns
sns.set_context(context='paper',font_scale=1)       
plt.figure(figsize=(14, 10))                                           
sns.heatmap(corrmat,square=True,xticklabels=1,yticklabels=1)
plt.show()