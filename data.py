import pandas as pd
import yfinance as yf
import numpy as np
import pandas_ta as pta
from utils import *
from pandas_datareader import data as pdr
import os
import joblib
from google.cloud import storage

PATH_TO_LOCAL_MODEL = 'model.joblib'
BUCKET_NAME = "one-stop-stock-analysis"

yf.pdr_override()

def get_technical(symbol="INFY.NS",start="2017-01-01", end="2021-04-30"):
    '''returns a DataFrame with stock technical data'''
    df = pdr.get_data_yahoo(symbol, start=start, end=end)
    #df.drop(columns=['Adj Close'],inplace=True)

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
    #breakpoint()
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


def download_model(storage_location='models/stockanalysis/Pipeline/INFY.NS.joblib',bucket=BUCKET_NAME,rm=False):
    client = storage.Client().bucket(bucket)
    blob = client.blob(storage_location)
    blob.download_to_filename('model.joblib')
    print("=> pipeline downloaded from storage")
    model = joblib.load('model.joblib')
    if rm:
        os.remove('model.joblib')
    return model
