import multiprocessing as mp

__AVAILIBLE_CPU__ = mp.cpu_count() - 2
if __AVAILIBLE_CPU__ < 1:
    __AVAILIBLE_CPU__ = 1

