import streamlit as st
import pandas as pd
import json 
import finplot as fplt
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import requests

def data(setup,month,week):
    #convert json to dataframe
    df = pd.read_json('Stock List.json')
    #taking only the important columns from the dataframe
    new_df = df[['close','high','low','open','symbol','date']]
    #indexing it by date
    new_df = new_df.set_index('date')
    new_df.index = pd.to_datetime(new_df.index)
    new_df = new_df.sort_index()
    if setup==0:
        if month>=1 and month<=12:
            if month!=10 and month!=11 and month!=12:
                st='2021-0'+str(month)
            else:
                st='2021-'+str(month)
        if week==1:
            ws1='-01'
            ws2='-07'
        elif week==2:
            ws1='-08'
            ws2='-14'
        elif week==3:
            ws1='-15'
            ws2='-21'
        elif week==4:
            ws1='-22'
            ws2='-29'
        else:
            ws1='-30'
            ws2='-31'
        new_df=new_df[st+ws1:st+ws2]
    if setup==1:
        if month>=1 and month<=12:
            if month!=10 and month!=11 and month!=12:
                st='2021-0'+str(month)
            else:
                st='2021-'+str(month)
        new_df=new_df[st]
    #grouping them by their symbols so we can visualize them
    grouped = new_df.groupby(['symbol'])
    #converting those grouped_Dataframes into list for each company
    list_grouped = list(grouped)
    return list_grouped

st.title('OHLC Dashboard')

#assigning a key value pair to each company
companies = {'AAPL': 0, 'ABBV': 1, 'ABT': 2, 'ACN': 3, 'ADBE': 4, 'ADSK': 5, 'AMAT': 6, 'AMD': 7, 'AMGN': 8, 'AMT': 9, 'AMZN': 10, 'ASML': 11, 'AVGO': 12, 'AXP': 13, 'BA': 14, 'BABA': 15, 'BAC': 16, 'BBL': 17, 'BHP': 18, 'BLK': 19, 'BMY': 20, 'BUD': 21, 'C': 22, 'CHTR': 23, 'CMCSA': 24, 'COST': 25, 'CRM': 26, 'CSCO': 27, 'CVX': 28, 'DHR': 29, 'DIS': 30, 'EL': 31, 'FB': 32, 'GOOG': 33, 'GOOGL': 34, 'GS': 35, 'HD': 36, 'HDB': 37, 'HON': 38, 'IBM': 39, 'INTC': 40, 'INTU': 41, 'ISRG': 42, 'JD': 43, 'JNJ': 44, 'JPM': 45, 'KO': 46, 'LIN': 47, 'LLY': 48, 'LOW': 49, 'MA': 50, 'MCD': 51, 'MDT': 52, 'MRK': 53, 'MRNA': 54, 'MS': 55, 'MSFT': 56, 'NEE': 57, 'NFLX': 58, 'NKE': 59, 'NOW': 60, 'NVDA': 61, 'NVO': 62, 'NVS': 63, 'ORCL': 64, 'PDD': 65, 'PEP': 66, 'PFE': 67, 'PG': 68, 'PM': 69, 'PYPL': 70, 'QCOM': 71, 'RIO': 72, 'RTX': 73, 'RY': 74, 'SAP': 75, 'SBUX': 76, 'SCHW': 77, 'SE': 78, 'SHOP': 79, 'SNAP': 80, 'SNY': 81, 'SONY': 82, 'SQ': 83, 'T': 84, 'TD': 85, 'TGT': 86, 'TM': 87, 'TMO': 88, 'TMUS': 89, 'TSLA': 90, 'TSM': 91, 'TXN': 92, 'UL': 93, 'UNH': 94, 'UNP': 95, 'UPS': 96, 'V': 97, 'VZ': 98, 'WFC': 99, 'WMT': 100, 'XOM': 101}
#giving user choice to select a company
company_name = st.selectbox('Select a company ', companies)

types = {'Weekly':0, 'Monthly':1, 'Yearly':2}
type_nm=st.selectbox('Range of plot you would like to see', types)
Month = {'January': 0, 'February': 1, 'March': 2, 'April': 3, 'May': 4, 'June': 5, 'July': 6, 'August': 7, 'September': 8, 'October': 9, 'Novemeber': 10, 'December': 11}
#giving user choice to select a company
if type_nm=='Weekly':
        s=0
        month = st.selectbox('Select the month ', Month)
        m=int(Month[month])+1
        weeks = {'1':0, '2':1, '3':2 , '4':3 , '5':4}
        week=st.selectbox('Select the week', weeks)
        w=int(weeks[week])+1
elif type_nm=='Monthly':
        month = st.selectbox('Select the month ', Month)
        s=1
        m=int(Month[month])+1
        w=0
else:
        s=2
        m=0
        w=0
        

#st.write(companies[company_name]) : making sure correct key value pair is being selected
grouped_companies = data(s,m,w)
grouped_companies[companies[company_name]][1]

#implementing differnt visualization techniques choosen by the user
graph_modalities = {'OHLC':0, 'Candlestick-charts':1, 'Colored-Bar':2, 'Vertex-Line':3, 'Hollow-Candle':4}
graph_chosen = st.selectbox('Select the type of Graph ',graph_modalities)
#st.write(graph_modalities[graph_chosen])

if(graph_modalities[graph_chosen]==0):
	fig = go.Figure(data=[go.Ohlc(x=grouped_companies[companies[company_name]][1].index,
                open=grouped_companies[companies[company_name]][1]['open'],
                high=grouped_companies[companies[company_name]][1]['high'],
                low=grouped_companies[companies[company_name]][1]['low'],
                close=grouped_companies[companies[company_name]][1]['close'])])
	st.plotly_chart(fig)

elif(graph_modalities[graph_chosen]==1):
	fig = go.Figure(data=[go.Candlestick(x=grouped_companies[companies[company_name]][1].index,
                open=grouped_companies[companies[company_name]][1]['open'],
                high=grouped_companies[companies[company_name]][1]['high'],
                low=grouped_companies[companies[company_name]][1]['low'],
                close=grouped_companies[companies[company_name]][1]['close'])])
	st.plotly_chart(fig)

elif(graph_modalities[graph_chosen]==2):
	fig = px.histogram(grouped_companies[companies[company_name]][1],x=grouped_companies[companies[company_name]][1].index, y=[grouped_companies[companies[company_name]][1]['open'],
                 grouped_companies[companies[company_name]][1]['low'], grouped_companies[companies[company_name]][1]['high'], grouped_companies[companies[company_name]][1]['close']])
	st.plotly_chart(fig)

elif(graph_modalities[graph_chosen]==3):
	fig = px.line(grouped_companies[companies[company_name]][1],x=grouped_companies[companies[company_name]][1].index, y=[grouped_companies[companies[company_name]][1]['open'],
                 grouped_companies[companies[company_name]][1]['low'], grouped_companies[companies[company_name]][1]['high'], grouped_companies[companies[company_name]][1]['close']])
	st.plotly_chart(fig)
	 


elif(graph_modalities[graph_chosen]==4):
	fig = px.box(grouped_companies[companies[company_name]][1],x=grouped_companies[companies[company_name]][1].index, y=[grouped_companies[companies[company_name]][1]['open'],
                 grouped_companies[companies[company_name]][1]['low'], grouped_companies[companies[company_name]][1]['high'], grouped_companies[companies[company_name]][1]['close']])
	st.plotly_chart(fig)



symbol = company_name.lower()
url = f'https://cloud.iexapis.com/stable/stock/{symbol}/quote?token={token}'
r = requests.get(url=url)
info = r.json()

companyName = info['companyName']
marketOpen = info['iexOpen']
marketClose = info['iexClose']
previousVolume = info['previousVolume']
peRatio = info['peRatio']
primaryExchange = info['primaryExchange']
week52High = info['week52High']
week52Low = info['week52Low']

st.title('Company Information: '+companyName)
st.markdown('**Market Open**: '+str(marketOpen))
st.markdown('**Market Close**: '+str(marketClose))
st.markdown('**PreviousVolume**: '+str(previousVolume))
st.markdown('**price-to-earnings (P/E) ratio**: '+str(peRatio))
st.markdown('**Primary Exchange**: '+primaryExchange)
st.markdown('**Highest in last year **: '+str(week52High))
st.markdown('**Lowest in last year **: '+str(week52Low))
