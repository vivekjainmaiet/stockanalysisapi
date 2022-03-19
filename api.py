# $DELETE_BEGIN
import pandas as pd
import joblib

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import mysql.connector as connection
from param import config
from data import *

from tradingview_ta import TA_Handler, Interval, Exchange
import tradingview_ta

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/")
def index():
    return dict(
        stocklist="/stocklist",
        stock="/stock?ticker=TCS",
        technical="/technical?ticker=TCS",
        fundamental="/fundamental?ticker=TCS",
        news="/newslist?ticker=TCS",
        twitter="/twitter?ticker=TCS",
        recommendation="/recommendation?ticker=TCS",
        prediction="/prediction?ticker=TCS",
        action="/action?ticker=TCS",
        summary="/summary?symbol=AAPL&exchange=NASDAQ&country=america&interval=1d"
    )


@app.get("/stocklist")
def stocklist():  # 1
    conn = connection.connect(**config)
    mycursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM stocksdb.StocksList;"
    mycursor.execute(query)
    stock_list = mycursor.fetchall()
    return stock_list


@app.get("/stock")
def stock(ticker):  # 1
    conn = connection.connect(**config)
    mycursor = conn.cursor(dictionary=True)
    query = f"SELECT * FROM stocksdb.StocksList where StockCode ='{ticker}';"
    mycursor.execute(query)
    stock = mycursor.fetchone()
    return stock


@app.get("/technical")
def technical(ticker):  # 1
    conn = connection.connect(**config)
    mycursor = conn.cursor(dictionary=True)
    query = f"SELECT * FROM stocksdb.StocksList where StockCode ='{ticker}';"
    mycursor.execute(query)
    stock = mycursor.fetchone()
    stock_id = stock['ID']
    query = f"SELECT * FROM stocksdb.raw_technical where Stock_id = {stock_id}"
    mycursor.execute(query)
    technical_data = mycursor.fetchall()
    return technical_data


@app.get("/fundamental")
def fundamental(ticker):  # 1
    conn = connection.connect(**config)
    mycursor = conn.cursor(dictionary=True)
    query = f"SELECT * FROM stocksdb.StocksList where StockCode ='{ticker}';"
    mycursor.execute(query)
    stock = mycursor.fetchone()
    stock_id = stock['ID']
    query = f"SELECT * FROM stocksdb.raw_fundamental where Stock_id = {stock_id}"
    mycursor.execute(query)
    fundamental_data = mycursor.fetchall()
    return fundamental_data


@app.get("/newslist")
def newslist(ticker):
    conn = connection.connect(**config)
    mycursor = conn.cursor(dictionary=True)
    query = f"SELECT * FROM stocksdb.StocksList where StockCode ='{ticker}';"
    mycursor.execute(query)
    stock = mycursor.fetchone()
    stock_id = stock['ID']
    query = f"SELECT * FROM stocksdb.raw_news where stock_id = {stock_id} ORDER BY ID DESC LIMIT 10;"
    mycursor.execute(query)
    newslist = mycursor.fetchall()
    return newslist


@app.get("/recommendation")
def recommendation(ticker):  # 1
    conn = connection.connect(**config)
    mycursor = conn.cursor(dictionary=True)
    query = f"SELECT * FROM stocksdb.StocksList where StockCode ='{ticker}';"
    mycursor.execute(query)
    stock = mycursor.fetchone()
    stock_id = stock['ID']
    query = f"SELECT * FROM stocksdb.raw_recommendation where stock_id = {stock_id} ORDER BY ID DESC LIMIT 10;"
    mycursor.execute(query)
    recommendation_list = mycursor.fetchall()
    return recommendation_list


@app.get("/twitter")
def twitter(ticker):  # 1
    conn = connection.connect(**config)
    mycursor = conn.cursor(dictionary=True)
    query = f"SELECT * FROM stocksdb.StocksList where StockCode ='{ticker}';"
    mycursor.execute(query)
    stock = mycursor.fetchone()
    stock_id = stock['ID']
    query = f"SELECT * FROM stocksdb.twitter_sentiment where stock_id = {stock_id} ORDER BY ID DESC LIMIT 1;"
    mycursor.execute(query)
    twitter_list = mycursor.fetchall()
    return twitter_list


@app.get("/prediction")
def prediction(ticker):
    conn = connection.connect(**config)
    mycursor = conn.cursor(dictionary=True)
    query = f"SELECT * FROM stocksdb.StocksList where StockCode ='{ticker}';"
    mycursor.execute(query)
    stock = mycursor.fetchone()
    stock_id = stock['ID']
    query = f"SELECT prediction_price,prediction_perchange,prediction_cum_perchange FROM stocksdb.Stock_Prediction where stock_id = {stock_id} ORDER BY ID DESC LIMIT 1;"
    mycursor.execute(query)
    prediction_data = mycursor.fetchall()
    prediction_list = prediction_data[0]['prediction_price'].replace("\n ", "").replace("[[", "").replace("]]", "").split(" ")



    prediction_perchange_list = prediction_data[0]['prediction_perchange'].replace("\n ","").replace("[[","").replace("]]","").split(" ")

    prediction_cum_perchange_list = prediction_data[0]['prediction_cum_perchange'].replace("\n ","").replace("[[", "").replace("]]", "").split(" ")

    prediction_dict = dict.fromkeys(range(len(prediction_list)))
    for i in range(len(prediction_list)):
        prediction_dict[i] = prediction_list[i]



    prediction_perchange_dict = dict.fromkeys(range(len(prediction_perchange_list)))
    for i in range(len(prediction_perchange_list)):
        prediction_perchange_dict[i] = prediction_perchange_list[i]

    prediction_cum_perchange_dict = dict.fromkeys(range(len(prediction_cum_perchange_list)))
    for i in range(len(prediction_cum_perchange_list)):
        prediction_cum_perchange_dict[i] = prediction_cum_perchange_list[i]

    nnnn = {
        "prediction": [prediction_dict],
        "prediction_perchange": [prediction_perchange_dict],
        "prediction_cum_perchange": [prediction_cum_perchange_dict]
    }

    return {
        "prediction": [prediction_dict],
        "prediction_perchange": [prediction_perchange_dict],
        "prediction_cum_perchange": [prediction_cum_perchange_dict]
    }

@app.get("/summary")
def summary(symbol,exchange,country,interval):
    data_summary={"summary":[],"oscillators":[],"moving_averages":[],"indicators":[]}
    handler = TA_Handler(symbol=symbol,exchange=exchange,screener=country,interval=interval)
    analysis = handler.get_analysis()
    data_summary["summary"].append(analysis.summary)
    data_summary["oscillators"].append(analysis.oscillators)
    data_summary["moving_averages"].append(analysis.moving_averages)
    data_summary["indicators"].append(analysis.indicators)
    #data_summary['moving_averages'][0]['COMPUTE'][new_key] = data_summary['moving_averages'][0]['COMPUTE']['EMA10']
    #del data_summary['moving_averages'][0]['COMPUTE']['EMA10']
    return data_summary


@app.get("/action")
def action(ticker):  # 1
    conn = connection.connect(**config)
    mycursor = conn.cursor(dictionary=True)
    query = f"SELECT * FROM stocksdb.StocksList where StockCode ='{ticker}';"
    mycursor.execute(query)
    stock = mycursor.fetchone()
    stock_id = stock['ID']
    query = f"SELECT action FROM stocksdb.Stock_Prediction where stock_id = {stock_id} ORDER BY ID DESC LIMIT 1;"
    mycursor.execute(query)
    prediction_action = mycursor.fetchone()
    return prediction_action
