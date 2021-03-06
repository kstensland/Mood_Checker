from time import sleep
import sys
import json 
import MySQLdb as mysql
import os, glob
from datetime import *

import urllib2
import httplib2
http = httplib2.Http()

class TweetReader():
    def __init__(self):
        # Save the current directory
        #-------CHANGE BEFORE REAL TIME RUN!----------#
        #self.tweetDir =  os.getcwd() + "/data/demo_tweets"
        #self.tweetDir = os.getcwd() + "/data/tweets"
        self.tweetDir = os.getcwd() + "/data/demo_tweets"
        self.goodTweetDir = os.getcwd() + "/data/useful_tweets"
        self.ECHONEST_API_KEY = "SNR0SROSCFKUZIZRH"
        self.echonestLink = "http://developer.echonest.com/api/v4/song/search?api_key=API_KEY_HERE&format=json&results=10&artist=ARTIST_HERE&bucket=audio_summary&title=SONG_HERE"
        self.echonestLink = self.echonestLink.replace("API_KEY_HERE", self.ECHONEST_API_KEY)
        self.youtubeData = "https://gdata.youtube.com/feeds/api/videos/ID_HERE?v=2&alt=json"
        self.timjLink = "http://api.thisismyjame.com/1/USER_NAME_HERE/jams.json"
        self.con = mysql.connect(user="root", passwd="a1b2c3d4", host='localhost', db="mood_prover")
        self.db = self.con.cursor()
        
    # expand shortened links
    # youtu.be, t.co, bit.ly, ow.ly, tinyurl.com, su.pr
    def expandLink(self, tinyUrl):
        content = ""
        try:
            req = urllib2.urlopen(tinyUrl)
            print req.url
            return req.url
        except ValueError:
            print "No response from", link
        except urllib2.URLError:
            print "URLError while expanding: ",tinyUrl
        return ''
    
    def cleanText(self, text):
        words = text.split(" ")
        newText = ""
        for word in words:
            if '#' not in word and 'http://' not in word:
                newText += word+' '
    
        return newText.replace('\n', ' ')
    
    # Removes featured artists from the artist name.
    # Ex: 'Eminem ft. Rihanna' becomes 'Eminem'
    def removeFeaturedArtists(self, phrase):
        phrase = phrase.lower()

        ftVariations = [' ft ', ' feat ', ' featuring ']
        for ft in ftVariations:
            pos = phrase.find(ft)
            
            if pos > -1:
                print "Featured artist found in", phrase
                return phrase[:pos]
        return phrase

    def checkEchonest(self, artist, song):
        url = self.echonestLink.replace('ARTIST_HERE', artist.replace(' ','+'))
        url = url.replace('SONG_HERE', song.replace(' ', '+'))
        resp, content = http.request(url, 'GET')
        enData = json.loads(content)['response']
        try:
            return enData
        except:
            return None

    # Checks for songs in text that has 1 or more '-' or 'by'
    def checkPhrasesForSong(self, phraseA, phraseB, seperator):

        if phraseA is '' or phraseB is '':
            print 'One of the phrases is blank'
            print 'A:', phraseA
            print 'B:', phraseB
            return None
                
        splitPhraseA = self.removeFeaturedArtists(phraseA).split(' ')
        splitPhraseB = self.removeFeaturedArtists(phraseB).split(' ')
        
        # Else: Check if we can remove some words in the phrase
        # For example, turn, 'Love this song Rolling Stones - Satisfaction' 
        # into 'Rolling Stones - Satisfaction'
        # OR 'Rolling Stones - Satisfaction is the best song ever' into the same thing.
        # use the '-1' because we don't want to check an empty string
        for i in range(len(splitPhraseA)-1):
            for j in reversed(range(len(splitPhraseB))):
                phrase1 = ' '.join(splitPhraseA[i:])
                phrase2 = ' '.join(splitPhraseB[:j])
                
                if phrase1 == '' or phrase2 == '':
                    continue

                artist = phrase1.replace(' ','+')
                song = phrase2.replace(' ', '+')
                try:
                    # Check if they are in order [artist] - [song]
                    enData = self.checkEchonest(artist, song)
                    
                    # If EchoNest found any songs from the data
                    if len(enData['songs']) > 0:
                        #print "Found Song:"
                        #print enData['artist_name'],seperator,enData['title']
                        #print enData['audio_summary']['valence']
                        #print "---------"
                        return enData['songs'][0]
                # There was no song found for those two phrases
                except KeyError:
                    """print "-----ERROR-----"
                    print phraseA, seperator, phraseB
                    print phrase1, seperator, phrase2
                    """
                    #raise
                    #print "Key error with", url
                except UnicodeEncodeError:
                    print 'One of the phrases has a UnicodeEncodeError'
                    print '1:', phrase1
                    print '2:', phrase2

                except ValueError:
                    print "ValueError", resp
                    print 'url', url

                try:
                    # Check if the song is in order [song] - [artist]
                    enData = self.checkEchonest(song, artist)
                    
                    # If EchoNest found any songs from the data
                    if len(enData['songs']) > 0:
                        #print "Found Song:"
                        #print enData['artist_name'],seperator,enData['title']
                        #print enData['audio_summary']['valence']
                        #print "---------"
                        return enData['songs'][0]

                    
                except KeyError:
                    """print "-----ERROR-----"
                    print phraseA, seperator, phraseB
                    print phrase1, seperator, phrase2
                    """
                    #raise
                    #print "Key error with", url
                except UnicodeEncodeError:
                    print 'One of the phrases has a UnicodeEncodeError'
                    print '1:', phrase1
                    print '2:', phrase2
                except ValueError:
                    print "ValueError", resp
                    print 'url', url
                
                sleep(0.5)
        

    
    def crawlLastFM(self, url):
        return
    
    def crawlTIMJ(self, url):
        #First get the youtube video ID

        """
        # Get the title of the youtube video
        try:
            url = self.youtubeData.replace('ID_HERE', videoID)
            resp, content = http.request(url, 'GET')
            data = json.loads(content)['entry']['title']
            return data
        except:
            raise
            """
        return False

    # Gets the title of a youtube video so we can try to find a song from it
    def crawlYoutube(self, url):
        return False
        
        #First get the youtube video ID
        videoID = url[len(url)-11:]    
        # Get the title of the youtube video
        try:
            url = self.youtubeData.replace('ID_HERE', videoID)
            resp, content = http.request(url, 'GET')
            data = json.loads(content)['entry']['title']
            return data
        except:
            raise
        return False

    def checkURL(self, url):
        # If url isn't a valid string
        if type(url) != type(u'') or len(url) < 0:
            return False
        
        if url is None or len(url) < 0: 
            return False
        
        if 'youtube.com' in url or 'youtu.be' in url:
            return self.crawlYoutube(url)
        """
        if 'thisismyjam.com' in url:
            return self.crawlTIMJ(url)
            
        if 'last.fm' in url:
            return self.crawlLastFM(url)
        """
        return False

    def processText(self, text, seperator):
        # Split the text up into different parts based on the seperator
        sects = text.split(seperator)
        for i in range(1, len(sects)):
            found = self.checkPhrasesForSong(seperator.join(sects[:i]), seperator.join(sects[i:]), seperator)
            if found is not None:
                return found
            
        return False

    # Looks for a song title in a tweet's text. 
    # If it finds one, it returns the song's echonestID and valence score
    def findSong(self, text, urls):
        # If there is a link to youtube, thisismyjam, or last.fm, 
        # we can get the artist and song title from it.
        if urls is not []:
            for url in urls:
                title = self.checkURL(url['expanded_url'])
                
                if title is not None and title != False:
                    # Test for [Artist] - [song]
                    if '-' in title:
                        # Split the text up into different parts based on the location of 'by'
                        songFound = self.processText(title, '-')            
                        print songFound
                        if songFound is not None and songFound is not False:
                            return songFound

                    # Test for [song] by [artist]
                    if 'by' in title:
                        # Split the text up into different parts based on the location of 'by'
                        songFound = self.processText(title, 'by')
                        if songFound is not None and songFound is not False:
                            return songFound
                        
        #This removes hashtags and hyperlinks
        #It actually cleans up the text quite a bit
        cleanText = self.cleanText(text)        
        # Test for [Artist] - [song]
        if '-' in cleanText:
            # Split the text up into different parts based on the location of 'by' 
            songFound = self.processText(cleanText, '-')            
            if songFound is not None and songFound is not False:
                return songFound

        # Test for [song] by [artist]
        if 'by' in cleanText:
            # Split the text up into different parts based on the location of 'by'
            songFound = self.processText(cleanText, 'by')
            if songFound is not None and songFound is not False:
                return songFound
        
        return False    

    def storeTweetInDB(self, tweetData, enData):
        
        try:
            # Store the user data into the interface
            # First check to make sure the user doesn't already exist
            self.db.execute("select id from User where User.user_name = %s", 
                            (str(tweetData['user']['id']),))
            userID = self.db.fetchone()
            
            # If the user is not already in the database
            if userID is None:
                self.db.execute("INSERT INTO User(user_name) VALUES (%s)", (str(tweetData['user']['id']),))
                self.con.commit()
                self.db.execute("select id from User where User.user_name = %s", 
                                (str(tweetData['user']['id']),))
                userID = self.db.fetchone()
            
            # Next store the tweet into the database
            self.db.execute("SELECT id FROM tweet WHERE tweet.twitterID = %s", 
                            (tweetData['id_str'],))
            tweetID = self.db.fetchone()

            # If the tweet is not already in the database
            if tweetID is None:
                pyDate = datetime.strptime(tweetData['created_at'], "%a %b %d %H:%M:%S +0000 %Y")
                date = pyDate.strftime("%Y-%m-%d %H:%M:%S")
                self.db.execute("INSERT INTO tweet("+
                                "twitterID, userID, text, creation_time, is_music_tweet) "+ 
                                "VALUES (%s, %s, %s, %s, %s)", 
                                (tweetData['id_str'], userID, tweetData['text'], date,
                                 True,))
                self.con.commit()
                self.db.execute("select id from tweet where tweet.twitterID = %s", 
                                (tweetData['id'],))
                tweetID = self.db.fetchone()

            # Next store the song into the database
            self.db.execute("SELECT id FROM Song WHERE Song.echonestID = %s", 
                            (enData['id'],))
            songID = self.db.fetchone()
            
            # If the song is not already in the database
            if songID is None:
                self.db.execute("INSERT INTO Song("+
                                "echonestID, name, artist, valence) "+ 
                                "VALUES (%s, %s, %s, %s)", 
                                (enData['id'], enData['title'], 
                                 enData['artist_name'],enData['audio_summary']['valence'],))
                self.con.commit()
                self.db.execute("select id from song where song.echonestID = %s", 
                                (enData['id'],))
                songID = self.db.fetchone()
            
            self.db.execute("INSERT INTO TweetToSong("+
                            "songID, tweetID) "+ 
                            "VALUES (%s, %s)", 
                            (tweetID, songID,))
                             
            self.con.commit()
            print enData['artist_name'], 'by', enData['title']
            return True
        except UnicodeEncodeError:
            print "unicode error with ", tweetData['id_str']
        except:
            print enData.keys()
            raise
        return False

    # Iterates through each directory that contains tweet json files
    # and processes each tweet.
    def startWalk(self):
        counter = 0
        tweetNum = 0
        # For each directory that contains tweets (in data/tweets/)
        for file in os.listdir(self.tweetDir):
            tweetNum += 1
            if file.endswith('.json'):
                try:
                    # Read the file
                    f = open(self.tweetDir + '/' + file, 'r')
                    tweet = json.load(f)
                    f.close()
                except:
                    print "Could not read tweet: ", self.tweetDir + '/' + dir + '/' + file
                    print "Have successfully read", tweetNum, "files"
                    raise
                
                    #Look for a song in the tweet
                song = self.findSong(tweet['text'], tweet['entities']['urls'])
                if song is not None and song is not False:
                    
                    if self.storeTweetInDB(tweet, song):
                        os.system("mv "+self.tweetDir+"/"+file+" "+self.goodTweetDir)
                        counter += 1 
                        
                    print "------------------------"

        print counter, "Songs found out of ", tweetNum, "tweets"
                    
def main():
    t = TweetReader()
    t.startWalk()

if __name__ == "__main__":
    main()
