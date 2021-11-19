import pymysql
import csv


db_connection = pymysql.connect(
    user='root',
    passwd='614614',
    host='127.0.0.1',
    db='library',
    charset='utf8'
)

con = db_connection
cur = con.cursor(pymysql.cursors.DictCursor)

with open('book_list.csv', encoding='utf-8') as datas:
    records = csv.DictReader(datas)
    result = [(w['title'], w['publisher'], w['author'], w['publication_date'],
               w['pages'], str(w['isbn']), w['description'], w['link']) for w in records]

cur.executemany("insert into book(title, publisher, author, publication_date, pages, isbn, description, link) values(%s, %s, %s, %s, %s, %s, %s, %s);", result)
con.commit()
con.close()
