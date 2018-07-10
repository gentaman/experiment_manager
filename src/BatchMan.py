import os
import pickle as pk

class BatchMan():
    """
        Batch Manager
    """
    def __init__(self, dbman, storageman=None, main_algorithm=None):
        self.dbman = dbman
        self.storageman = dbman
        self.main_algorithm = main_algorithm
        self._first_process = True

    def setup(self):
        pass

    def do_experiment(self, main_algorithm, plan):
        pass

    def do_each_experiment(self, plan, main_algorithm=None, table_name='tmp'):
        if main_algorithm is not None:
            main_algorithm(**plan)
        else:
            self.main_algorithm(**plan)
        result = self.get_result(plan)
        if self._first_process:
            self.dbman.table_name = table_name
            self.dbman.create_table(plan, result)
            self._first_process = False

        self.store_result(result)
        self.dbman.set_experimentinfo(plan)
        self.dbman.record()

    def get_result(self, plan):
        path = plan["path"]
        fname= plan["experimetinfo_file"]
        with open(os.path.join(path, fname), mode='rb') as f:
            res = pk.load(f)
        return res

    def store_result(self, result):
        if self.storageman is None:
            self.dbman.set_storeinfo(result)
        else:
            # TODO:
            self.storageman.store_result(result)


    def record(self, plan):
        pass
