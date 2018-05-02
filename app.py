import csv
import numpy as np
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
from json import loads, dumps
from operator import itemgetter
import pickle
from categories import sent_categories
from insensitive_dict_reader import InsensitiveDictReader


WEIGHTS = {
    'retweets': .05,
    'comments': .025,
    'favorites': .01
}


def interpret(filename):
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        tweets = [row for row in reader]
        f.close()

    # scoring and sentiment analysis
    scores, features, feature_names = analyze(tweets)

    test_idx = list(range(0, len(scores), 5))

    # training data
    train_score = np.delete(scores, test_idx)
    train_features = np.delete(features, test_idx, axis=0)

    # testing data
    test_score = []
    test_features = []
    for pk in test_idx:
        test_score.append(scores[pk])
        test_features.append(features[pk])

    # machine learning stuff
    regr = linear_model.BayesianRidge()
    regr.fit(train_features, train_score)

    # model = {
    #     'regr': regr,
    #     'feature_names': feature_names
    # }
    #
    # #pickle regr
    # filename = 'finalized_model.sav'
    # pickle.dump(model, open(filename, 'wb'))
    #
    # loaded_model = pickle.load(open(filename, 'rb'))
    # result = loaded_model['regr'].predict(test_features)
    # print(predictions[41])
    # print(predictions[250])
    # print(predictions[500])

    # The mean squared error
    # print("Mean squared error: %.2f"
    #       % mean_squared_error(test_score, predictions))
    # # Explained variance score: 1 is perfect prediction
    # print('Variance score: %.2f' % r2_score(test_score, predictions))

    # The coefficients
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
    sorted_coefs = sorted(coefs, key=itemgetter('value'))
    # #print(sorted_coefs)
    top5 = sorted(sorted_coefs[-5:], key=itemgetter('value'), reverse=True)
    # # print(top5)
    # print("------")
    bottom5 = sorted_coefs[:5]
    # print(bottom5)
    print("Here are categories to use:")
    for item in top5:
        print(item["name"])
    print("------")
    print("Here are categories to avoid:")
    for item in bottom5:
        print(item["name"])
    print("------")
    print("For more information on what this means, go to: https://repositories.lib.utexas.edu/bitstream/handle/2152/31333/LIWC2015_LanguageManual.pdf")

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

    # Sort by score and remove the top and bottom 300 to remove outliers
    scored_tweets = sorted(scored_tweets, key=itemgetter('score'))
    scored_tweets = scored_tweets[300:-300]

    # Creature x(features) and y(scores) lists for ML
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

# def report(scores,features):
#     print(sorted_coefs)


def get_best(filename, modelname):
    model, features_list = interpret('data/train/analyzed/' + modelname)

    with open('data/test/analyzed/' + filename, 'r') as f:
        reader = InsensitiveDictReader(f)
        tweets = [row for row in reader]
        f.close()

    all_texts = []
    all_features = []
    for tweet in tweets:
        all_texts.append(tweet['text'])

        features = []
        for feature_name in features_list:
            features.append(float(tweet[feature_name]))
        all_features.append(features)

    predictions = list(model.predict(all_features))
    best_prediction = predictions.index(max(predictions))

    return tweets[best_prediction]['text']


if __name__ == '__main__':
    best_tweet = get_best('test.csv', 'nytimes.csv')
    print('----------\n' + best_tweet)
