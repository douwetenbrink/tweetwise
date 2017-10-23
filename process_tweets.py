import argparse, json, format, sentiment


def process_tweets_from_file(fin, fout):
    list_of_tweets = []
    with open(fin) as f:
        for line in f:
            j = json.loads(line)

            # text formatting
            formatted_text = format.format_full(j['text'])
            j['formatted_text'] = formatted_text

            # sentiment
            sent = sentiment.calculate_sentiment(formatted_text)
            j['sentiment'] = sent

            list_of_tweets.append(json.dumps(j))
    
    with open(fout, 'w') as f:
        for tweet in list_of_tweets:
            f.write(tweet+'\n')
    
    print("Successfully processed", len(list_of_tweets), "tweets")


if __name__ == '__main__':
    # Create an argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Input file", required=True)
    parser.add_argument("-o", "--output", help="output file", required=True)
    args = parser.parse_args()

    # Process tweets
    process_tweets_from_file(args.input, args.output)
