import json
import os
from datetime import datetime

class ExpMan():
    """
        Experiment Manager
    """
    def __init__(self, main_algorithm, plan, dir_name='exp',log_path=None, batchman=None, **kwargs):
        self.main_algorithm = main_algorithm
        self.plan = plan
        self.dir_name = dir_name + '_'+str(datetime.now().strftime("%Y%m%d-%H:%M"))
        if not os.path.exists(self.dir_name):
            os.mkdir(self.dir_name)

        if log_path is None:
            log_path = os.path.join(self.dir_name, './auto.log')
        with open(log_path, 'w') as f:
            pass
        self.log_path = log_path
        self.kwargs = kwargs
        self._done = False
        self.batchman = batchman

    def planning(self):
        if isinstance(self.plan, str):
            if self.plan.find('.json') != -1:
                with open(self.plan, 'r') as f:
                    raw_data = json.load(f)
                tmps = []
                for i, d in enumerate(raw_data['configures']):
                    path = os.path.join(self.dir_name, 'plan{}'.format(i))
                    tmps.append({'configure':d, 'path':path})
                self.plan = tmps

    def run(self):
        if not self._done:
            self.planning()
            if not os.path.exists(self.dir_name):
                os.mkdir(self.dir_name)

            for config in self.plan:
                log = '"start time":{}\n"configures":{}\n'.format(datetime.now(), config)
                self.logging(log)
                if self.batchman is None:
                    self.main_algorithm(**config)
                else:
                    config["bacthman"] = True
                    config["experimetinfo_file"] = 'expinfo.csv'
                    self.batchman.do_each_experiment(self.main_algorithm, **config)

                self.logging('"end  time":{}\n'.format(datetime.now()))

        self._done = True

    def logging(self, log):
        with open(self.log_path, mode='a') as f:
            f.write(log)


    def _check_interrupt(self, ch):
        if ch == 'C':
            return True
        else:
            return False

    def _check_skip(self, ch):
        if ch == 'Q':
            return True
        else:
            return False

    def check_key(self):
        # TODO
        # key detect
