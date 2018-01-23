# Skeleton for CSV dump script

import sqlite3
import csv

connect_db = sqlite3.connect('sentimentator/db.sqlite')
output_file = open('en.csv', 'w')
output_csv = csv.writer(output_file)

cursor = connect_db.execute('select * from sentence')

rows = cursor.fetchall()
output_csv.writerows(rows)

output_file.close()
