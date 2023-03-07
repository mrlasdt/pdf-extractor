import time
from typing import Callable


class Timer:
    def __init__(self, name: str) -> None:
        self.name = name

    def __enter__(self):
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, func: Callable, *args):
        self.end_time = time.perf_counter()
        self.elapsed_time = self.end_time - self.start_time
        print(f"[INFO]: {self.name} took : {self.elapsed_time:.6f} seconds")


if __name__ == "__main__":
    # example usage
    with Timer():
        print("test timer")
