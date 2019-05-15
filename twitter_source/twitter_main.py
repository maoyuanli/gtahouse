from twitter_source.database_util import DatabaseUtil
from twitter_source.tweets_ETL import save_listedtweets, save_searchtweets


def purge_table(table_name):
    tweetdb = DatabaseUtil()
    engine = tweetdb.get_engine()
    conn = engine.connect()
    query = 'delete from {0};'.format(table_name)
    conn.execute(query)


def populate_table():
    save_listedtweets('biznews', 'realtor')
    save_searchtweets()


if __name__ == '__main__':
    purge_table('tweets')
    populate_table()
