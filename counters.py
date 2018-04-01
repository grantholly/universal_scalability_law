#!/usr/bin/env python3
import multiprocessing as mp

class Counter:
    def __init__(self, work):
        self.n = 0
        self.work = work

    def incr(self, upto):
        for i in range(upto):
            self.n += 1

    def do_work(self):
        for job in self.work:
            self.incr(job)

class StupidLockingCounter(Counter):
    def __init__(self, work):
        self._lock = mp.Lock()
        super().__init__(work)
            
    def do_work(self):
        for job in self.work:
            self._lock.acquire()
            self.incr(job)
            self._lock.release()

class UnsharedConcurrentCounter(Counter):
    def __init__(self, work):
        super().__init__(work)

    def do_work(self, f):
        self.workers = mp.Pool(processes=len(self.work))
        self.workers.map(f, self.work)

class SharedConcurrentCounter(Counter):
    def __init__(self, work, worker_count):
        self._work_queue = mp.Queue()
        self.worker_count = worker_count
        super().__init__(work)
        for job in self.work:
            self._work_queue.put(job)
        self._workers = [
            mp.Process(target=self.incr,
                       args=(self._work_queue,)) for n in range(worker_count)
        ]

    def incr(self, q):
        n = 0
        if not q.empty():
            while not q.empty():
                job = q.get()
                for i in range(job):
                    n += 1

    def do_work(self):
        tuple(map(lambda x: x.start(), self._workers))

def incr(upto):
    n = 0
    for i in range(upto):
        n += 1
    return n
        

