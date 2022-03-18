from os import walk, remove
from os.path import dirname, join
from shutil import copy
from time import time
from subprocess import call
from threading import Thread

def getAllStars():
    allStars = []
    for root, dirs, files in walk('.'):
        for f in files:
            if f.lower().endswith('.dat'):
                allStars.append(join(root, f))
                copy(join(bisDir, 'template', 'template_uint16.dat.xfs'), join(root, f+'.xfs'))
            elif f.lower().endswith('.spe'):
                allStars.append(join(root, f))
                copy(join(bisDir, 'template', 'template.SPE.xfs'), join(root, f+'.xfs'))
    return allStars

def calculate(sPath, n):
    s = time()
    bispectr = r'd:\PROGRAMS\SpeckleEx\bispectr64.exe'
    call([bispectr, sPath])
    print(n, sPath, '{:.2f}m'.format((time() - s)/60))

if __name__ == "__main__":
    start = time()
    bispectr = r'd:\PROGRAMS\SpeckleEx\bispectr64.exe'
    bisDir = dirname(bispectr)
    allStars = getAllStars()
    n = 10
    allThreads = []
    a = 1
    while True:
        if len(allStars) and len(allThreads) < n:
            obj = allStars.pop()
            allThreads.append(Thread(target=calculate, args=(obj,a), daemon=True))
            allThreads[-1].start()
            a+=1
        else:
            live_threads = 0
            for t in allThreads:
                if t.isAlive():
                    live_threads += 1
                elif len(allStars):
                    obj = allStars.pop()
                    t = Thread(target=calculate, args=(obj,a), daemon=True)
                    t.start()
                    a+=1
            if live_threads == 0 and len(allStars) == 0: break

    print(time()-start, 'sec')
    print((time()-start)/60, 'min')
    print((time()-start)/3600, 'hour')
    

