import os

def main():
	tweetDir = "/Users/jimi/Sites/kstensland/Mood_Project_V1/data/tweets/"
	for file in os.listdir(tweetDir+"2014-02-13/"):
		os.system("mv "+tweetDir+"2014-02-13/"+file+" "+tweetDir)
       
main()