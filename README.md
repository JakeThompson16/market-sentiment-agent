# market-sentiment-agent

Agent to track market and individual stock sentiment. Only for equities.

## Setup

pip install yfinance

Create file key.py at root including: OPENROUTER_KEY = {your free key}

## Pipeline

The agent is prompted to evaluate sentiment for a stock.

It first pulls recent articles from yfinance which include that stocks ticker. It then
prompts an openrouter free model to assign a relevance of that article based on if the
ticker is primary focus, secondary, or incidental. These relevance scores are used downstream for sentiment analysis. 
It also applies a bearish, bullish, or neutral classification based on article content 
along with confidence score on [0,1] and a driving factor description explaining its decision. 

The analysis of all articles are then passed to the second agent which composes
signals from all articles into a general market sentiment. This layer also uses
last 5 day pricing to prevent the agent from overreacting to small rebounds after
steep declines. This layer returns a macro score on [-1.0, +1.0] where -1.0 is purely
bearish and +1.0 is purely bullish. It also returns a short executive summary explaining
the reasoning for its classification.

## Constraints

 - The agent is currently susceptible to short term volatile markets and lacks long term sight for decreasing stocks
 - Using openrouter/free which routes to a different model everytime removing deterministic results
 - Because agent routes to different models pipeline failures can occur for individual articles because prompting language cannot reliably guarantee output format for different models

## Example Outputs

Apple (AAPL) 6/14/2026

{'consensus_stance': 'MIXED', 'macro_score': -0.3, 'executive_summary': 'The dominant signal is bearish, driven by a high‑confidence regulatory acti
on article. The strongest counter‑signal is a bullish view that Apple will win the AI race, which moderates the conviction but does not reverse the 
bearish anchor. No reported price jump was overridden by historical trends, as the recent price action shows a modest decline rather than a breakout.'}

Broadcom (AVGO) 6/14/2026

{'consensus_stance': 'BULLISH', 'macro_score': 0.62, 'executive_summary': 'The dominant bullish signal stems from the primary analyst projection of strong upside and margin strength, reinforced by the AI XPV platform launch and accelerating revenue trajectory. A secondary bearish note cites cautious AI guidance, but it is outweighed by the bullish drivers. The modest rally on June 11 was a limited bounce within an overall downtrend and does not negate the bullish outlook.'}

### Disclaimer
*This project is for research and educational purposes and should not be interpreted as financial or trading advice*
