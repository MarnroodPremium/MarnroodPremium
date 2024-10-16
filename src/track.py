from time import time
from os import getpid
from psutil import Process
from colorama import Fore


def get_process_memory():
    process = Process(getpid())
    return process.memory_info().rss


def track(func):
    def wrapper(*args, **kwargs):
        mem_before = get_process_memory()
        start = time()
        result = func(*args, **kwargs)
        mem_after = get_process_memory()
        elapsed_time = time() - start
        mem_used = mem_after - mem_before
        print(f"{Fore.YELLOW}{func.__name__} statistics")
        print(f"memory before: {mem_before:,} bytes")
        print(f"memory after: {mem_after:,} bytes")
        print(f"memory consumed: {mem_used:,} bytes")
        print(f"execution time: {elapsed_time} seconds{Fore.RESET}")
        return result

    return wrapper
