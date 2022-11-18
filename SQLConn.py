
import pymysql   import collections

def _convert(data):

    if isinstance(data, str):
        return str(data)
    elif isinstance(data, collections.Mapping):
        #return dict(map(_convert, data.iteritems()))
        return dict(map(_convert, data.items()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(_convert, data))
    else:
        return data


class MySQLConnection(object):
    # init method with configurations.
    def __init__(self):

        
        host = ''
        password = ""

        self.conn = pymysql.connect(host=host, user='', password=password, db='', charset='utf8') 



    # Begin fetch
    def fetch(self, query):
        #cursor = self.conn.cursor(dictionary=True)
        cursor = self.conn.cursor(pymysql.cursors.DictCursor)

        cursor.execute(query)
        data = list(cursor.fetchall())
        cursor.close()

        return _convert(data)


    # Begin run_mysql_query
    def run_mysql_query(self, query):
        #cursor = self.conn.cursor(dictionary=True)
        cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        data = cursor.execute(query)
        self.conn.commit()
        cursor.close()
        return data

    def escape_string(self, query):
        string_escaper = self.conn.converter.escape
        escaped_string = string_escaper(query)
        return escaped_string


