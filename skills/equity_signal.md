# Skill: Equity Signal Analyzer

## Description
Generate technical trading signals for a given stock ticker.

## When to Use
Use ONLY when the user asks about:
- trend (bullish/bearish)
- technical signals
- buy/sell timing

Do NOT use for:
- portfolio-level questions
- news or sentiment

## Input
```json
{
  "ticker": "string"
}
```

## Output
```json
{
  "ticker": "string",
  "price": "float",
  "trend": "bullish | bearish | neutral",
  "risk": "low | medium | high",
  "confidence": "float (0-1)"
}
```

## Rules
- MUST call tool for real data 
- NEVER hallucinate price 
- Return JSON ONLY

## Error Handling
```json
{
  "status": "error",
  "message": "string"
}
```

## Examples
### Input
```json
{ "ticker": "AAPL" }
```
### Output
```json
{
  "ticker": "AAPL",
  "price": 182.3,
  "trend": "bullish",
  "risk": "medium",
  "confidence": 0.87
}
```
## Priority
HIGH