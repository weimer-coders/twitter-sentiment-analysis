---


---

<h1 id="twitter-sentiment-analysis">Twitter Sentiment Analysis</h1>
<p>This creates a model for tweets based on lexical categories and audience engagement. It analyzes past tweets to highlight high and low performing categories and compares tweets for maximum engagement.</p>
<h2 id="how-does-this-work">How does this work?</h2>
<p>First, scrape tweets from a specific Twitter account using <a href="http://scraper.py">scraper.py</a>. This will get around 3,200 of the user’s recent tweets. Next, run the csv through <a href="https://liwc.wpengine.com/">LIWC</a>, which performs the sentiment analysis. Then, run <a href="http://training.py">training.py</a> to create a model based on the previous tweets. In use template.csv in data/test/input to write potential tweets. Then run <a href="http://test.py">test.py</a> to see which tweet scored the highest for potential engagement based on your sentiment analysis model.</p>
<h2 id="limitations">Limitations</h2>
<p>We tried to use empath to perform the sentiment analysis, but it wasn’t giving us any meaningful conclusions. However, using LIWC requires a subscription, which costs $89.95.</p>

