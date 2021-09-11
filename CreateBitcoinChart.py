import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.offline import plot
import matplotlib.pyplot as plt
import datetime
from pycoingecko import CoinGeckoAPI
from mplfinance.original_flavor import candlestick2_ohlc

cg = CoinGeckoAPI()

# request bitcoin data from CoinGecko API
bitcoin_data = cg.get_coin_market_chart_by_id(id='bitcoin', vs_currency='usd', days=30)

# save price data
bitcoin_price_data = bitcoin_data['prices']

# convert to dataframe using pandas
data = pd.DataFrame(bitcoin_price_data, columns=['TimeStamp', 'Price'])

# convert date into readable format
data['date'] = data['TimeStamp'].apply(lambda d: datetime.date.fromtimestamp(d/1000.0))

# group data by date
candlestick_data = data.groupby(data.date, as_index=False).agg({"Price": ['min', 'max', 'first', 'last']})

# create candlestick chart
fig = go.Figure(data=[go.Candlestick(x=candlestick_data['date'],
                open=candlestick_data['Price']['first'], 
                high=candlestick_data['Price']['max'],
                low=candlestick_data['Price']['min'], 
                close=candlestick_data['Price']['last'])],
                layout=go.Layout(title=go.layout.Title(text='Bitcoin Candlestick Chart'))
                )

fig.update_layout(xaxis_rangeslider_visible=False)

# show graph 
fig.show()
