import sqlite3
import csv

connect_db = sqlite3.connect('sentimentator/db.sqlite')
output_file = open('en.csv', 'w')
output_csv = csv.writer(output_file)

cursor = connect_db.execute('select * from sentence')

output_csv.writerow(x[0] for x in cursor.description)
output_csv.writerows(cursor.fetchall())

output_file.close()
