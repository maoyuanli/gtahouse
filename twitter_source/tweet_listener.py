from tweepy import StreamListener
from time import sleep

# for streaming
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