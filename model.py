import textblob
from textblob import TextBlob
import numpy as np
from gensim.models.fasttext import FastText
import nltk
from nltk.stem import WordNetLemmatizer
from sentiment_config import *
from article_preprocessing import load_dicts
import spacy


positive_polar_words_dicts = {}

for key in positive_polar_words.keys():
    positive_polar_words_dicts[key] = load_dicts(positive_polar_words[key], key)

negative_polar_words_dicts = {}

for key in negative_polar_words.keys():
    negative_polar_words_dicts[key] = load_dicts(negative_polar_words[key], key)

nltk.download("wordnet")
nlp = spacy.load("en")

lemmatizer = WordNetLemmatizer()
"""
# retrieving the sentiment vector 
def sentiment_coeff(article):
	sentiment_vector = []
	for word in article:
		token = TextBlob(word).polarity
		sentiment_vector.append(token)

	return sentiment_vector

"""

# retrieving the term frequency vector
def term_frequency(article):
    term_freq = {}
    for token in article:
        term_freq[token] = article.count(token)
    term_vector = []
    for token in article:
        term_val = term_freq[token] / len(article)
        term_vector.append(term_val)
    return term_vector


def predict_sentiment(article, lang_code, model):
    term_vector = term_frequency(article)
    if lang_code == "en":
        senti_vector = sentiment_coeff(article)
    else:
        senti_vector = get_senti_coeff_indic(article, lang_code, model)
    term_vector = np.array(term_vector)
    senti_vector = np.array(senti_vector)

    polarity = np.dot(term_vector, senti_vector)

    if polarity > 0:
        num = 1
    elif polarity == 0:
        num = 0
    else:
        num = -1

    return num


# Getting the sentiment vectors of each sentence


def get_senti_coeff_indic(article, lang_code, model):
    sentiment_vector = []
    for word in article:
        token = get_word_polarity(word, lang_code, model)
        sentiment_vector.append(token)
    return sentiment_vector


# updated version of the  get polarity function
def get_sentiment(word, word_list, model):
    max_similarity = 0
    for i in word_list:
        try:
            similarity = model.wv.similarity(word, i["word"])
        except KeyError:
            similarity = 0
        if i["pos"] > i["neg"]:
            coeff = i["pos"]
        else:
            coeff = i["neg"]
        score = similarity * coeff
        if score > max_similarity:
            max_similarity = score
    return max_similarity


# Getting similar words


def word_gen(word_array, lang_code, model, polarity):
    words = []

    pos_words_dict = positive_polar_words_dicts[lang_code]
    neg_words_dict = negative_polar_words_dicts[lang_code]

    for i in word_array:
        for word in model.wv.most_similar(i):
            words.append(word[0])

    correct_words = []

    if polarity == 1:
        word_list = pos_words_dict
    else:
        word_list = neg_words_dict

    for i in words:
        if get_sentiment(i, word_list, model) > 0.40:
            correct_words.append(i)

    return correct_words


# Getting word level polarity, return a value between -1 and 1 which reflects  the polarity
def get_word_polarity(word, lang_code, model):

    # loading the positive and negative words of a given language
    pos_words = positive_polar_words_dicts[lang_code]
    neg_words = negative_polar_words_dicts[lang_code]

    # getting a set of absolute positive polar words
    pos_list = [i["word"] for i in pos_words]
    pos_list = set(pos_list)
    # getting a set of absolute negative polar words
    neg_list = [i["word"] for i in neg_words]
    neg_list = set(neg_list)

    if word in pos_list:
        score = 0.9

    elif word in neg_list:
        score = -0.9

    else:
        token_pos = get_sentiment(word, pos_words, model)
        token_neg = get_sentiment(word, neg_words, model)

        if token_pos >= token_neg:
            score = token_pos
            if score < 0.40:
                score = 0
        else:
            score = -1 * token_neg
            if score > -0.40:
                score = 0
    return score


def get_lemmatized_text(text):
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc]
    text = " ".join(tokens)
    return text


# Loading polar words
def get_polar_words(filename):
    with open(filename, encoding="ISO-8859-1") as f:
        words = set(f.read().splitlines())
    return words


pos_words = get_polar_words("resources/pos_lemm.txt")
neg_words = get_polar_words("resources/neg_lemm.txt")


# retrieving the sentiment vector
def sentiment_coeff(article):
    sentiment_vector = []
    flip_polarity = False
    for word in article:
        word_lemmatized = get_lemmatized_text(word)
        if word_lemmatized == "not":
            flip_polarity = True
            score = 0
        elif word_lemmatized in pos_words:
            score = 0.9
        elif word_lemmatized in neg_words:
            score = -0.9
        else:
            score = TextBlob(word).polarity
            if abs(score) < 0.75:
                score = 0
        sentiment_vector.append(score)
    if flip_polarity:
        sentiment_vector = [e * -1 for e in sentiment_vector]
    return sentiment_vector


# Getting word polarity of english words


def get_word_polarity_en(word):
    word_lemmatized = get_lemmatized_text(word)

    if word_lemmatized in pos_words:
        score = 0.9
    elif word_lemmatized in neg_words:
        score = -0.9
    else:
        score = TextBlob(word_lemmatized).polarity
        if score < 0.75:
            score = 0
    return score
