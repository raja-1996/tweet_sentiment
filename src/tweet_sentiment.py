from src.article_preprocessing import *
from config.sentiment_config import *
from src.model import *

from modules.tweet_clean import clean_tweet
from langdetect import detect
from modules.spacy_nlp import get_entities

polarity_map = {0: "neutral", 1: "positive", -1: "negative"}


def detect_language(tweet):
    language = detect(tweet)
    return language


def get_sentiment(tweet):
    sentis = []
    for tweet in tweet.split(". "):
        if len(tweet) == 0:
            continue
        tweet = tweet.lower().strip()
        tweet = clean_tweet(tweet)
        tweet = tweet.split()
        senti = predict_sentiment(tweet, "en", None)
        senti = polarity_map[senti]
        if senti != "neutral":
            sentis.append(senti)

    if len(sentis):
        senti = max(set(sentis), key=sentis.count)
    else:
        senti = "neutral"
    return senti


def get_tweet_sentiment(tweet):
    tweet = tweet.lower().strip()
    language = detect_language(tweet)
    if language != "en":
        print("Non English Language Detected!!")
        return dict()

    senti = get_sentiment(tweet)
    entities = get_entities(tweet)

    output = dict()
    output["sentiment"] = senti
    output["entities"] = entities

    return output


if __name__ == "__main__":
    tweet = "camera is of poor quality"
    print(get_tweet_sentiment(tweet))

    tweet = "jiomeet works really well "
    print(get_tweet_sentiment(tweet))

