import random
import time


def random_sleep(min=1, max=3):
    delta = max-min
    sleep_time = min + random.betavariate(2, 5) * delta
    random.betavariate(2, 5)
    time.sleep(sleep_time)


def is_int(str):
    try:
        int(str)
        return True
    except ValueError:
        return False
