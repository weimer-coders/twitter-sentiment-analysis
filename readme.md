# Twitter Sentiment Analysis

This creates a model for tweets based on lexical categories and audience engagement. It analyzes past tweets to highlight high and low performing categories and compares tweets for maximum engagement. 

## How does this work?
First, scrape tweets from a specific Twitter account using [scraper.py](twitter-sentiment-analysis/scraper.py). This will get around 3,200 of the user's recent tweets. Next, run the csv through [LIWC](https://liwc.wpengine.com/), which performs the sentiment analysis. Then, run training.py to create a model based on the previous tweets. In use template.csv in data/test/input to write potential tweets. Then run [test.py](twitter-sentiment-analysis/scraper.py) to see which tweet scored the highest for potential engagement based on your sentiment analysis model. 

## Limitations
We tried to use empath to perform the sentiment analysis, but it wasn't giving us any meaningful conclusions. However, using LIWC requires a subscription, which costs $89.95. 
