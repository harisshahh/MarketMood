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
def analyze():
    '''
    Flask API route that takes a stock ticker, scrapes the news,
    analyzes the sentiment, and returns a score
    '''
    ticket = requests.arg.get('ticker')
    headlines = scrape_yahoo_news(ticker)
    sentiments = [analyze_sentiment(h) for h in headlines]
    average_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0

    return jsonify({
        'ticker': ticker.upper(),
        'average_sentiment': average_sentiment,
        'headlines': headlines,
        'individual_scores': sentiments
    })


