# Location of all the resources and language models to be used for the Modules
# Useful to quickly change resources being used by directly changing the path

# Location of the file containing stopwords for hindi
HINDI_STOPWORDS = "resource_management/hindi_stopwords.txt"

# Location where all the polar words files of all different languages are stored
LANGUAGE_RESOURCES = "data/language_resources/"

# Location where all the FastText Language models are stored
LANGUAGE_MODELS = "data/language_models/"


# list of all the languages that the current code can support
language_codes = {
    "Hindi": "hi",
    "Marathi": "mr",
    "Malayalam": "ml",
    "Gujarati": "gu",
    "Kannada": "kn",
    "Urdu": "ur",
    "Bangla": "bn",
    "Telugu": "te",
    "Tamil": "ta",
    "Oriya": "or",
    "Punjabi": "pa",
}


# Dictionary to get the location of language models by passing the language_code as key
language_model_dict = {
    "hi": LANGUAGE_MODELS + "cc.hi.300.bin",
    "mr": LANGUAGE_MODELS + "cc.mr.300.bin",
    "ml": LANGUAGE_MODELS + "cc.ml.300.bin",
    "gu": LANGUAGE_MODELS + "cc.gu.300.bin",
    "kn": LANGUAGE_MODELS + "cc.kn.300.bin",
    "ur": LANGUAGE_MODELS + "cc.ur.300.bin",
    "bn": LANGUAGE_MODELS + "cc.bn.300.bin",
    "te": LANGUAGE_MODELS + "cc.te.300.bin",
    "ta": LANGUAGE_MODELS + "cc.ta.300.bin",
    "or": LANGUAGE_MODELS + "cc.or.300.bin",
    "pa": LANGUAGE_MODELS + "cc.pa.300.bin",
}

# Dictionary  to get the location of positive words for a given language by passing language_code as key
positive_polar_words = {
    "hi": LANGUAGE_RESOURCES + "pos_words_Hindi.csv",
    "mr": LANGUAGE_RESOURCES + "pos_words_Marathi.csv",
    "ml": LANGUAGE_RESOURCES + "pos_words_Malayalam.csv",
    "gu": LANGUAGE_RESOURCES + "pos_words_Gujarati.csv",
    "kn": LANGUAGE_RESOURCES + "pos_words_Kannada.csv",
    "ur": LANGUAGE_RESOURCES + "pos_words_Urdu.csv",
    "bn": LANGUAGE_RESOURCES + "pos_words_Bangla.csv",
    "te": LANGUAGE_RESOURCES + "pos_words_Telugu.csv",
    "ta": LANGUAGE_RESOURCES + "pos_words_Tamil.csv",
    "or": LANGUAGE_RESOURCES + "pos_words_Oriya.csv",
    "pa": LANGUAGE_RESOURCES + "pos_words_Punjabi.csv",
}

# Dictionary to get the location of negative words for a given language by passing language_code as key
negative_polar_words = {
    "hi": LANGUAGE_RESOURCES + "neg_words_Hindi.csv",
    "mr": LANGUAGE_RESOURCES + "neg_words_Marathi.csv",
    "ml": LANGUAGE_RESOURCES + "neg_words_Malayalam.csv",
    "gu": LANGUAGE_RESOURCES + "neg_words_Gujarati.csv",
    "kn": LANGUAGE_RESOURCES + "neg_words_Kannada.csv",
    "ur": LANGUAGE_RESOURCES + "neg_words_Urdu.csv",
    "bn": LANGUAGE_RESOURCES + "neg_words_Bangla.csv",
    "te": LANGUAGE_RESOURCES + "neg_words_Telugu.csv",
    "ta": LANGUAGE_RESOURCES + "neg_words_Tamil.csv",
    "or": LANGUAGE_RESOURCES + "neg_words_Oriya.csv",
    "pa": LANGUAGE_RESOURCES + "neg_words_Punjabi.csv",
}

