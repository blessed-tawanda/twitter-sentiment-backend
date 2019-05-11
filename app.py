from TwitterClient import TwitterClient
from flask import Flask,request,jsonify
from flask_cors import CORS

tc = TwitterClient()

app = Flask(__name__)
CORS(app)

@app.route('/twittersentiment', methods=['POST'])
def twittersentiment():
  topic = request.get_json()
  tweets = tc.get_tweets(topic['query'],topic['count'])
  if len(tweets) == 0:
    message = {
      'message': 'No tweets found on that topic'
    }
    return jsonify(message)
  else:
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    statistics = {
      'positiveTweets': {
        'tweets': ptweets,
        'percentage': len(ptweets)/len(tweets) * 100
      },
      'negativeTweets': {
        'tweets': ntweets,
        'percentage': len(ntweets)/len(tweets) * 100
      },
      'neutralTweets' : {
        'percentage': ((len(tweets) - len(ntweets) - len(ptweets))/len(tweets)) * 100
      }
    }

    return jsonify(statistics)

@app.route('/setsentiment', methods=['POST'])
def setsentiment():
  tweet = request.get_json()
  if tc.get_tweet_sentiment(tweet['text']) == 'positive':
    tweet['Class'] = 'positive'
  elif tc.get_tweet_sentiment(tweet['text']) == 'negative':
    tweet['Class'] = 'negative'
  elif tc.get_tweet_sentiment(tweet['text']) == 'neutral':
    tweet['Class'] = 'neutral'
  
  return jsonify(tweet)


if __name__ == '__main__':
  app.run(port=4000)

