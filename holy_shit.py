#!/usr/bin/env python3
import random
import time
import math
import sys
import multiprocessing as mp

work = list(range(100000, 200000))
random.shuffle(work)
concurrency = int(sys.argv[1])

def chunk(l, pieces):
    return [l[i:i+pieces] for i in range(0, len(l), pieces)]

def is_factor(factor_me, maybe_factor):
    result = None
    div = (factor_me // maybe_factor)
    if div * maybe_factor == factor_me:
        result = (maybe_factor, div)
    return result

def f(q, deadline, out):
    ops = 0
    while not q.empty() and time.time() < deadline:
        n = q.get()
        check_these = range(1, int(math.floor(math.sqrt(n))) + 1)
        factors = [is_factor(n, pf) for pf in check_these]
        done = [f for f in factors if f != None]
        ops += 1
    out.put(ops)
    
output_queue = mp.Queue()

work_queues = [
    mp.Queue() for n in range(concurrency)
]

# divide work up
work_chunks = chunk(work, len(work) // concurrency)

# loda work into the work_queues
for q in list(zip(work_queues, work_chunks)):
    # put the numbers into the queue
    for num in q[-1]:
        q[0].put(num)

end = time.time() + 1

workers = [
    mp.Process(target=f, args=(work_queues[i], end, output_queue,)) 
    for i in range(concurrency)
]

tuple(map(lambda x: x.start(), workers))
tuple(map(lambda x: x.join(), workers))

total = 0
while not output_queue.empty():
    total += output_queue.get()

print(str(concurrency) + "," + str(total))
