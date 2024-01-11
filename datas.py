import os
import time
import scraper
import loadCurrent
import database_func
import matplotlib.pyplot as plt

filepath=".\\tmp\\current.csv"

def checktime():
    if os.path.exists(filepath):
        t=os.path.getmtime(filepath)
        t=time.time()-t
        if t<3600:
            return True
        else:
            return False
    else:
        return False

def getcurrentdata(city,site):
    #if(0):
    if(not checktime()):
        result = scraper.spider()
        if result != True:
            print(result)
            return False
        else:
            loadCurrent.updateCurrent()
    print(city)
    print(site)
    tmp = database_func.get_current_data(city,site)
    #database_func.get_history_data(city,site)
    return tmp