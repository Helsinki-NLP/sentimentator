# Skeleton for CSV dump script

import sqlite3
import csv

connect_db = sqlite3.connect('sentimentator/db.sqlite')
output_file = open('en.csv', 'w')
output_csv = csv.writer(output_file)

# Example: dump all sentences with the annotation label 'neg'
cursor = connect_db.execute('select sentence.sentence from sentence inner join annotation on sentence.id = annotation.sentence_id where annotation.annotation like "%neg%"')

rows = cursor.fetchall()
output_csv.writerows(rows)

output_file.close()
