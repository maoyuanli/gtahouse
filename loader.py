import json
import os
from time import sleep

import tweepy
from sqlalchemy.orm import sessionmaker
from tweepy import OAuthHandler, StreamListener, API

from database import Tweet
from database import TweetDB

cur_path = os.path.dirname(__file__)
par_path = os.path.dirname(cur_path)
u_dont_need2know = os.path.join(par_path, 'twiken.json')

token = json.load(open(u_dont_need2know, 'r'))

auth = OAuthHandler(token['api_key'], token['api_secret'])
auth.set_access_token(token['access_token'], token['access_secret'])

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


class Listener(StreamListener):

    def on_status(self, status):
        print(
            status.author.screen_name,
            status.created_at,
            status.source,
            status.text,
            '\n'
        )

    def on_error(self, status_code):
        print('Error: {0}'.format(status_code))
        return False

    def on_timeout(self):
        print('Listener time out.')
        return True

    def on_limit(self, track):
        print('Limit: {0}').format(track)
        sleep(10)


# get the members of the list "biznews"(verfied news outlet accounts)
def get_list():
    api = API(auth)
    watch_list = []
    for member in tweepy.Cursor(api.list_members, 'sombrevader', 'biznews').items():
        watch_list.append(member.screen_name)
    return watch_list


# load the tweets of the news outlets into sqlite3 database
def save_user_tweets(screen_name):
    api = API(auth)
    tweets = tweepy.Cursor(api.user_timeline, screen_name=screen_name, tweet_mode='extended').items(1000)
    tweetdb = TweetDB()
    engine = tweetdb.get_engine()
    conn = engine.connect()
    Session = sessionmaker(bind=conn)
    session = Session()
    for tweet in tweets:
        if not 'RT @' in tweet.full_text:
            tweet_row = Tweet(id=tweet.id_str,
                              author=tweet.author.screen_name,
                              tweet=tweet.full_text,
                              timestamp=tweet.created_at)
            session.add(tweet_row)
            session.commit()
