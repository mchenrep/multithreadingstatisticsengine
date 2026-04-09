# Name: Matthew Chen
# FSUID: mc23c
# Due Date: 02/16/2026
# The program in this file is the individual work of Matthew Chen

# Problem Description
# Given an integer array A with size = N, compute:
# - Sum, min, max, mean, variance

# Run program as python stats_parallel.py --n size --workers amount --mode option --seed random --chunks (optional) amount

import argparse
import random
import time
import math
import threading 
import multiprocessing

def parse_args():
    '''
        Defines arguments passed from CLI (command line interface).
        Uses argparse Python library for input validation and convience.
    '''
    ap = argparse.ArgumentParser(description="Compute statistics (serial, threads_bad, threads_lock, or mp)")

    ap.add_argument(
        "--n",
        type = int,
        required = True,
        help = "Integers to generate" # info for an optional --help argument
    )

    ap.add_argument(
        "--workers",
        type = int,
        required = True,
        help = "Number of threads/processes to use" # info for an optional --help argument
    )

    ap.add_argument(
        "--mode",
        type = str,
        choices = ["serial", "threads_bad", "threads_lock", "mp"],
        required = True,
        help = "Execution mode" # info for an optional --help argument
    )

    ap.add_argument(
        "--seed",
        type = int,
        required = True,
        help = "Random seed for reproducibility" # info for an optional --help argument
    )

    ap.add_argument(
        "--chunks",
        type = int,
        required = False,
        default = None,
        help= "Optional argument to specify number of chunks to split the data into (default = n/workers)" # info for an optional --help argument
    )

    # Validate CLI arguments
    args = ap.parse_args()

    if args.n <= 0:
        ap.error("--n must be > 0")
    if args.workers <= 0:
        ap.error("--workers must be > 0")
    if args.chunks is not None and args.chunks <= 0:
        ap.error("--chunks must be > 0")

    # Return arguments if input was valid
    return args

def compute_serial(data: list) -> list:
    '''
        Serial implementation for statistics engine.
        Calculates sum, mean, min, max, and variance in a single loop.
        Equations used:
            Mean = sum / length of list
            Variance = (sum of squares - (sum^2 / n)) / n
    ''' 
    n = len(data)
    sum_data = sum(data)
    squares = sum(x**2 for x in data)
    minimum = min(data)
    maximum = max(data) 

    mean = sum_data / n
    variance = (squares - ((sum_data**2)/n)) / n
    return [sum_data, mean, minimum, maximum, variance]

def compute_threads_bad(data: list, workers: int, chunks: int) -> list:
    '''
        "Bad" implementation of multithreading to compute sum, mean, min, max, and variance.
        Uses global variables (of function scope) which get written to from every thread.
    '''
    n = len(data)
    # Split data into contiguous chunks, chunks = workers if unprovided
    chunks = chunks if chunks is not None else workers
    chunks = min(n, chunks) # ensures chunks are never > data

    chunk_size = math.ceil(n/chunks)
    data_chunks = [data[i:i+chunk_size] for i in range(0, n, chunk_size)] # split data list

    # Compute using global variables
    gs, gmin, gmax, gsquares = 0, float('inf'), float('-inf'), 0
    
    # Helper function with worker instructions
    def worker_bad(worker_number): 
        nonlocal gs, gmin, gmax, gsquares

        # Assign chunk(s) to worker
        for i in range(worker_number, len(data_chunks), workers):
            chunk = data_chunks[i]
            gs += sum(chunk)
            gmin = min(gmin, min(chunk))
            gmax = max(gmax, max(chunk))
            gsquares += sum(x**2 for x in chunk)
    
    # Spawn and terminate threads
    threads = [] # list to keep track of threads
    
    for w in range(workers):
        thread = threading.Thread(target=worker_bad, args=(w,))
        threads.append(thread)
        thread.start()
    
    for t in threads: # terminate threads
        t.join()

    # Compute and return sum, mean, min, max, and variance
    mean = gs / n
    variance = (gsquares - ((gs**2)/n)) / n
    return [gs, mean, gmin, gmax, variance]

def compute_threads_lock(data: list, workers: int, chunks: int) -> int:
    '''
        "Lock" implementation of multithreading to compute sum, mean, min, max, and variance.
        Each thread updates "global" variables through an acquired lock.
        Avoids race conditions that compute_threads_bad() introduces with proper multithreading practices.
    '''
    n = len(data)
    # Split data into contiguous chunks, chunks = workers if unprovided
    chunks = chunks if chunks is not None else workers
    chunks = min(n, chunks) # ensures chunks are never > data

    chunk_size = math.ceil(n/chunks)
    data_chunks = [data[i:i+chunk_size] for i in range(0, n, chunk_size)] # split data list

    # Helper function with worker instructions and lock for proper synchronization
    lock = threading.Lock()
    s, minimum, maximum, squares = 0, float('inf'), float('-inf'), 0
    def worker_lock(worker_number):
        nonlocal s, minimum, maximum, squares
        
        # Initialize local variables
        lsum = 0
        lmin = float('inf')
        lmax = float('-inf')
        lsq = 0

        # Assign chunk(s) to worker
        for i in range(worker_number, len(data_chunks), workers):
            chunk = data_chunks[i]
            lsum += sum(chunk)
            lmin, lmax = min(lmin, min(chunk)), max(lmax, max(chunk))
            lsq += sum(x**2 for x in chunk)
        
        # Acquire lock and update "global" variables
        with lock:
            s += lsum
            minimum = min(minimum, lmin)
            maximum = max(maximum, lmax)
            squares += lsq

    # Spawn and terminate threads
    threads = [] # list to keep track of threads
    for w in range(workers):
        thread = threading.Thread(target=worker_lock, args=(w,))
        threads.append(thread)
        thread.start()
    
    for t in threads: # terminate threads
        t.join()

    mean = s / n
    variance = (squares - ((s**2)/n)) / n
    return [s, mean, minimum, maximum, variance]

def compute_mp(data: list, workers: int, chunks: int) -> list:
    n = len(data)
    # Split data into contiguous chunks, chunks = workers if unprovided
    chunks = chunks if chunks is not None else workers
    chunks = min(n, chunks) # ensures chunks are never > data

    chunk_size = math.ceil(n/chunks)
    data_chunks = [data[i:i+chunk_size] for i in range(0, n, chunk_size)] # split data list

    # Helper function with instructions for each process
    def worker_mp(worker_number, q):
        for i in range(worker_number, len(data_chunks), workers):
            chunk = data_chunks[i]
            s = sum(chunk)
            minimum = min(chunk)
            maximum = max(chunk)
            squares = sum(x**2 for x in chunk)
            q.put([s, minimum, maximum, squares])
        
    # Spawn and track processes
    queue = multiprocessing.Queue() # queue for multiprocess communication and future computation
    processes = []
    for w in range(workers):
        process = multiprocessing.Process(target=worker_mp, args=(w, queue))
        process.start()
        processes.append(process)
    
    # End processes
    for p in processes:
        p.join()

    # Get results from processes and compute statistics
    s, minimum, maximum, squares = 0, float('inf'), float('-inf'), 0
    total_chunks = sum(1 for w in range(workers) for i in range(w, len(data_chunks), workers)) # get number of chunks processed
    for _ in range(total_chunks):
        qs, qmin, qmax, qsq = queue.get()
        s+=qs
        minimum = min(minimum, qmin)
        maximum = max(maximum, qmax)
        squares += qsq
    
    # Close queue
    queue.close()
    queue.join_thread()

    mean = s / n
    variance = (squares - ((s**2)/n)) / n
    return [s, mean, minimum, maximum, variance]

def main(args):
    # Get all CLI argument values
    n, workers, mode, seed, chunks = args.n, args.workers, args.mode, args.seed, args.chunks if args.chunks else args.workers
    
    # Seed and generate data
    random.seed(seed)
    data = [random.randint(0, 100) for _ in range(n)] # generate a list of n random integers using list comprehension, range is from 0 to largest possible integer on a 64 bit platform

    # Serial implementation
    if mode == "serial":
        start = time.time()
        sum, mean, minimum, maximum, variance = compute_serial(data)
        end = time.time()
        
    # Bad thread implementation (threads_bad)
    if mode == "threads_bad":
        start = time.time()
        sum, mean, minimum, maximum, variance = compute_threads_bad(data, workers, chunks)
        end = time.time()

    # Thread implementation (threads_lock)
    if mode == "threads_lock":
        start = time.time()
        sum, mean, minimum, maximum, variance = compute_threads_lock(data, workers, chunks)
        end = time.time()

    # Multiprocess implementation
    if mode == "mp":
        start = time.time()
        sum, mean, minimum, maximum, variance = compute_mp(data, workers, chunks)
        end = time.time()

    check = (sum + minimum + maximum) % 1000000011
    print(f"MODE {mode}")
    print(f"N {n} WORKERS {workers} CHUNKS {chunks}")
    print(f"SUM {sum}\nMIN {minimum} MAX {maximum}\nMEAN {mean}\nVAR {variance}")
    print(f"TIME {(end - start)}")
    print(f"CHECK {check}")

if __name__ == "__main__":
    args = parse_args()
    main(args)