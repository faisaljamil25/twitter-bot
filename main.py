import tweepy
import time

auth = tweepy.OAuthHandler('{YOUR API KEY}', '{YOUR API KEY SECRET}')

auth.set_access_token('{YOUR ACCESS TOKEN}', '{YOUR ACCESS TOKEN SECRET}')

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

user = api.me()

search = 'Biden2020'
nrTweets = 10

for tweet in tweepy.Cursor(api.search, search).items(nrTweets):
    try:
        print('Tweet Liked')
        tweet.favorite()
        time.sleep(10)
    except tweepy.TweepError as e:
        print(e.reason)
    except StopIteration:
        break