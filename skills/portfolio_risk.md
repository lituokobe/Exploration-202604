# Skill: Portfolio Risk Analyzer

## Description
Evaluate portfolio-level risk metrics.

## When to Use
Use ONLY when:
- user provides multiple holdings
- asks about diversification, risk, exposure

Examples:
- "Is my portfolio risky?"
- "Analyze my holdings: AAPL 50%, TSLA 50%"

## Input
```json
{
  "holdings": [
    { "ticker": "string", "weight": "float" }
  ]
}
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
- weights must sum ≈ 1 
- normalize if needed 
- no hallucinated assets

## Priority
HIGH