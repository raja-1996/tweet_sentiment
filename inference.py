from article_preprocessing import *
from sentiment_config import *
from model import *

headlines = ["camera is awesome"]

sentis = []
for article_eng in headlines:
    article_eng = article_eng.lower().strip()
    article_eng = preprocess(article_eng)
    article_eng = article_eng.split()
    article_eng = remove_stopwords(article_eng)
    senti = predict_sentiment(article_eng, "en", None)
    sentis.append(senti)


print(sentis)

