from abc import ABC, abstractclassmethod
import time
import threading
import multiprocessing
import asyncio


class Server(ABC):
    def __init__(self) -> None:
        super(ABC).__init__()

    @abstractclassmethod
    def run(cls, list_of_query: list):
        pass

    def processing(self, q: dict):
        print("  ", q['type'])
        time.sleep(q['time'])


"""------------------------------------"""


class ThreadServer(Server):
    def __init__(self) -> None:
        super().__init__()
        self.load = 0
        self.load_cond = threading.Condition()

    def processing(self, q: dict):

        # if self.load + q['cpu_load'] > 100:
        #     # print('T: overloaded \n')
        #     with self.load_cond:
        #         self.load_cond.wait()

        self.load += q['cpu_load']
        time.sleep(q['time'])
        self.load -= q['cpu_load']
        with self.load_cond:
            self.load_cond.notify()

    def run(self, list_of_query: list):
        thread_list = []
        for q in list_of_query:
            thread = threading.Thread(
                target=self.processing, args=(q,), daemon=False)
            thread_list.append(thread)
            thread.start()

        for thread in thread_list:
            thread.join()


"""------------------------------------"""


class ProcessServer(Server):
    def __init__(self) -> None:
        super().__init__()
        self.load = 0
        self.load_cond = multiprocessing.Condition()

    def processing(self, q: dict):
        # if self.load + q['cpu_load'] > 100:
        #     print('P: overloaded \n')
        #     with self.load_cond:
        #         self.load_cond.wait()

        self.load += q['cpu_load']
        time.sleep(q['time'])
        self.load -= q['cpu_load']
        with self.load_cond:
            self.load_cond.notify()

    def run(self, list_of_query: list):
        p_list = []
        for q in list_of_query:
            p = multiprocessing.Process(
                target=self.processing, args=(q,), daemon=False)
            p_list.append(p)
            p.start()

        for p in p_list:
            p.join()


