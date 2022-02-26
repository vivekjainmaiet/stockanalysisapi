import pandas as pd
import yfinance as yf
import numpy as np
import pandas_ta as pta
from stockanalysis.utils import *
from pandas_datareader import data as pdr
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
yf.pdr_override()

def get_technical(symbol="INFY.NS",start="2017-01-01", end="2021-04-30"):
    '''returns a DataFrame with stock technical data'''
    df = pdr.get_data_yahoo(symbol, start=start, end=end)
    df.drop(columns=['Adj Close'],inplace=True)

    df['ema12'] = get_ema(df, column='Close', period=12)
    df['ema21'] = get_ema(df, column='Close', period=21)
    df['ema26'] = get_ema(df, column='Close', period=26)
    df['ema34'] = get_ema(df, column='Close', period=34)
    df['ema55'] = get_ema(df, column='Close', period=55)
    df['ema99'] = get_ema(df, column='Close', period=99)
    df['ema200'] = get_ema(df, column='Close', period=200)
    df['hma12'] = get_hma(df, column='Close', period=12)
    df['hma21'] = get_hma(df, column='Close', period=21)
    df['hma26'] = get_hma(df, column='Close', period=26)
    df['hma34'] = get_hma(df, column='Close', period=34)
    df['hma55'] = get_hma(df, column='Close', period=55)
    df['hma99'] = get_hma(df, column='Close', period=99)
    df['hma200'] = get_hma(df, column='Close', period=200)
    df['rsi'] = get_rsi(df, period=14)
    df['atr'] = get_atr(df, period=14)
    df['bb_upper'] = get_bband(df, period=20, std=2)['BBU_20_2.0']
    df['bb_lower'] = get_bband(df, period=20, std=2)['BBL_20_2.0']
    df['macd_signal'] = get_macd(df, fast=12, slow=26,
                                 signal=9)['MACD_12_26_9']
    df['macd_line'] = get_macd(df, fast=12, slow=26, signal=9)['MACDs_12_26_9']
    df['adx'] = get_adx(df, length=14)['ADX_14']
    df['vwap'] = get_vwap(df)
    cleaned_df = clean_data(df)
    return cleaned_df

def clean_data(df, test=False):
    '''returns a DataFrame without outliers and missing values'''
    df = df.dropna(how='any')
    df = df.reset_index()
    return df


def split_predict(scaled_data, X):
    # Create the training data set
    # Create the scaled training data set
    train_data = scaled_data
    # Split the data into x_train and y_train data sets
    x_train = []
    y_train = []

    for i in range(60, len(train_data)):
        x_train.append(train_data[i - 60:i, 0])
        y_train.append(X[i, 0])
        if i <= 61:
            print(x_train)
            print(y_train)
            print()

    # Convert the x_train and y_train to numpy arrays
    x_train, y_train = np.array(x_train), np.array(y_train)

    # Reshape the data
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
    # x_train.shape

    return x_train, y_train


def set_pipeline(cleaned_data):
    '''returns a pipelined model'''
    data_pipe = Pipeline([('stdscaler', StandardScaler())])
    preproc_pipe = ColumnTransformer(
        [('data', data_pipe, cleaned_data.columns)], remainder="drop")

    pipe = Pipeline([('preproc', preproc_pipe)])

    scaled_data = pipe.fit_transform(cleaned_data)
    return scaled_data, pipe
