from config import *
import requests
import datetime
import time

workers=[]
start=time.time()

def id_list(worker_dict):
    out=[worker['marketId'] for worker in worker_dict]
    return sorted(out)


while True:
    print(str(datetime.datetime.utcnow()) + ': downloading latest workers')
    tw=requests.get(WORKERS_URL).json()
    if id_list(tw)!=workers:
        mins=(time.time()-start)/60
        print("workers updated, time since last update %.1f minutes" %mins)
        print(len(workers),len(tw))
        workers=id_list(tw)
        start=time.time()
    else:
        print('workers unchanged')
    #time.sleep(10)