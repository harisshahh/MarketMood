# MarketMood: A Real-Time Stock Sentiment Analyzer
# By: Haris Shah

import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
from flask import Flask, jsonify, request
import streamlit as st

def scrape_yahoo_news(ticker):
    url = f"https://finance.yahoo.com/quote{ticker}?p={ticker}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

headlines = []
for tag in soup.find_all('h3'):
    title = tag.get_text(strip = True)
    if title and ticker.upper() in title.upper():
        headlines.append(title)
    return headlines

def analyze_sentiment(text):
    '''''
    Using TextBlob to calculate the Sentiment Polarity
    The Range is from -1 to +1 
    '''''
    blob = TextBlob(text)
    return blob.sentiment.polarity

app = Flask(__name__)

@app.route('/analyze', methods = ["GET"])


