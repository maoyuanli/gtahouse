import tweepy
from tweepy import OAuthHandler, API

from utils.database_util import DatabaseUtil
from utils.database_util import Tweets
from utils.fetch_token import TokenFetcher

tf = TokenFetcher('token.json')
api_key = tf.fetch_token('api_key')
api_secret = tf.fetch_token('api_secret')
access_token = tf.fetch_token('access_token')
access_secret = tf.fetch_token('access_secret')

auth = OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


def save_listedtweets(*args:'twitter list name(s)'):
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


DButil = DatabaseUtil()


# load the tweets of the user's tweets into sqlite3 database
def save_usertweets(screen_name, type:'flag/category of the tweet, i.e. search, list'):
    api = API(auth)
    tweets = tweepy.Cursor(api.user_timeline, screen_name=screen_name, tweet_mode='extended').items(1000)
    session = DButil.create_session()
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
    session = DButil.create_session()
    for tweet in tweets:
        if not 'RT @' in tweet.full_text:
            tweet_row = Tweets(id=tweet.id_str,
                               author=tweet.author.screen_name,
                               tweet=tweet.full_text,
                               time=tweet.created_at,
                               type='search')
            session.add(tweet_row)
            session.commit()


def purge_table(table_name):
    conn = DButil.get_conn()
    query = 'delete from {0};'.format(table_name)
    conn.execute(query)


def populate_table():
    save_listedtweets('biznews', 'realtor')
    save_searchtweets()


def main():
    purge_table('tweets')
    populate_table()


if __name__ == '__main__':
    main()
