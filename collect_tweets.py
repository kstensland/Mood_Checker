import os
import time

from datetime import date
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

consumer_name = "kris_stensland"
consumer_key = "FKTiIngLDHGefWkjFCA"
consumer_secret = "QkB5YBiiW1L4PxlbHoFAKJwv9S8tWQdPBGdcwCxZ4Mw"

access_token="425494278-tmaiw5vKUB7qBAv3Yhx37mtou9l5P1gYE7B2fr91"
access_token_secret="4Y1j1DnG6vQJfeeLw9Hu6RiVQGh214Ym0y3fGGXJYF0cu"

class TweetListener(StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.

    """
    def __init__(self, tweetDirIn):
        self.tweetDir = tweetDirIn
        self.today = date.today()
        self.itr = 0
        print "Today is: ", str(self.today)

        path, dirs, files = os.walk(self.tweetDir).next()
        self.numFiles = len(files) + 100
        print "There are currently", self.numFiles, "tweets stored. Adding more now."
        print "\n______________________________________\n\tCOLLECTING TWEETS\tDO NOT CLOSE THIS WINDOW\n______________________________________\n"
        #Create the directory for today
        if not os.path.exists(self.tweetDir + str(self.today)):
            os.makedirs(self.tweetDir + str(self.today))
        
    def on_data(self, data):
        self.itr += 1
        # All files will follow format: data/tweets/[itr].json
        f = open(self.tweetDir + str(self.itr + self.numFiles) + '.json', 'w')
        #print str(self.itr + self.numFiles) + '.json'
        f.write(data)
        f.close()
        return True

    def on_error(self, status):
        print status

if __name__ == '__main__':
    l = TweetListener("data/tweets/")
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(track=['#spotify', '#itunes', '#nowplaying', '#thisismyjam', '#musicmonday', 'np', 'thisismyjam'])
