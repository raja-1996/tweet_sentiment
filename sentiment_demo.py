from src.article_preprocessing import *
from config.sentiment_config import *
from src.model import *

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


# output = {
#     "aspect_polarity": [
#         {
#             {"aspect": "jio", "sentiment": "positive", "score": 0.98},
#             {"aspect": "jiomeet", "sentiment": "negative", "score": 0.98},
#             {"aspect": "jiomart", "sentiment": "positive", "score": 0.68},
#         }
#     ],
#     "entities": ["jio", "jiomeet", "reliance", "ambani"],
# }

