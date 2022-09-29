from statistics import pvariance
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def fetch_data(currency):
    resolution = 3600
    return pd.DataFrame.from_dict(requests.get(
        f'https://ftx.com/api/markets/{currency}/USD/candles?resolution={resolution}'
        ).json()['result'])

st.set_page_config(page_title='Franco Pietrokovsky - PI03',layout='wide',page_icon='Henry.png')
 
l_col,r_col,_,_,_ = st.columns([1,7,3,3,3])

with l_col:
    st.text('')
    st.image('Henry.png',width = 80)
with r_col: 
    st.title('Franco Pietrokovsky - DTS03 - PI03')
    
with st.expander('Documentation'):
    with open('README.md',encoding='utf-8') as f:
        st.markdown(f.read())

st.markdown('---')

markets = pd.DataFrame.from_dict(requests.get('https://ftx.com/api/markets').json()['result'])

currency_data = markets[['name',
                   'last',
                   'bid',
                   'price',
                   'priceHigh24h',
                   'priceLow24h']].sort_values(by='price',ascending=False)

currency_data[['name','name2']]=currency_data['name'].str.split('/',1,expand=True)
currency_data['name']=currency_data['name'].drop_duplicates()

mask = currency_data['name'] != ''
names = ['SUSHI','USDT','BNB','XRP','GMT','DOGE','ETHW','HNT','SNX','OMG']
currency_data = currency_data[mask].loc[[True if value in names else False for value in currency_data['name'].values]]
 
currency_data.dropna(inplace=True)
currency_data.reset_index(inplace=True)

currency_data = currency_data[:10]
currency_data.reset_index(inplace=True)

del currency_data['index']
del currency_data['name2']
del currency_data['level_0']

l_col,r_col = st.columns([2,3])

with l_col:
    st.markdown('# General data:')

with r_col:
    st.markdown('# Top performer:')

l_col,r_col,r2_col,r3_col = st.columns((2,1,1,1))

with l_col:
    
    plot = px.bar(currency_data,x='name',y='price')
    plot.update_traces(textfont_size=12,textangle=0,textposition='outside',cliponaxis=False)
    plot.update_layout(barmode='stack',xaxis_tickangle=-45)
    plot.update_yaxes(title=None)
    plot.update_xaxes(title=None)
    st.plotly_chart(plot)
    

with r_col:
    st.title('')
    
    mask = currency_data['price'] == max(currency_data['price'])
    
    name = currency_data[mask]['name'].values[0]
    low = round(currency_data[mask]['priceLow24h'].values[0],2) 
    current = round(currency_data[mask]['price'].values[0],2)
    
    st.metric(label='Crypto:',value = name)
    st.metric(label='Lowest price (USD):',value=f'$ {low} ')
    
with r2_col:
    st.title('')
    mask = currency_data['price'] == max(currency_data['price'])
    
    price = round(currency_data[mask]['price'].values[0],2)
    
    st.metric(label='Price (USD):',value = f'$ {price} ')
        
with r3_col:
    
    st.title('')
    high = round(currency_data[mask]['priceHigh24h'].values[0],2)

    st.metric(label='Highest price (USD):',value=f'$ {high} ')
    
    st.title('')
    st.markdown('##')
    st.markdown('###')
    
st.markdown('---')
st.markdown('## Detailed data:')

l_col,m_col,m2_col,r_col = st.columns(4)
with l_col:
    currency = st.selectbox(label='Currency:',options=currency_data['name'])
# with m_col:
#     every = st.selectbox(label='Every:',options=['1 hour','24 hours','30 days'])

# if every == '1 hour':
    # resolution = 3600
# elif every == '24 hours':
#     resolution = 86400
# elif every == '30 days':
#     resolution = 86400*30

historic_data = fetch_data(currency)

detailed = st.expander('Details',expanded=True)
dataframe = st.expander('Dataframe')

with dataframe:
    st.markdown('---')
    st.table(historic_data)
with detailed:
    st.markdown('---')
    col1,col2,col3 = st.columns(3)
    
    _,l_col,m_col,m2_col,m3_col,r_col,_ = st.columns([1.5,1,1,1,1,1,1])
    
    open_price = round(historic_data['open'][0],2)
    highest_price = round(historic_data['high'][0],2)
    low_price = round(historic_data['low'][0],2)
    close_price = round(historic_data['close'][0],2)
    variance = round(pvariance([open_price,highest_price,low_price,close_price]),2)
    
    st.markdown('---')
    
    with l_col:
        st.metric(label='Highest price (USD):',value=f'$ {highest_price}')

    with m_col:
        st.metric(label='Lowest price (USD):',value=f'$ {low_price}')
        
    with m2_col:
        st.metric(label='Variance (USD):',value=f'$ {variance}')
    
    with m3_col:
        st.metric(label='Opening price (USD):',value=f'$ {open_price}')
        
    with r_col:
        st.metric(label='Closing price (USD):',value=f'$ {close_price}')

    plot = go.Figure(
        data=[
            go.Candlestick(x=historic_data['startTime'],
                open=historic_data['open'],
                high=historic_data['high'],
                low=historic_data['low'],
                close=historic_data['close']
            )
        ]
    )
    plot.update_layout(title='Historic data')
    
    st.plotly_chart(plot,use_container_width=True)
