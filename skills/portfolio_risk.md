# Skill: portfolio_risk_analyzer

## Description
Evaluate portfolio-level risk metrics across multiple holdings.

## When to Use
Use ONLY when the user asks about:
- risk across multiple tickers simultaneously
- portfolio diversification or exposure
- allocation weights between stocks (e.g. "half X half Y", "60/40", "equal split", "evenly split")

Do NOT use for:
- single stock analysis → use equity_signal instead
- news or sentiment → use news_sentiment instead

## Input
```json
{
  "holdings": [
    { "ticker": "string", "weight": "float" }
  ]
}
```

## Examples
### Input
"What's the portfolio risk with half ADBE and half NVDA?"
```json
{ "holdings": [{ "ticker": "ADBE", "weight": 0.5 }, { "ticker": "NVDA", "weight": 0.5 }] }
```

### Input
"Analyze my holdings: AAPL 60%, TSLA 40%"
```json
{ "holdings": [{ "ticker": "AAPL", "weight": 0.6 }, { "ticker": "TSLA", "weight": 0.4 }] }
```

## Output
```json
{
  "volatility": "float",
  "diversification_score": "float",
  "risk_level": "low | medium | high"
}
```

## Rules
- MUST include all tickers the user mentioned — NEVER substitute or drop any
- Infer weights from natural language: "half" = 0.5, "equal" = evenly distributed
- Weights MUST sum to 1.0
- Respond with RAW JSON only — no markdown, no backticks