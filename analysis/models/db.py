import MySQLdb
import os
import json


def singleton(cls):
    instances = {}

    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance


class Db:

    def __init__(self):
        # Clean up the args coming in, should be a hash not an object
        config = self._fetch_database_config()
        self.conn = MySQLdb.connect(
            host=config['host'], user=config['user'], passwd=config['password'], db=config['db_name'])

    def _fetch_database_config(self):
        config_file_path = os.path.dirname(__file__) + '/../config/db_config.json'
        with open(config_file_path, 'r') as f:
            config = json.load(f)
            return config

    def _drop_table(self, table_name):
        print """dropping table {0} """.format(table_name)
        self.conn.query("""DROP TABLE IF EXISTS {0}""".format(table_name))

    def create_table(self, table_name, column_definition, drop_table=False):
        if drop_table:
            self._drop_table(table_name)
        self.conn.query(
            """CREATE TABLE IF NOT EXISTS {0} {1} """.format(table_name, column_definition))

    def query(self, query):
        self.conn.query(query)

db = singleton(Db)()
