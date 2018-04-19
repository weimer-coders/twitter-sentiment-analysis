import csv
import numpy as np
from empath import Empath
from sklearn import tree


WEIGHTS = {
    'retweets': 5,
    'comments': 2.5,
    'favorites': 1
}

CATEGORIES = [
    'help',
    'violence',
    'money',
    'valuable',
    'hate',
    'cheerfulness',
    'aggression',
    'envy',
    'anticipation',
    'crime',
    'attractive',
    'masculine',
    'health',
    'dispute',
    'nervousness',
    'government',
    'weakness',
    'horror',
    'swearing_terms',
    'leisure',
    'suffering',
    'wealthy',
    'art',
    'fear',
    'irritability',
    'business',
    'exasperation',
    'religion',
    'hipster',
    'surprise',
    'worship',
    'confusion',
    'death',
    'healing',
    'celebration',
    'ridicule',
    'neglect',
    'exotic',
    'order',
    'sympathy',
    'deception',
    'fight',
    'politeness',
    'war',
    'disgust',
    'gain',
    'injury',
    'rage',
    'optimism',
    'sadness',
    'fun',
    'emotional',
    'joy',
    'anger',
    'politics',
    'strength',
    'technology',
    'power',
    'terrorism',
    'poor',
    'pain',
    'beauty',
    'timidity',
    'philosophy',
    'negative_emotion',
    'competing',
    'law',
    'achievement',
    'disappointment',
    'feminine',
    'contentment',
    'positive_emotion'
]


def interpret(filename):
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        tweets = [row for row in reader]
        f.close()

    # scoring and sentiment analysis
    scores, features, feature_names = analyze(tweets)

    test_idx = [100, 200, 300]

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
    clf = tree.DecisionTreeClassifier()
    clf.fit(train_features, train_score)

    # testing machine learning stuff
    print(test_score)
    predictions = clf.predict(test_features)
    print(predictions)
    accuracies = []
    for idx, val in enumerate(test_score):
        accuracies.append(float(predictions[idx]) - float(val))
    print(accuracies)


def analyze(tweets):
    lexicon = Empath()
    scores = []
    feature_names = []
    features = []

    for tweet in tweets:
        score = tweet['favorite_count'] * WEIGHTS['favorites']
        score = score + tweet['retweet_count'] * WEIGHTS['retweets']
        scores.append(score)

        sentiments = lexicon.analyze(tweet['text'], categories=CATEGORIES, normalize=True)

        if len(feature_names) == 0:
            feature_names = list(sentiments.keys())

        feature = []
        for k, v in sentiments.items():
            feature.append(v)
        features.append(feature)

    return scores, features, feature_names


def save(data, filename):
    keys = data[0].keys()
    with open(filename, 'w') as f:
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)
        f.close()


if __name__ == '__main__':
    interpret('nytimes_tweets.csv')
