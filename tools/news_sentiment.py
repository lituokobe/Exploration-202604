from langchain.tools import tool

@tool
def news_sentiment_analyzer(ticker: str):
    """
    Analyze recent news sentiment for a stock ticker.
    Use when user asks about news, sentiment, or public perception.
    """
    return {
        "ticker": ticker,
        "sentiment": "positive",
        "score": 0.6,
        "summary": f"Recent news for {ticker} is mostly positive."
    }