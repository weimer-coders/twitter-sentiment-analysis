import csv
from empath import Empath
# import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
from json import loads, dumps
from operator import itemgetter
<<<<<<< HEAD
import pickle
=======
>>>>>>> b3080ea94b87905e2421ab04014826d325fca5c4


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

    model = {
        'regr': regr,
        'feature_names' : feature_names
    }

    #pickle regr
    filename = 'finalized_model.sav'
    pickle.dump(model, open(filename, 'wb'))

    loaded_model = pickle.load(open(filename, 'rb'))
    result = loaded_model['regr'].predict(test_features)

    #pickle feature_names


    # print(result)

    # testing machine learning stuff
    # print(test_score[53])
    # print(test_score[41])
    # print(test_score[250])
    # print(test_score[500])
    predictions = regr.predict(test_features)
    # print('-----')
<<<<<<< HEAD
    # print(result[53])
=======
>>>>>>> b3080ea94b87905e2421ab04014826d325fca5c4
    # print(predictions[41])
    # print(predictions[250])
    # print(predictions[500])

    # The mean squared error
    print("Mean squared error: %.2f"
          % mean_squared_error(test_score, predictions))
    # Explained variance score: 1 is perfect prediction
    print('Variance score: %.2f' % r2_score(test_score, predictions))
    # The coefficients
    coefs = []
    print('Coefficients: \n')
    for idx, val in enumerate(regr.coef_):
        output = {}
        output['name'] = feature_names[idx]

        if val > 0:
            output['pos/neg'] = '+'
        else:
            output['pos/neg'] = '-'

        output['value'] = val
        coefs.append(output)
    sorted_coefs = sorted(coefs, key=itemgetter('value'))
<<<<<<< HEAD
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
=======
>>>>>>> b3080ea94b87905e2421ab04014826d325fca5c4


def analyze(tweets):
    scored_tweets = []
    scores = []
    feature_names = []
    features = []

    # Calculate score based on retweets and favorites
    for tweet in tweets:
        score = float(tweet['favorite_count']) * WEIGHTS['favorites']
        score = score + float(tweet['retweet_count']) * WEIGHTS['retweets']
        tweet['score'] = score
        scored_tweets.append(loads(dumps(tweet)))

    # Sort by score and remove the top and bottom 300 to remove outliers
    scored_tweets = sorted(scored_tweets, key=itemgetter('score'))
    scored_tweets = scored_tweets[300:-300]

    # Creature x(features) and y(scores) lists for ML
    for tweet in scored_tweets:
        # Remove unnesecary properties
        tweet.pop('id')
        tweet.pop('created_at')
        tweet.pop('text')
        tweet.pop('favorite_count')
        tweet.pop('retweet_count')

        # Add to score list
        scores.append(tweet.pop('score'))

        # Create list of sentiment categoreis
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

def save(data, filename):
    keys = data[0].keys()
    with open(filename, 'w') as f:
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)
        f.close()


<<<<<<< HEAD
def sortDictList(arr, sort_key, reverse=False):
    output = [(dict_[sort_key], dict_) for dict_ in arr]
    output.sort(reverse=reverse)
    return [dict_ for (key, dict_) in output]
=======
    return tweets[best_prediction]['text']


if __name__ == '__main__':
    interpret('nytimes_liwc_filtered.csv')
