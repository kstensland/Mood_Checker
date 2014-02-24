import MySQLdb as mysql
from time import sleep

def main():
	con = mysql.connect(user="root", passwd="a1b2c3d4", host='localhost', db="mood_prover")
	db = con.cursor()
	selectSQL = "SELECT id, text, valence FROM tweet WHERE valence is NULL ORDER BY id ASC"
	selectSQL2 = "SELECT id, text, valence FROM tweet WHERE valence is NULL AND id > %s ORDER BY id ASC"
	db.execute(selectSQL)

	row = db.fetchone()
	recentRow = 0
	while True:
		if row is not None:
			print row
			recentRow = row[0]
			row = db.fetchone()
		else:
			sleep(0.3)
			db.execute(selectSQL2, (recentRow,))
			row = db.fetchone()
		con.commit()

if __name__ == "__main__":
    main()