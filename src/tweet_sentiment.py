from src.article_preprocessing import *
from config.sentiment_config import *
from src.model import *

from modules.tweet_clean import clean_tweet
from textblob import TextBlob
from modules.spacy_nlp import get_entities

polarity_map = {0: "neutral", 1: "positive", -1: "negative"}


def detect_language(tweet):
    b = TextBlob(tweet)
    language = b.detect_language()
    print(tweet, language)
    return language


def get_sentiment(tweet):
    polarity_score = dict()
    polarity_score["positive"] = {"count": 0, "score": 0}
    polarity_score["negative"] = {"count": 0, "score": 0}

    for tweet in tweet.split(". "):
        if len(tweet) == 0:
            continue
        tweet = tweet.lower().strip()
        tweet = clean_tweet(tweet)
        tweet = tweet.split()
        senti = predict_sentiment(tweet, "en", None)
        senti["sentiment"] = polarity_map[senti["sentiment"]]

        if senti["sentiment"] != "neutral":
            polarity = polarity_score[senti["sentiment"]]
            polarity["count"] += 1
            polarity["score"] = max(polarity["score"], abs(senti["score"]))

    positive_polarity = polarity_score["positive"]["count"]
    negative_polarity = polarity_score["negative"]["count"]
    is_polarity_exists = positive_polarity != 0 or negative_polarity != 0
    if is_polarity_exists:
        if positive_polarity > negative_polarity:
            return {
                "sentiment": "positive",
                "score": polarity_score["positive"]["score"],
            }
        else:
            return {
                "sentiment": "negative",
                "score": -polarity_score["negative"]["score"],
            }
    else:
        return {
            "sentiment": "neutral",
            "score": 0,
        }


def make_output(senti, entities, aspects):
    output = dict()
    output["aspect_polarity"] = dict()
    for aspect in aspects:
        output["aspect_polarity"][aspect] = senti
    output["entities"] = entities
    output["overall_polarity"] = senti

    return output


def get_tweet_sentiment(tweet, aspects=None):
    tweet = tweet.lower().strip()
    language = detect_language(tweet)
    if language != "en":
        print("Non English Language Detected!!")
        return dict()

    senti = get_sentiment(tweet)
    entities = get_entities(tweet)

    if aspects is None:
        aspects = entities

    output = make_output(senti, entities, aspects)

    return output


if __name__ == "__main__":

    tweet = "Reliance’s JioMeet Ridiculed At Launch For ‘Copy-Pasting’ Zoom"
    print(get_tweet_sentiment(tweet))

