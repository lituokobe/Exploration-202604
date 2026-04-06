import random

from langchain.tools import tool

from tools.mockup_data import NVDA, NVDA_trend, NVDA_risk, NVDA_confidence, AAPL, AAPL_trend, AAPL_risk, \
    AAPL_confidence, ADBE, ADBE_trend, ADBE_risk, ADBE_confidence


@tool
def equity_signal_analyzer(ticker: str):
    """
    Analyze stock trend and return technical signal including price, trend, risk, and confidence.
    Use this tool when the user asks about stock trend or trading signal.
    """
    num = random.randint(0, 4)
    if ticker == "NVDA":
        price = NVDA[num]
        trend = NVDA_trend[num]
        risk = NVDA_risk[num]
        confidence = NVDA_confidence[num]
    elif ticker == "AAPL":
        price = AAPL[num]
        trend = AAPL_trend[num]
        risk = AAPL_risk[num]
        confidence = AAPL_confidence[num]
    elif ticker == "ADBE":
        price = ADBE[num]
        trend = ADBE_trend[num]
        risk = ADBE_risk[num]
        confidence = ADBE_confidence[num]
    else:
        price = 100.53
        trend = "bullish"
        risk = "low"
        confidence = 0.6

    return {
        "ticker": ticker,
        "price": price,
        "trend": trend,
        "risk": risk,
        "confidence": confidence
    }