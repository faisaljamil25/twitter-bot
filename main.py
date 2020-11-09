import tweepy
import time

auth = tweepy.OAuthHandler('{YOUR API KEY}', '{YOUR API KEY SECRET}')

auth.set_access_token('{YOUR ACCESS TOKEN}', '{YOUR ACCESS TOKEN SECRET}')

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

user = api.me()

FILE_NAME = 'last_seen_id.txt'


def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id


def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return


def reply_to_tweets():
    print('retrieving and replying to tweets...')
    """ 
    DEV NOTE: use 1325482760996151297 for testing.
    NOTE: We need to use tweet_mode='extended' below to show
    all full tweets (with full_text). Without it, long tweets
    would be cut off.
    """
    last_seen_id = retrieve_last_seen_id(FILE_NAME)
    mentions = api.mentions_timeline(
        last_seen_id,
        tweet_mode='extended')
    for mention in reversed(mentions):
        print(str(mention.id) + ' - ' + mention.full_text)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, FILE_NAME)
        if '#helloworld' in mention.full_text.lower():
            print('found #helloworld!')
            print('responding back...')
            try:
                mention.favorite()
                print('Tweet Liked')
                api.update_status('@' + mention.user.screen_name +
                                  '#HelloWorld back to you!', mention.id)
            except tweepy.TweepError as e:
                print(e.reason)


while True:
    reply_to_tweets()
    time.sleep(15)
