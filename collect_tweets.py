import json

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

consumer_name = "kris_stensland"
consumer_key = "FKTiIngLDHGefWkjFCA"
consumer_secret = "QkB5YBiiW1L4PxlbHoFAKJwv9S8tWQdPBGdcwCxZ4Mw"

access_token="425494278-tmaiw5vKUB7qBAv3Yhx37mtou9l5P1gYE7B2fr91"
access_token_secret="4Y1j1DnG6vQJfeeLw9Hu6RiVQGh214Ym0y3fGGXJYF0cu"

STREAM_URL = ""

class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.

    """
    def __init__(self, fileName):
        self.out_file = fileName
        
    def on_data(self, data):
        f = open(self.out_file, 'a')
        f.write(data.replace(",", "\n") + "\n\n")
        f.close()
        print "More data"
        return True

    def on_error(self, status):
        print status

if __name__ == '__main__':
    l = StdOutListener("demo_out.txt")
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(track=['#nowplaying', '#thisismyjam', '#musicmonday', 'np'])
