# Skill: news_sentiment_analyzer

## Description
Analyze recent news sentiment for a stock.

## When to Use
Use ONLY when:
- user asks about news impact
- sentiment, public perception, headlines

Examples:
- "What's the sentiment on NVDA?"
- "Any bad news about TSLA?"

## Input
```json
{ "ticker": "string" }
```

## Output
```json
{
  "ticker": "string",
  "sentiment": "positive | negative | neutral",
  "score": "float (-1 to 1)",
  "summary": "string"
}
```

## Rules
- summarize concisely 
- avoid speculation 
- must reflect real signals

## Priority
MEDIUM