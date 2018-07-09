import os

class BatchMan():
    """
        Batch Manager
    """
    def __init__(self, dbman, storageman=None, main_algorithm=None):
        self.dbman = dbman
        self.storageman = dbman
        self.main_algorithm = main_algorithm

    def setup(self):
        pass

    def do_experiment(self, main_algorithm, config):
        pass

    def do_each_experiment(self, config, main_algorithm=None):
        if main_algorithm is not None:
            main_algorithm(**config)
        else:
            self.main_algorithm(**config)
        result = self.get_result(config)
        self.store_result(result)
        self.dbman.set_experimentinfo(config)
        self.dbman.record()

    def get_result(self, config):
        path = config["path"]
        fname= config["experimetinfo_file"]
        with open(os.path.join(path, fname)) as f:
            res = f.read()
        return res

    def store_result(self, result):
        if self.storageman is None:
            self.dbman.set_storeinfo(result)
        else:
            # TODO:
            self.storageman.store_result(result)


    def record(self, config):
        pass
