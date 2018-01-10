import sqlite3
import csv
from sentimentator.model import *

connect_db = sqlite3.connect('db.sqlite')
output_file = open('en.csv', 'wb')
output_csv = csv.writer(output_file)

cursor = connect_db.execute('select * from sentence')

output_csv.writerow(x[0] for x in cursor.description)
output_csv.writerows(cursor.fetchall())

output_file.close()
