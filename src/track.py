from time import time
from os import getpid
from psutil import Process


def get_process_memory():
    process = Process(getpid())
    return process.memory_info().rss


def track(func):
    def wrapper(*args, **kwargs):
        mem_before = get_process_memory()
        start = time.time()
        result = func(*args, **kwargs)
        mem_after = get_process_memory()
        elapsed_time = time.time() - start
        memory_used = mem_after - mem_before
        print(f"{func.__name__} statistics")
        print(f"memory consumed: {memory_used:,} bytes")
        print(f"execution time: {elapsed_time} seconds")
        return result
    return wrapper
