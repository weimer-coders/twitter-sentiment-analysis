import csv
import sys
import pickle
from sklearn import linear_model
from json import loads, dumps
from operator import itemgetter
from categories import sent_categories, cat_info
from insensitive_dict_reader import InsensitiveDictReader


WEIGHTS = {
    'retweets': .05,
    'favorites': .01
}

MARGIN_SIZE = .1


def interpret(filename):
    with open('data/train/analyzed/%s.csv' % filename, 'r') as f:
        reader = InsensitiveDictReader(f)
        tweets = [row for row in reader]
        f.close()

    # scoring and sentiment analysis
    scores, features, feature_names = analyze(tweets)

    # train machine learning model
    regr = linear_model.BayesianRidge()
    regr.fit(features, scores)

    # Order coeficients
    coefs = []
    for idx, val in enumerate(regr.coef_):
        output = {}
        output['name'] = feature_names[idx]

        if val > 0:
            output['pos/neg'] = ''
        else:
            output['pos/neg'] = '-'

        output['value'] = val
        coefs.append(output)

    # Print out report
    sorted_coefs = sorted(coefs, key=itemgetter('value'))
    report(sorted_coefs, len(scores))

    # Save regr model
    model = {
        'regr': regr,
        'features': feature_names
    }
    modelname = 'models/%s.sav' % filename
    pickle.dump(model, open(modelname, 'wb'))

    return regr, feature_names


def analyze(tweets):
    scored_tweets = []
    scores = []
    feature_names = []
    features = []

    # Calculate score based on retweets and favorites
    for tweet in tweets:
        tweet_data = {}

        score = float(tweet['favorite_count']) * WEIGHTS['favorites']
        score = score + float(tweet['retweet_count']) * WEIGHTS['retweets']
        tweet_data['score'] = score
        # Filter out unnecessary data
        for cat in sent_categories:
            tweet_data[cat] = tweet[cat]

        scored_tweets.append(loads(dumps(tweet_data)))

    # Sort by score and remove the top and bottom 10 percent to remove outliers
    scored_tweets = sorted(scored_tweets, key=itemgetter('score'))
    margin_length = int(len(scored_tweets) * MARGIN_SIZE)
    scored_tweets = scored_tweets[margin_length:-margin_length]

    # Create x(features) and y(scores) lists for ML
    for tweet in scored_tweets:
        # Add scores to score list
        scores.append(tweet.pop('score'))

        # Create list of sentiment category names
        if len(feature_names) == 0:
            feature_names = list(tweet.keys())

        # Create list of features
        feature = []
        for k, v in tweet.items():
            feature.append(float(v))
        features.append(feature)

    return scores, features, feature_names


def report(coefs, num_tweets):
    top5 = sorted(coefs[-5:], key=itemgetter('value'), reverse=True)
    bottom5 = coefs[:5]

    print("Your %s tweets have been analyzed and modeled based on %s lexical categories." % (
        num_tweets,
        len(sent_categories)
    ))

    print("These are the top five categories of words you should use:")
    for item in top5:
        cat = cat_info[item["name"]]
        output = '– ' + cat['name']
        if len(cat['eg']) > 0:
            output += ' (e.g. %s)' % cat['eg']
        print(output)
    print("________")

    print("These are the ones to avoid:")
    for item in bottom5:
        cat = cat_info[item["name"]]
        output = '– ' + cat['name']
        if len(cat['eg']) > 0:
            output += ' (e.g. %s)' % cat['eg']
        print(output)
    print("________")

    more_link = "https://repositories.lib.utexas.edu/bitstream/handle/2152/31333/LIWC2015_LanguageManual.pdf"
    print("For more information on what this means, go to: %s" % more_link)


if __name__ == '__main__':
    interpret(sys.argv[1])
