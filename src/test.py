from ExpMan import ExpMan
from BatchMan import BatchMan
from DBMan import DBMan
#from StorageMan import StorageMan

from getpass import getpass
import json
import pickle as pk
import time
import os

etas = []
alphas = []
betas = []
for i in [1]:
    etas.append(i)
for i in [0, 1]:
    alphas.append(i)
    betas.append(i)
hyperparam = []
for e in etas:
    for a in alphas:
        for b in betas:
            hyperparam.append({
                    'eta':e,
                    'alpha':a,
                    'beta':b
                })
lrs = [i for i in [1e-3,1e-2]]
n_epochs = [i for i in [50]]
batch_size=[100]
configures = []
for h in hyperparam:
    for lr in lrs:
        for e in n_epochs:
            configures.append({
                    'model':"A",
                    'hyperparam':h,
                    'lr':lr,
                    'n_epoch':e,
                    'n_hidden':100,
                    'batch_size':100
                })

with open('test.json', 'w') as f:
    json.dump({"configures":configures}, f)

def test_loop(configure, path, experimetinfo_file):
    s = time.time()
    for i in range(1000):
        pass
    e = time.time()
    result = {}
    result['acc'] = 1
    result['loss'] = -1
    result['processed_time'] = "{}".format(round(e-s))
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path+'/'+experimetinfo_file, 'wb') as f:
        pk.dump(result, f)


if __name__ == '__main__':
    print('input user name')
    user=input()
    print('input password')
    pwd = getpass()
    print('input port num')
    port=input()
    db_info = {
        "dbname":"testdb",
        "user":user,
        "password":pwd,
        "host":"localhost",
        "port":port
    }
    dbman = DBMan(db_info)
    batchman = BatchMan(dbman)
    expman = ExpMan(main_algorithm=test_loop, plan="test.json", batchman=batchman)
    expman.planning()
    expman.run()
