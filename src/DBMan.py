import psycopg2

class DBMan():
    """
        Database Manager
    """
    def __init__(self, db_info):
        self.dbanme = db_info["dbname"]
        self.user = db_info["user"]
        self.password = db_info["password"]
        self.host = db_info["host"]
        self.port = db_info["port"]
        self.db_info = db_info

    def set_storeinfo(self, result):
        pass

    def set_experimentinfo(self, config):
        pass

    def create_table(self, config):
        sql = """
        """
        self._execute(sql)

    def record(self):
        sql = """
        """
        self._execute(sql)

    def _execute(self, sql):
        with psycopg2.connect(dbname=self.dbanme,
                              user=self.user,
                              password=self.password,
                              host=self.host,
                              port=self.port) as conn:
            curosr = conn.cursor()
            curosr .execut(sql)
            curosr.commit()
