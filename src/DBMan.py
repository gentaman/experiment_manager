import psycopg2 as ps

import numpy as np
def _convert2type_of_sql(values):
    converted_types = []
    for t in values:
        if isinstance(t, np.int32):
            converted_types.append('ineger')
        elif isinstance(t, np.int64):
            converted_types.append('bigint')
        elif isinstance(t, np.float32):
            converted_types.append('real')
        elif isinstance(t, np.float64):
            converted_types.append('double precision')
        elif isinstance(t, str):
            converted_types.append('text')
    return converted_types

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
        self.record_info = {}
        self.table_name = None

    def set_storeinfo(self, result):
        assert isinstance(result, dict)
        self.record_info["storage"] = result.values()

    def set_experimentinfo(self, plan):
        assert isinstance(plan, dict)
        self.record_info["experiment"] = plan.values()

    def _parser_plan(self, plan):
        assert isinstance(plan, dict)
        def _flatten_dict(d, name=''):
            assert isinstance(d, dict)
            tmp = {}
            for k in d:
                if isinstance(d[k], dict):
                    tmp.update(_flatten_dict(d[k], k+'_'))
                else:
                    tmp[name+k] = d[k]
            return tmp
        plan = _flatten_dict(plan)
        column = list(plan)
        #types = list(map(type, plan.values()))
        types = _convert2type_of_sql(plan.values())
        return column, types

    def _parser_result(self, result):]
        # TODO:
        column = result
        types = result
        return columns, types

    def create_table(self, plan, result):
        plan, p_types = self._parser_plan(plan)
        # TODO:
        result, r_types = self._parser_plan(result)
        columns = plan + result
        types = p_types + r_types
        columns_types = [" ".join(c, d) for c, d in zip(columns, types)]
        columns_types = ",\n".join(columns_types)
        sql = """
            CREATE TABLE {table_name}(
                {columns_types}
            )
        """.format(table_name=self.table_name, columns_types=columns_types)
        self._execute(sql)

    def record(self):
        value = self.record_info["experiment"] + self.record_info["storage"]
        sql = """
            INSERT INTO {table_name}
            VALUES {value}
        """.format(table_name=self.table_name, value=tuple(value))
        self._execute(sql)

    def _execute(self, sql):
        with ps.connect(dbname=self.dbanme,
                        user=self.user,
                        password=self.password,
                        host=self.host,
                        port=self.port) as conn:
            curosr = conn.cursor()
            curosr .execut(sql)
            curosr.commit()
