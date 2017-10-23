import json, time
from datetime import datetime

SENTIMENT_VECTOR_SIZE = 3


def load_data(fname):
    output = []
    with open(fname) as f:
        for line in f:
            j = json.loads(line)
            output.append(j)
    return output


def add_sentiments(sentiments, price_change, output):
    sentiments.sort(reverse=True)
    sentiments = sentiments[:SENTIMENT_VECTOR_SIZE]
    if len(sentiments) == SENTIMENT_VECTOR_SIZE:
        change = 1 if price_change > 0 else 0
        output.append((sentiments, change))


def build_features(ftweets, fprices):
    tweets = load_data(ftweets)
    prices = load_data(fprices)
    
    features = []
    sentiments = []
    p = 0
    
    for tweet in tweets:
        if p >= len(prices):
            break

        price_time = datetime.utcfromtimestamp(prices[p]['timestamp'])
        tweet_time = datetime.strptime(tweet['created_at'], '%Y-%m-%dT%H:%M:%S')

        if price_time.hour - tweet_time.hour == 1:
            sentiments.append(tweet['sentiment']['compound'])
        else:
            add_sentiments(sentiments, float(prices[p]['ticker']['change']), features)
            sentiments.clear()
            p += 1
    
    add_sentiments(sentiments, float(prices[p]['ticker']['change']), features)

    return features


def write_features_to_csv(features, fname):
    with open(fname, 'w') as f:
        column_headers = ','.join(['S'+str(i) for i in range(SENTIMENT_VECTOR_SIZE)]) + ',CHANGE\n'
        f.write(column_headers)
        for feature_vector in features:
            x = [str(v) for v in feature_vector[0]]
            y = str(feature_vector[1])
            f.write(','.join(x))
            f.write(',' + y)
                




f = build_features('processed_tweets.txt', 'prices.txt')
write_features_to_csv(f, 'test_features.csv')
