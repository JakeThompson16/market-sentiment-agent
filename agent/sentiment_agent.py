
from agent.model_interaction import run_model
from config import SENTIMENT_SYSTEM_PROMPT_PATH

def run_sentiment_agent(ticker: str, title: str, summary: str) -> dict:
    """ Runs sentiment agent and returns scoring and primary driver for specific stock """
    with open(SENTIMENT_SYSTEM_PROMPT_PATH, "r") as prompt:
        system_prompt = prompt.read()
    user_document = f"""---
TICKER: {ticker}
TITLE: {title}
SUMMARY: {summary}
---"""

    try:
        return run_model(system_prompt, user_document)

    except Exception as e:
        print("Agent pipeline failed in analyst stage:", e)
        return {
            'sentiment': 'NEUTRAL',
            'confidence': 0.0,
            'primary_driver': 'pipeline error'
        }

def run_sentiment_batch(ticker: str, articles: dict) -> list[dict]:
    """ Runs sentiment agent and returns scoring and primary driver each article in dict """
    return [run_sentiment_agent(ticker, article['title'], article['summary']) for article in articles['articles']]

