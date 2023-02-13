import cProfile
import io
import os
import pstats
import signal
import time
from abc import ABC, abstractmethod
from pstats import SortKey

from .actions import IOOperation


class AbstractWorker(ABC):

    _operations: set = None

    def __init__(self, ops_count: int, daemon_mode=False):
        self.gen_ops(ops_count)
        self.pf: cProfile.Profile = cProfile.Profile()
        self.stopped = not daemon_mode

    def gen_ops(self, count: int = 10):
        print(f"Adding {count} new tasks...")
        self._operations = {IOOperation(i + 1) for i in range(count)}

    def start(self):
        self.startup_info()
        self.register_signal_handler()
        self.pf.enable()
        while True:
            if self._operations:
                self._process()
            else:
                print("No Operations to perform")
                time.sleep(1)

            if self.stopped:
                break

        self.pf.disable()
        self.summary_info()

    @abstractmethod
    def _process(self):
        pass

    @property
    def task_count(self):
        return len(self._operations)

    def startup_info(self):
        print("Starting Worker ...")
        print(f"Process PID is {os.getpid()}")
        print(f"Tasks in queue: {self.task_count}")
        print("=" * 10)

    def summary_info(self):
        print("=" * 10)
        buf = io.StringIO()
        sort_by = SortKey.CUMULATIVE
        ps = pstats.Stats(self.pf, stream=buf).sort_stats(sort_by)
        ps.print_stats()
        print(buf.getvalue())

    def register_signal_handler(self):
        pass

    def signal_handler_stop(self, *_, **__):
        self.stopped = True
        print("=" * 10)
        print(f"Stop processing after {self.task_count} tasks...")
        print("=" * 10)

    def signal_handler_add_tasks(self, sig, *_, **__):
        if sig == signal.SIGUSR1:
            self.gen_ops(1)
        elif sig == signal.SIGUSR2:
            self.gen_ops(10)
