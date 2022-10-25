from threading import Thread
from typing import Callable


def spawn(func: Callable, *args) -> Thread:
    thread = Thread(target=func, args=args, daemon=True)
    thread.start()
    return thread
