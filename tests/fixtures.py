import MySQLdb as Db
from tests.settings import MYSQL_CONNECTION_PARAMS


class Fixture:
    def __init__(self):
        self._connection = None

    def cursor(self):
        if not self._connection:
            self._connection = Db.connect(**MYSQL_CONNECTION_PARAMS)

        return self._connection.cursor()

    def create_database(self):
        create_connection_params = MYSQL_CONNECTION_PARAMS.copy()
        db = create_connection_params.pop('db')
        con = Db.connect(**create_connection_params)

        cur = con.cursor()
        cur.execute('DROP DATABASE IF EXISTS `{0}`;'.format(db))
        cur.execute('CREATE DATABASE `{0}`;'.format(db))
        cur.close()

    def create_key_value_example(self):
        cur = self.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS `key_value_example` (
                  `id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                  `name` varchar(128) NOT NULL UNIQUE,
                  `value` int(11) NOT NULL
                ) ENGINE=InnoDB;""")
        cur.close()

    def create_multicolumn_example(self):
        cur = self.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS `multicolumn_example` (
                  `id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                  `identifier1` varchar(128) NOT NULL UNIQUE,
                  `identifier2` int(11) NOT NULL UNIQUE,
                  `identifier3` varchar(128) NOT NULL UNIQUE,
                  `value1` int(11) NOT NULL,
                  `value2` varchar(255) NOT NULL,
                  `value3` text
                ) ENGINE=InnoDB;""")
        cur.close()

    def insert_into_key_value_example(self, key, value):
        cur = self.cursor()
        cur.execute('insert into `key_value_example` values (DEFAULT, %s, %s);', (key, value))
        self._connection.commit()
        cur.close()

    def insert_into_multicolumn_example(self, ids, vals):
        cur = self.cursor()
        cur.execute("insert into `multicolumn_example` values (DEFAULT, '%s', %s, '%s', %s, '%s', '%s');" %
                    tuple(ids + vals))
        self._connection.commit()
        cur.close()

    def count_multicolumn_example(self):
        cur = self.cursor()
        cur.execute('select COUNT(*) from `multicolumn_example`')
        (result,) = cur.fetchone()
        cur.close()
        return result

    def count_key_value_example(self):
        cur = self.cursor()
        cur.execute('select COUNT(*) from `key_value_example`')
        (result,) = cur.fetchone()
        cur.close()
        return result

    def close(self):
        if self._connection:
            self._connection.close()
