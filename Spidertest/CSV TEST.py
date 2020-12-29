import csv

with open('2020-01-23~2020-02-07.csv','r') as f:
    reader = csv.reader(f)
    result = list(reader)
    print(result[1][1])