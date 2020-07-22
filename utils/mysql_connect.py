import os
import pymysql


class MysqlConnect():

    def __init__(self):
        self.path = './data/'
        self.hostname = os.getenv("DB_HOST")
        self.username = os.getenv("DB_USERNAME")
        self.password = os.getenv("DB_PASSWORD")
        self.database = os.getenv("DB_DATABASE")
        self.conn = pymysql.connect(self.hostname, self.username, self.password, self.database, charset='utf8')
        self.cur = self.conn.cursor()

    def select(self, query):
        data = []
        try:
            self.cur.execute(query)
            return self.cur.fetchall()
        except Exception as msg:
            print(msg)

    def execute(self, sql):
        try:
            self.cur.execute(sql)
            self.conn.commit()
        except Exception as msg:
            print(msg)
            self.conn.rollback()

    def execute_file(self, file):

        with open(self.path + file + '.sql', 'r', encoding='utf-8') as fd:
            sql_file = fd.read()

        sql_commands = sql_file.split(';')
        for command in sql_commands:
            command = command.strip('\n')
            command = command.replace('\n', ' ')
            if command == '':
                continue
            try:
                self.cur.execute(command)
            except Exception as msg:
                print(msg)
                self.conn.rollback()
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()
