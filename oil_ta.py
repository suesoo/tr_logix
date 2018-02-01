#-*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import talib as ta
import mysql.connector
from sklearn import model_selection
import pickle

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import KNeighborsRegressor
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis


def load_data(data_path, db=False):
    '''
    load oil price data from csv file
    :param path: file_path to data file
    :return: dataframe including price data
    '''
    db_data =None
    conn = None

    if db == False:
        b_data = pd.read_table(filepath_or_buffer=data_path)
        print b_data.head()
    else:
        conn = mysql.connector.connect(user='bunker', password='cost', database='OilPrice', host='130.1.12.38')
        query = "select * from Closings order by trade_date asc"
        db_data = pd.read_sql(query, conn)
        conn.close()
        print db_data
    return db_data


def ta_analizer(b_data):
    '''
    implement technical analysis
    :param b_data: dataframe including price & volume
    :return: dataframe including technical analysis with price & volume
    '''
    macd_5, macdsignal_5, macdhist_5 = ta.MACD(b_data['brent'].as_matrix(), fastperiod=5, slowperiod=15, signalperiod=4)
    macd_20, macdsignal_20, macdhist_20 = ta.MACD(b_data['brent'].as_matrix(), fastperiod=20, slowperiod=60, signalperiod=16)
    sma_5 = ta.SMA(b_data['brent'].as_matrix(), timeperiod=5)
    # dollar_sma_5 = ta.SMA(b_data['dollar_idx'].as_matrix(), timeperiod=5)
    sma_20 = ta.SMA(b_data['brent'].as_matrix(), timeperiod=20)
    b_upper, b_middle, b_lower = ta.BBANDS(b_data['brent'].as_matrix(), timeperiod=20)

    rsi = ta.RSI(b_data['brent'].as_matrix())
    b_data['sma_5'] = sma_5
    b_data['sma_20'] = sma_20
    b_data['macd_5'] = macd_5
    b_data['macdsignal_5'] = macdsignal_5
    b_data['macdhist_5'] = macdhist_5
    b_data['macd_20'] = macd_20
    b_data['macdsignal_20'] = macdsignal_20
    b_data['macdhist_20'] = macdhist_20
    b_data['b_upper'] = b_upper
    b_data['b_middle'] = b_middle
    b_data['b_lower'] = b_lower
    # b_data['dollar_sma_5'] = dollar_sma_5

    b_data['rsi'] = rsi
    # b_data['d_price'] = b_data['price'].diff(5)
    b_data['pct5_sma_5'] = b_data['sma_5'].pct_change(5) *100
    b_data['pct5_sma_5'] = b_data['pct5_sma_5'].shift(-5)
    # b_data['pct5_dollar_sma_5'] = b_data['dollar_sma_5'].pct_change(5) * 100
    # b_data['pct5_dollar_sma_5'] = b_data['pct5_dollar_sma_5'].shift(-5)
    b_data['pct5_brent'] = b_data['brent'].pct_change(5) * 100
    b_data['pct5_brent'] = b_data['pct5_brent'].shift(-5)
    b_data['pct5_macd_5'] = b_data['macd_5'].diff(5)/b_data['brent'] *100
    b_data['pct5_macdsignal_5'] = b_data['macdsignal_5'].diff(5)/b_data['brent'] *100
    b_data['pct5_macdhist_5'] = b_data['macdhist_5'].diff(5)/b_data['brent'] *100
    b_data['d5_rsi'] = b_data['rsi'].diff(5)
    b_data['pct5_vol'] = b_data['vol'].pct_change(5)*100
    b_data['b_upper'] = b_data['b_upper'] - b_data['brent']
    b_data['b_lower'] = b_data['b_lower'] - b_data['brent']

    print b_data
    b_data['pct5_sma_20'] = b_data['sma_20'].pct_change(5) *100
    b_data['pct5_sma_20'] = b_data['pct5_sma_20'].shift(-5)
    b_data['pct5_macd_20'] = b_data['macd_20'].diff(5) /b_data['brent']* 100
    b_data['pct5_macdsignal_20'] = b_data['macdsignal_20'].diff(5) /b_data['brent'] * 100
    b_data['pct5_macdhist_20'] = b_data['macdhist_20'].diff(5) /b_data['brent']* 100
    # b_data['d20_rsi'] = b_data['rsi'].diff(20)
    # b_data['pct20_vol'] = b_data['vol'].pct_change(20)
    return b_data

# b_data = load_data('c:\\ml_test\\oilpricedata_2.txt')
# b_data = ta_analizer(b_data)
# b_data.to_csv('c:\\ml_test\\fine_oil_price.txt')

b_data = load_data('c:\\ml_test\\new_data.txt', True)
b_data = ta_analizer(b_data)
b_data.to_csv('c:\\ml_test\\fine_oil_price.txt')
