from modules.patterns import Patterns
import re
import string


def remove_urls(tweet_string, repl):
    return Patterns.URL_PATTERN.sub(repl, tweet_string)


def remove_hashtags(tweet_string, repl):
    return Patterns.HASHTAG_PATTERN.sub(repl, tweet_string)


def remove_mentions(tweet_string, repl):
    return Patterns.MENTION_PATTERN.sub(repl, tweet_string)


def remove_reserved_words(tweet_string, repl):
    return Patterns.RESERVED_WORDS_PATTERN.sub(repl, tweet_string)


def remove_emojis(tweet_string, repl):
    processed = Patterns.EMOJIS_PATTERN.sub(repl, tweet_string)
    return processed.encode("ascii", "ignore").decode("ascii")


def remove_smileys(tweet_string, repl):
    return Patterns.SMILEYS_PATTERN.sub(repl, tweet_string)


def remove_numbers(tweet_string, repl):
    return re.sub(
        Patterns.NUMBERS_PATTERN, lambda m: m.groups()[0] + repl, tweet_string
    )


def remove_emails(tweet_string, repl):
    return Patterns.EMAIL_PATTERN.sub(repl, tweet_string)


def replace_contractions(tweet_tokens):
    mappings = Patterns.CONTRACTION_MAPPINGS
    mappings = {k.lower(): v.lower() for k, v in mappings.items()}
    tweet_tokens = [
        mappings[token] if token in mappings else token for token in tweet_tokens
    ]
    return tweet_tokens


def replace_is_contraction(tweet):
    tweet = re.sub(r"(\w)['`]s", r"\1 is", tweet)
    return tweet


def repititive_func(text):
    grp = text.group(0)
    if len(grp) > 1:
        return grp[0:1]  # can change the value here on repetition


def replace_repititive_words(rep, sentence):
    convert = re.sub(r"(\w)\1{2,}", rep, sentence)
    return convert


def remove_punctuation(tweet):
    punctuation = string.punctuation

    tweet = tweet.translate(str.maketrans("", "", punctuation))
    return tweet


def clean_tweet(tweet):
    repl = ""

    tweet = tweet.lower().replace("`", "'")
    tweet = replace_is_contraction(tweet)
    tweet = replace_repititive_words(repititive_func, tweet)

    tweet = remove_urls(tweet, repl)
    tweet = remove_hashtags(tweet, repl)
    tweet = remove_mentions(tweet, repl)
    tweet = remove_reserved_words(tweet, repl)
    tweet = remove_emojis(tweet, repl)
    tweet = remove_smileys(tweet, repl)
    tweet = remove_numbers(tweet, repl)
    tweet = remove_emails(tweet, repl)

    tweet_tokens = tweet.split()
    tweet_tokens = replace_contractions(tweet_tokens)
    tweet = " ".join(tweet_tokens)
    tweet = remove_punctuation(tweet)

    return tweet
