import psycopg2 as ps

import numpy as np
def _convert2type_of_sql(values):
    converted_types = []
    for v in values:
        if isinstance(v, np.int32):
            converted_types.append('integer')
        elif isinstance(v, np.int64):
            converted_types.append('bigint')
        elif isinstance(v, np.float32):
            converted_types.append('real')
        elif isinstance(v, np.float64):
            converted_types.append('double precision')
        elif isinstance(v, str):
            converted_types.append('text')
        elif isinstance(v, int):
            converted_types.append('integer')
        elif isinstance(v, float):
            converted_types.append('real')
        else:
            raise TypeError("undefined type:{}, value:{}".format(type(v), v))

    return converted_types

def _flatten_dict(d, name=''):
    assert isinstance(d, dict)
    tmp = {}
    for k in d:
        if isinstance(d[k], dict):
            tmp.update(_flatten_dict(d[k], name+'_'+k+'_'))
        else:
            tmp[name+k] = d[k]
    return tmp

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
        self.experiment_schema_name = "experiment"
        self.connect()

    def set_storeinfo(self, result):
        assert isinstance(result, dict)
        result = _flatten_dict(result)
        self.record_info["storage"] = result.values()

    def set_experimentinfo(self, configure, path):
        assert isinstance(configure, dict)
        configure = _flatten_dict(configure)
        self.record_info["experiment"] = list(configure.values())
        self.record_info["experiment"] += [path]

    def _parser_plan(self, plan):
        assert isinstance(plan, dict)
        plan = _flatten_dict(plan)
        column = list(plan)
        types = _convert2type_of_sql(plan.values())
        return column, types

    def _parser_result(self, result):
        # TODO:
        column = result
        types = result
        return columns, types

    def create_table(self, plan, result):
        configure, c_types = self._parser_plan(plan["configure"])
        path = ["path"]
        p_types = ["text"]
        # TODO:
        result, r_types = self._parser_plan(result)
        columns = configure + path + result
        types = c_types + p_types + r_types
        columns_types = [" ".join([x, y]) for x, y in zip(columns, types)]
        columns_types = ",\n".join(columns_types)
        sql = """
            CREATE TABLE {schema}.{table_name}(
                {columns_types}
            )
        """.format(schema=self.experiment_schema_name,
                   table_name=self.table_name,
                   columns_types=columns_types)
        self._execute(sql)

    def record(self):
        value = list(self.record_info["experiment"]) + list(self.record_info["storage"])
        sql = """
            INSERT INTO {schema}.{table_name}
            VALUES {value}
        """.format(schema=self.experiment_schema_name,
                   table_name=self.table_name,
                   value=tuple(value))
        self._execute(sql)

    def _execute(self, sql):
        with ps.connect(dbname=self.dbanme,
                        user=self.user,
                        password=self.password,
                        host=self.host,
                        port=self.port) as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()

    def connect(self):
        with ps.connect(dbname=self.dbanme,
                        user=self.user,
                        password=self.password,
                        host=self.host,
                        port=self.port) as conn:
            pass
        print('connection succeed')
