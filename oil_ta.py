#-*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import talib as ta
from sklearn import model_selection
import pickle

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import KNeighborsRegressor
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis


def load_data(data_path):
    '''
    load oil price data from csv file
    :param path: file_path to data file
    :return: dataframe including price data
    '''
    b_data = pd.read_table(filepath_or_buffer=data_path)
    b_data['vol'] = b_data['vol_1'] + b_data['vol_2']
    return b_data


def ta_analizer(b_data):
    '''
    implement technical analysis
    :param b_data: dataframe including price & volume
    :return: dataframe including technical analysis with price & volume
    '''
    macd, macdsignal, macdhist = ta.MACD(b_data['price'].as_matrix(), fastperiod=12, slowperiod=26, signalperiod=9)
    rsi = ta.RSI(b_data['price'].as_matrix())
    b_data['macd'] = macd
    b_data['macdsignal'] = macdsignal
    b_data['macdhist'] = macdhist
    b_data['rsi'] = rsi
    # b_data['d_price'] = b_data['price'].diff(5)
    b_data['d_price'] = b_data['price'].diff(5)
    b_data['d_price'] = b_data['d_price'].shift(-5)
    b_data['d_macd'] = b_data['macd'].diff(5)
    b_data['d_macdsignal'] = b_data['macdsignal'].diff(5)
    b_data['d_macdhist'] = b_data['macdhist'].diff(5)
    b_data['d_rsi'] = b_data['rsi'].diff(5)
    return b_data


b_data = load_data('oilpricedata.txt')
b_data = ta_analizer(b_data)
b_data.to_csv('c:\\fine_oil_price.txt')
