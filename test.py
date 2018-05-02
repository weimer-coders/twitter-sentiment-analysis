import pickle
import sys
from insensitive_dict_reader import InsensitiveDictReader


def get_best(filename, modelname):
    load = pickle.load(open('models/%s.sav' % modelname, 'rb'))

    model = load['regr']
    features_list = load['features']

    with open('data/test/analyzed/%s.csv' % filename, 'r') as f:
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
    best_tweet = get_best(sys.argv[1], sys.argv[2])
    print('----------\n' + best_tweet)
