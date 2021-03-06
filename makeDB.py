import MySQLdb as mysql

con = mysql.connect(user="root", passwd="a1b2c3d4", host='localhost')
db = con.cursor()

def recreateDB():
    
    db.execute('DROP DATABASE IF EXISTS mood_prover')
    db.execute('CREATE DATABASE mood_prover')
    db.execute('USE mood_prover')
    
    db.execute('CREATE TABLE user('+
               'id INT NOT NULL auto_increment,'+
               'user_name varchar(30) NOT NULL,'+
               'PRIMARY KEY(id))')
    
    db.execute('CREATE TABLE tweet('+
               'id INT NOT NULL auto_increment,'+
               'twitterID varchar(24) NOT NULL,'+
               'userID INT NOT NULL,'+
               'text varchar(140) NOT NULL,'+
               'creation_time DATETIME NOT NULL,'+
               'valence FLOAT,'+
               'is_music_tweet BOOLEAN,'+
               'PRIMARY KEY(id),'+
               'FOREIGN KEY (userID) REFERENCES user(id))')
    
    db.execute('CREATE TABLE Song('+
               'id INT NOT NULL auto_increment,'+
               'echonestID varchar(24) NOT NULL,'+
               'name varchar(140) NOT NULL,'+
               'artist varchar(140) NOT NULL,'+
               'valence FLOAT NOT NULL,'+
               #'hyperlink varchar(60),'+
               'PRIMARY KEY(id))')

    db.execute('CREATE TABLE TweetToSong('+
               'id INT NOT NULL auto_increment,'+
               'songID INT NOT NULL,'+
               'tweetID INT NOT NULL,'+
               'PRIMARY KEY(id),'+
               'FOREIGN KEY (songId) references Song(id),'+
               'FOREIGN KEY (tweetID) REFERENCES tweet(id))')
    
    print "DONE"

def main():
    created = recreateDB()
    """
    if input("ENTER 1 IF YOU ARE SURE YOU WANT TO RECREATE THE DATABSE: ") == 1:
        print "Gonna create the database"
        created = recreateDB()

    else:
        print "No database created"
        """

main()
