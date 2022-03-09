import pymysql

conn = pymysql.connect(host='localhost', user='tester', password='tester1234',db ='doorlock_schema', charset='utf8')
cursor = conn.cursor()

sql = '''CREATE TABLE status_table (
        time datetime,
        category tinyint not null,
        temperature float
        )
        '''

with conn:
    with conn.cursor() as cur:
        cur.execute(sql)
        conn.commit()