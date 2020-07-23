import pandas as pd
import nltk
import re
from re import sub
import string
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import spacy
from spacy.lang.hi import Hindi
from spacy import displacy
from collections import Counter
import en_core_web_sm
from google.cloud import translate_v2 as translate

nltk.download("stopwords")
nltk.download("punkt")
nltk.download("wordnet")


# removing named entities
def remove_named_entities(text):
    nlp = en_core_web_sm.load()
    doc = nlp(text)
    words = text.split()
    named_entities = [X.text for X in doc.ents]
    words = [i for i in words if not i in named_entities]
    result = " ".join(words)
    return result


# removing punctuations and numbers
def preprocess(text):
    text = text.lower()
    text = sub(r"[^A-Za-z0-9^,!?.\/'+]", " ", text)
    text = sub(r"\+", " plus ", text)
    text = sub(r",", " ", text)
    text = sub(r"\.", " ", text)
    text = sub(r"!", " ! ", text)
    text = sub(r"\?", " ? ", text)
    text = sub(r"'", " ", text)
    text = sub(r":", " : ", text)
    text = sub(r"\s{2,}", " ", text)

    return text


# tokenize and remove left over named entities as well as lemmatize
def tokenize_named_entities_removal(text):
    nlp = en_core_web_sm.load()
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc]
    tokens = [i for i in tokens if i != "-PRON-"]
    named_entities = [X.text for X in doc.ents]
    words = [i for i in tokens if not i in named_entities]

    return words


# removing stop words
def remove_stopwords(article):
    stopwords = nltk.corpus.stopwords.words("english")
    result = [i for i in article if not i in stopwords]
    return result


# Preprocessing hindi
def preprocess_hin(article):
    text = sub(r"[a-zA-Z]", "", article)
    text = sub(r"[0-9][0-9]", "", text)
    text = sub(r"\n", "", text)
    text = sub(r",", "", text)
    text = sub(r":", "", text)
    text = sub(r"[0-9]", "", text)
    text = sub(r"।", "", text)
    text = sub(r"-", "", text)
    emoji_pattern = re.compile(
        "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "]+",
        flags=re.UNICODE,
    )
    # text = emoji_pattern.sub(r'', text)
    text = text.strip(string.punctuation)

    return text


# tokenizing hindi data
def tokenize_hin(article):
    nlp = Hindi()
    doc = nlp(article)
    tokens = [token.text for token in doc]

    return tokens


#  Getting Synonyms  for a given word with polarity, and word origin
def get_synonyms(word, polarity):
    words = []
    for sysnet in wordnet.sysnets(word):
        for lemma in sysnet.lemmas():
            sys = {}
            sys["origin"] = word
            sys["word"] = lemma.name()
            sys["polarity"] = polarity
            words.append(sys)
    return words


# Get translation
def translator(word, lang_code):
    translate_client = translate.Client()
    translation = translate_client.translate(word, target_language=lang_code)[
        "translatedText"
    ]
    return translation


# Get the synonyms
def get_synonyms(word):
    syn = []
    for synset in wordnet.synsets(word["SynsetTerms"]):
        for lemma in synset.lemmas():
            syn.append(lemma.name())
    syn = set(syn)
    synonyms = []
    try:
        syn.remove(word["SynsetTerms"])
    except KeyError:
        pass
    for i in syn:
        article = {}
        article["parent"] = word["SynsetTerms"]
        article["word"] = i
        article["pos"] = word["PosScore"]
        article["neg"] = word["NegScore"]
        synonyms.append(article)
    synonyms = pd.DataFrame(synonyms)
    return synonyms


# loading the dictionary of ground positive and negative words rem
def load_dicts(filepath, lang_code):

    lang_dict = {
        "hi": "hindi",
        "mr": "Marathi",
        "ml": "Malayalam",
        "gu": "Gujarati",
        "kn": "Kannada",
        "ur": "Urdu",
        "bn": "Bangla",
        "te": "Telugu",
        "ta": "Tamil",
        "or": "Oriya",
        "pa": "Punjabi",
    }
    df = pd.read_csv(filepath)

    word_map = pd.DataFrame()
    word_map["word"] = df[lang_dict[lang_code]]
    word_map["pos"] = df["PosScore"]
    word_map["neg"] = df["NegScore"]

    word_map = word_map.to_dict("record")

    return word_map


# loading the simple spacy tokenizer for english
def spacy_tokenizer(text):
    nlp = en_core_web_sm.load()
    doc = nlp(text)
    tokens = [token.text for token in doc]
    tokens = [i for i in tokens if i != "-PRON-"]
    return tokens


# Sentence Segmentation using spacy for different lanaguages
# Returns the array of strings each being a sentence in a whole article
def sentence_segmentation(article, lang_code):
    if lang_code == "en":
        nlp = en_core_web_sm.load()
    if lang_code == "hi":
        nlp = Hindi()
    nlp.add_pipe(nlp.create_pipe("sentencizer"))
    doc = nlp(article)
    sentences = [i for i in doc.sents]
    sentences = [str(i) for i in sentences]
    return sentences


# loading hindi stopwords
def load_hin_stopwords(filepath):
    with open(filepath, encoding="utf-8") as f:
        stopword = f.read().strip("\ufeff")
    stopword = stopword.split(", ")
    stopwords = [i.strip("'") for i in stopword]
    return stopwords


# Removing hindi stopwords from tokenized text
def remove_hin_stopwords(text, filepath):
    stopwords = load_hin_stopwords(filepath)
    text = [i for i in text if not i in stopwords]
    return text
