from langchain.tools import tool
import numpy as np
from pydantic import BaseModel, Field

class Holding(BaseModel):
    ticker: str = Field(description="Stock ticker symbol, e.g. AAPL")
    weight: float = Field(description="Portfolio weight as decimal, e.g. 0.5 for 50%")


class PortfolioRiskInput(BaseModel):
    holdings: list[Holding] = Field(
        description="List of holdings with ticker and weight. Weights must sum to 1.0"
    )

@tool(args_schema=PortfolioRiskInput)
def portfolio_risk_analyzer(holdings: list):
    """
    Analyze portfolio-level risk across multiple stock holdings with weights.
    Use ONLY for:
    - Multiple tickers with allocation weights (e.g. "half NVDA half ADBE", "60/40 split")
    - Portfolio diversification or combined risk exposure
    Do NOT use for single stock analysis — use equity_signal instead.
    holdings: list of dicts with keys 'ticker' (str) and 'weight' (float), weights must sum to 1.0
    """
    normalized = [
        {"ticker": h.ticker if hasattr(h, "ticker") else h["ticker"],
         "weight": h.weight if hasattr(h, "weight") else h["weight"]}
        for h in holdings
    ]
    weights = np.array([h["weight"] for h in normalized])
    weights = weights / weights.sum()

    volatility = round(float(np.std(weights)),3)

    if volatility < 0.1:
        risk = "low"
    elif volatility < 0.2:
        risk = "medium"
    else:
        risk = "high"

    diversification = round(float(1 - np.sum(weights**2)))

    return {
        "volatility": volatility,
        "diversification_score": diversification,
        "risk_level": risk
    }