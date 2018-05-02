# adapted from https://gist.github.com/gabrielsoule/638201ac0cc12828d3cde69035a25336
# twitter documentation: https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object

import tweepy
from time import sleep
import os
import csv
import sys
import credentials

consumer_key = credentials.consumer_key
consumer_secret = credentials.consumer_secret
access_token = credentials.access_token
access_token_secret = credentials.access_token_secret


def get_all_tweets(screen_name):
    # Twitter only allows access to a users most recent 3240 tweets with this method

    # authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    # initialize a list to hold all the tweepy Tweets
    alltweets = []

    # make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name=screen_name, count=200, tweet_mode='extended')

    # save most recent tweets
    alltweets.extend(new_tweets)

    # save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print ("getting tweets before %s" % (oldest))

        # all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest, tweet_mode='extended')

        # save most recent tweets
        alltweets.extend(new_tweets)

        # update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print ("...%s tweets downloaded so far" % (len(alltweets)))

    # transform the tweepy tweets into a 2D array that will populate the csv
    # this is where I tried to include tweet.reply_count and tweet.quote_count but it didn't work
    outtweets = [
        [tweet.id_str, tweet.created_at, tweet.favorite_count, tweet.retweet_count, tweet.full_text.encode("utf-8")]
        for tweet in alltweets
    ]

    # write the csv
    with open('data/train/scraped/%s.csv' % screen_name, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["id", "created_at", "favorite_count", "retweet_count", "text"])
        writer.writerows(outtweets)

    pass


if __name__ == '__main__':
    # pass in the username of the account you want to download
    get_all_tweets(sys.argv[1])
