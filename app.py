import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
from flask import Flask, jsonify, request
import streamlit as st


st.set_page_config (
    page_title = "MarketMood: Stock Sentiment Analyzer",
    page_icon = "📈",
    layout = "wide",
    initial_sidebar_state = "expanded"
)

def scrape_yahoo_news(ticker):
    url = f"https://finance.yahoo.com/quote/{ticker}?p={ticker}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    headlines = []
    
    for tag in soup.find_all('h3'):
        title = tag.get_text(strip = True)
        if title and ticker.upper() in title.upper():
            headlines.append(title)
    return headlines

def analyze_sentiment(text):
    '''
    Using TextBlob to calculate the Sentiment Polarity
    The Range is from -1 to +1 
    '''
    blob = TextBlob(text)
    return blob.sentiment.polarity

app = Flask(__name__)

@app.route('/analyze', methods=["GET"])
def analyze():
    '''
    Flask API route that takes a stock ticker, scrapes the news,
    analyzes the sentiment, and returns a score
    '''
    ticker = request.args.get('ticker')  
    headlines = scrape_yahoo_news(ticker)
    sentiments = [analyze_sentiment(h) for h in headlines]
    average_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0

    return jsonify({
        'ticker': ticker.upper(),
        'average_sentiment': average_sentiment,
        'headlines': headlines,
        'individual_scores': sentiments
    })

def run_streamlit():
    '''
    Streamlit UI to allow user to enter ticker and view sentiment
    '''
    st.title("MarketMood: Stock Sentiment Analyzer")
    ticker = st.text_input("Enter the stock ticker (e.g., NVDA): ")

    if ticker:
        with st.spinner("Analyzing the sentiment..."):
            res = requests.get("http://127.0.0.1:5000/analyze", params = {'ticker': ticker})
            data = res.json()

            sentiment = data["average_sentiment"]
            color = "🟢 Bullish" if sentiment > 0.1 else "🔴 Bearish" if sentiment < -0.1 else "🟡 Neutral"

            st.subheader(f"The Overall Sentiment for {data['ticker']}: {color}")
            st.write(f"The Average Score: {round(sentiment, 2)}")

            st.markdown("### Headlines: ")
            for title, score in zip(data['headlines'], data['individual_scores']):
                st.write(f"**{title}** - Sentiment: {round(score, 2)}")

'''
Entrypoint
'''
if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'runserver':
        app.run(debug = True)
    else:
        run_streamlit()
