import json 
import MySQLdb
import os, glob

class TweetReader():
    def __init__(self):
        # Save the current directory
        #-------CHANGE BEFORE REAL TIME RUN!----------#
        #self.tweetDir =  os.getcwd() + "/data/demo_tweets"
        self.tweetDir = os.getcwd() + "/data/tweets"

    # Looks for a song title in a tweet's text. 
    # If it finds one, it returns the song's echonestID and valence score
    def findSong(self, text):
        if '-' in text:
            print text
            return True
        return None

    # Iterates through each directory that contains tweet json files
    # and processes each tweet.
    def startWalk(self):
        # For each directory that contains tweets (in data/tweets/)
        for dir in os.listdir(self.tweetDir):
            # For each tweet .json file in that directory
            for file in os.listdir(self.tweetDir + '/' + dir):
                if file.endswith('.json'):
                    # Read the file
                    f = open(self.tweetDir + '/' + dir + '/' + file, 'r')
                    tweet = json.loads(f.read())
                    f.close()
                    
                    #Look for a song in the tweet
                    song = self.findSong(tweet['text'])
                    if song is not None:
                        print "Song Found"
                    
def main():
    t = TweetReader()
    t.startWalk()

if __name__ == "__main__":
    main()
