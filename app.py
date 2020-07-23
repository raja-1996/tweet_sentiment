from flask import Flask, request
from src.tweet_sentiment import get_tweet_sentiment

app = Flask(__name__)


@app.route("/sentiment")
def get_sentiment():
    text = request.args.get("text")
    return get_tweet_sentiment(text)


if __name__ == "__main__":
    app.run()
