import os
import psutil
from typing import Callable
import gc


def printMemory():
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    print(f"RSS (Resident Set Size): {memory_info.rss / (1024**2):.2f} MB")
    print(f"VMS (Virtual Memory Size): {memory_info.vms / (1024**2):.2f} MB")


def gc_collect(func: Callable):
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        gc.collect()
        return res

    return wrapper
