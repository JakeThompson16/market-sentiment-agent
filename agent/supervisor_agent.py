
from agent.model_interaction import run_model
from agent.sentiment_agent import run_sentiment_batch

from config import SUPERVISOR_SYSTEM_PROMPT_PATH
from fetch_data.source_yfinance import fetch_yfinance_stock_sentiment

import yfinance as yf
import json


def run_full_sentiment_analysis(ticker: str) -> dict:
    """
    Returns an analysis of a stock with the following sections;
    "consensus_stance": "BULLISH" | "BEARISH" | "MIXED" | "NEUTRAL",
    "macro_score": 0.00, // A strictly calculated float between -1.00 (purely bearish) and +1.00 (purely bullish)
    "executive_summary": "A cohesive 2-3 sentence strategic brief synthesizing why these data points result in the selected posture."
    """
    articles = fetch_yfinance_stock_sentiment(ticker)
    reactions = run_sentiment_batch(ticker, articles)

    if not reactions:
        return {
            "consensus_stance": "NEUTRAL",
            "macro_score": 0.0,
            "executive_summary": f"No recent market news or sentiment data points were available for {ticker}."
        }

    serialized_reactions = json.dumps(reactions)

    history = yf.Ticker(ticker).history(period="5d")
    history = history.reset_index()
    history['Date'] = history['Date'].dt.strftime('%Y-%m-%d')
    history = history[["Date", "Open", "Close", "Volume"]]

    history_dict = history.to_dict('records')
    serialized_history = json.dumps(history_dict)

    with open(SUPERVISOR_SYSTEM_PROMPT_PATH, "r") as f:
        system_prompt = f.read()

    user_document = f"""---
TARGET TICKER: {ticker}
TOTAL DATA POINTS: {len(reactions)}

DATA EXTRACTION PAYLOAD:
{serialized_reactions}

LAST 5 DAYS HISTORY PAYLOAD:
{serialized_history}
---"""

    try:
        return run_model(system_prompt, user_document)

    except Exception as e:
        print("agent pipeline failed in supervisor stage:", e)
        return {
            "consensus_stance": "NEUTRAL",
            "macro_score": 0.0,
            "executive_summary": "pipeline failure, no sentiment analysis available"
        }