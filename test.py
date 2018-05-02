import pickle
import sys
from insensitive_dict_reader import InsensitiveDictReader
from operator import itemgetter
from training import WEIGHTS


def test_tweets(filename, modelname):
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

    return format_predictions(all_texts, predictions)


def format_predictions(all_texts, predictions):
    tweets = []
    for idx, text in enumerate(all_texts):
        abbrev = text[:50]
        if(len(text) > 50):
            abbrev += '...'

        score = predictions[idx]
        retweets = int(round(score/2 * 1/WEIGHTS['retweets']))
        favorites = int(round(score/2 * 1/WEIGHTS['favorites']))

        tweet = {
            'full_text': text,
            'abbrev_text': abbrev,
            'retweets': retweets,
            'favorites': favorites,
            'score': score
        }

        tweets.append(tweet)

    return sorted(tweets, key=itemgetter('score'), reverse=True)


if __name__ == '__main__':
    scored_tweets = test_tweets(sys.argv[1], sys.argv[2])

    title = "The \"%s\" model predicts this is how your tweets will perform " % sys.argv[2]
    title += "(given an equal worth of both favorites and retweets):"
    print(title)

    headings = ['Tweet', 'Favorites', 'Retweets']
    row_format = "{0:<0} {1:^55} {2:^10} {3:^10}"
    print(row_format.format("", *headings))
    for tweet in scored_tweets:
        row = [tweet['abbrev_text'], tweet['favorites'], tweet['retweets']]
        print(row_format.format("", *row))
