import json
import os

import tweepy
from sqlalchemy.orm import sessionmaker
from tweepy import OAuthHandler, API

from twitter_source.database_util import DatabaseUtil
from twitter_source.database_util import Tweets

cur_path = os.path.dirname(__file__)
par_path = os.path.dirname(os.path.dirname(cur_path))
u_dont_need2know = os.path.join(par_path, 'twiken.json')

token = json.load(open(u_dont_need2know, 'r'))

auth = OAuthHandler(token['api_key'], token['api_secret'])
auth.set_access_token(token['access_token'], token['access_secret'])

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


def create_session():
    tweetdb = DatabaseUtil()
    engine = tweetdb.get_engine()
    conn = engine.connect()
    Session = sessionmaker(bind=conn)
    session = Session()
    return session


def save_listedtweets(*args):
    for arg in args:
        tlist = get_list(arg)
        for member in tlist:
            save_usertweets(screen_name=member, type=arg)


# get the members of the twitter list
def get_list(list_name):
    api = API(auth)
    watch_list = []
    for member in tweepy.Cursor(api.list_members, 'sombrevader', list_name).items():
        watch_list.append(member.screen_name)
    return watch_list


# load the tweets of the user's tweets into sqlite3 database
def save_usertweets(screen_name, type):
    api = API(auth)
    tweets = tweepy.Cursor(api.user_timeline, screen_name=screen_name, tweet_mode='extended').items(1000)
    session = create_session()
    for tweet in tweets:
        if not 'RT @' in tweet.full_text:
            tweet_row = Tweets(id=tweet.id_str,
                               author=tweet.author.screen_name,
                               tweet=tweet.full_text,
                               time=tweet.created_at,
                               type=type)
            session.add(tweet_row)
            session.commit()


# load twitter search results to sqlite3 database
def save_searchtweets():
    api = API(auth)
    search_query = '(Toronto OR GTA OR Ontario) AND (real estate OR housing OR home sales OR house market)'
    tweets = tweepy.Cursor(api.search, q=search_query, tweet_mode='extended').items(1500)
    session = create_session()
    for tweet in tweets:
        if not 'RT @' in tweet.full_text:
            tweet_row = Tweets(id=tweet.id_str,
                               author=tweet.author.screen_name,
                               tweet=tweet.full_text,
                               time=tweet.created_at,
                               type='search')
            session.add(tweet_row)
            session.commit()
