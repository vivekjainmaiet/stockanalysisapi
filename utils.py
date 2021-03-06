import numpy as np
import pandas as pd
import pandas_ta as pta
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer

def compute_rmse(y_pred, y_true):
    '''returns root mean square error'''
    return np.sqrt(((y_pred - y_true) ** 2).mean())


def compute_mpe(y_pred, y_true):
    return abs(y_pred / y_true).mean()


def get_sma(df, period=5, column='Close'):
    '''returns simple moving average of provide column and period'''
    return pta.sma(df[column],length=period)

def get_ema(df, period=10 , column='Close'):
    '''returns simple moving average of provide column and period'''
    return pta.ema(df[column], length=period)

def get_hma(df, period=10 ,column='Close'):
    '''returns simple moving average of provide column and period'''
    return pta.hma(df[column], length=period)

def get_rsi(df,period=14):
    '''returns relative strength index of provided period'''
    return pta.rsi(df['Close'], length = period)

def get_atr(df,period=14):
    '''returns average true range of provided period'''
    return pta.atr(df['High'],df['Low'],df['Close'],length=period)

def get_bband(df,period=20,std=2):
    '''returns Upper , Lower and Middle bolinger band of provided period and std'''
    return pta.bbands(df['Close'],length=period,std=std)

def get_macd(df,fast=12, slow=26, signal=9):
    '''returns Moving average convergence divergence (MACD)'''
    return pta.macd(df['Close'],fast=fast, slow=slow, signal=signal)

def get_adx(df,length=14):
    '''returns ADX of provided period'''
    return pta.adx(df['High'],df['Low'],df['Close'],length=length)

def get_vwap(df):
    '''returns Voumne weighted average'''
    return pta.vwap(df['High'],df['Low'],df['Close'], df['Volume'])


def get_donchian(df, lower_length=20, upper_length=20):
    '''returns Voumne weighted average'''
    return pta.donchian(df['High'],
                        df['Low'],
                        lower_length=20,
                        upper_length=20)

def get_stock_info(ticker):
    '''returns a DataFrame with stock detailed information.'''
    df = pd.DataFrame()
    df = pd.concat([pd.DataFrame([pd.Series(ticker.info.values())]), df], ignore_index=False)
    df.columns =list(ticker.info.keys())
    return df

def isSupport(df,i):
    '''returns True or False for isSupport'''
    support = df['Low'][i] < df['Low'][i-1]  and df['Low'][i] < df['Low'][i+1] and df['Low'][i+1] < df['Low'][i+2] and df['Low'][i-1] < df['Low'][i-2]
    return support

def isResistance(df,i):
    '''returns True or False for isResistance'''
    resistance = df['High'][i] > df['High'][i-1]  and df['High'][i] > df['High'][i+1] and df['High'][i+1] > df['High'][i+2] and df['High'][i-1] > df['High'][i-2]
    return resistance

def isFarFromLevel(df,l,levels):
    '''returns True or False to supress support and registnace duplicate/close lines'''
    s =  np.mean(df['High'] - df['Low'])
    return np.sum([abs(l-x) < s  for x in levels]) == 0

def get_support_registance_levels(df):
    '''returns a DataFrame with stock support and registnace level.'''
    levels = []
    for i in range(2,df.shape[0]-2):
        if isSupport(df,i):
            l = df['Low'][i]
            if isFarFromLevel(df,l,levels):
                levels.append((i,l))
            elif isResistance(df,i):
                l = df['High'][i]
                if isFarFromLevel(df,l,levels):
                    levels.append((i,l))
    return pd.DataFrame(levels, columns=['candle_number','key_level'])


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
