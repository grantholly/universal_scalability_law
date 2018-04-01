#!/usr/bin/env python3
import random
import datetime
import time
import os

from counters import (Counter, 
                      UnsharedConcurrentCounter,
                      incr,
                      SharedConcurrentCounter)


OUTPUT_DIR = os.path.dirname(__file__) + "/output/"
TIME_FMT = "%Y-%m-%d-%H,%M,%S"

def time_it(f):
    start = time.time()
    f()
    end = time.time()
    print(end - start)

def simple_counter_trial(trials, workload):
    with open(OUTPUT_DIR + 
              "non_concurrency" +
              date_stamp, "a") as f:
        for trial in trials:
            # do each trial
            pass
            
def unshared_counter_trial(trials, workload):
    with open(OUTPUT_DIR + 
              "unshared_concurrency" +
              date_stamp, "a") as f:
        pass

def shared_concurrent_counter_trial(trials, concurrency, workload):
    with open(OUTPUT_DIR + "shared_concurrency", "a") as f:
        pass

def counter_trial(counter_type, trials, workload, 
                  file_name, concurrency=0, **kwargs):
    date_stamp = datetime.datetime.now().strftime(TIME_FMT)
    results = []
    with open(OUTPUT_DIR +
              file_name +
              date_stamp, "a") as f:
        for trial in range(trials):
            # make a counter instance
            if concurrency != 0:
                c = counter_type(workload, concurrency)
            else:
                c = counter_type(workload)
            # do each trial
            if kwargs:
                start = time.time()
                c.do_work(kwargs["func"])
            else:
                start = time.time()
                c.do_work()
            end = time.time()
            duration = end - start
            results.append(duration)
            f.write(str(duration) + "\n")
            # need to get the average from the results still
        
            
def main():
    size = 20
    work = [random.randint(0,1000000) for n in range(size)]
    trials = 10

    counter_trial(Counter, trials, work, "plain_counter")
    counter_trial(UnsharedConcurrentCounter, trials, work, 
                  "mapped_counter", func=incr)
    counter_trial(SharedConcurrentCounter, trials, work,
                  "shared_counter", concurrency=2)
"""
    sc = Counter(work)
    time_it(sc.do_work)

    ucc = UnsharedConcurrentCounter(work)
    start = time.time()
    ucc.do_work(incr)
    end = time.time()
    print(end - start)

    scc = SharedConcurrentCounter(work, 4)
    time_it(scc.do_work)
"""


main()
