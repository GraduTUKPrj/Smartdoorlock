
from CMySQLConnection import MySQLConnection


class Mysql:


    def __init__(self):
        self.tablename = ""
        # mysql = MySQLConnector()
        self.mysql = MySQLConnection()

    def insert_userinfo():  # 행 row 추가하기
        try:

            sql = "INSERT INTO {}(, , ,) VALUES ('{}', '{}', '{}')".format()




    def insert_status():  # 행 row 추가하기
        try:

            sql = "INSERT INTO {}() VALUES ({}, '{}', '{}', '{}')".format()


    def select_db():
        try:
            self.mysql = MySQLConnection()
            sql = """SELECT * from %s"""%()



            return "-1"

    def update_db():

        try:



            sql = """UPDATE %s set %s = '%s' WHERE id=%s"""%()




    def delete_user(self, tablename, id):
        try:


            sql = "DELETE from %s where id=%s"%(tablename, id)





    def delete_status(self, tablename):
        try:


            sql = "DELETE from %s"%(tablename)





def MySQLConnector():
    return MySQLConnection()



if __name__ == '__main__':
    csql = CMysql()
