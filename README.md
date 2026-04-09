<<<<<<< HEAD
# Run Time Comparisons

## Serial (Baseline)
mchen@linprog5.cs.fsu.edu:~/COP4521/Assignment2>python3 stats_parallel.py --n 6000000 --workers 10 --mode serial --seed 123
MODE serial
N 6000000 WORKERS 10 CHUNKS 10
SUM 299906972
MIN 0 MAX 100
MEAN 49.984495333333335
VAR 849.725158938645
**TIME 0.7822072505950928**
CHECK 299907072

## MP (Multiprocessing)
### 4 workers
mchen@linprog5.cs.fsu.edu:~/COP4521/Assignment2>python3 stats_parallel.py --n 6000000 --workers 4 --mode mp --seed 123
MODE mp
N 6000000 WORKERS 4 CHUNKS 4
SUM 299906972
MIN 0 MAX 100
MEAN 49.984495333333335
VAR 849.725158938645
**TIME 0.3251926898956299**
CHECK 299907072

### 8 workers
mchen@linprog5.cs.fsu.edu:~/COP4521/Assignment2>python3 stats_parallel.py --n 6000000 --workers 8 --mode mp --seed 123
MODE mp
N 6000000 WORKERS 8 CHUNKS 8
SUM 299906972
MIN 0 MAX 100
MEAN 49.984495333333335
VAR 849.725158938645
**TIME 0.22687411308288574**
CHECK 299907072

### 16 workers
mchen@linprog5.cs.fsu.edu:~/COP4521/Assignment2>python3 stats_parallel.py --n 6000000 --workers 16 --mode mp --seed 123
MODE mp
N 6000000 WORKERS 16 CHUNKS 16
SUM 299906972
MIN 0 MAX 100
MEAN 49.984495333333335
VAR 849.725158938645
**TIME 0.1909496784210205**
CHECK 299907072

### 32 workers
mchen@linprog5.cs.fsu.edu:~/COP4521/Assignment2>python3 stats_parallel.py --n 6000000 --workers 32 --mode mp --seed 123
MODE mp
N 6000000 WORKERS 32 CHUNKS 32
SUM 299906972
MIN 0 MAX 100
MEAN 49.984495333333335
VAR 849.725158938645
**TIME 0.20189595222473145**
CHECK 299907072

## Threads_Lock (Multithreading with Synchronization via Locks)
### 4 workers
mchen@linprog5.cs.fsu.edu:~/COP4521/Assignment2>python3 stats_parallel.py --n 6000000 --workers 4 --mode threads_lock --seed 123
MODE threads_lock
N 6000000 WORKERS 4 CHUNKS 4
SUM 299906972
MIN 0 MAX 100
MEAN 49.984495333333335
VAR 849.725158938645
**TIME 1.4678082466125488**
CHECK 299907072

### 8 workers
mchen@linprog5.cs.fsu.edu:~/COP4521/Assignment2>python3 stats_parallel.py --n 6000000 --workers 8 --mode threads_lock --seed 123
MODE threads_lock
N 6000000 WORKERS 8 CHUNKS 8
SUM 299906972
MIN 0 MAX 100
MEAN 49.984495333333335
VAR 849.725158938645
**TIME 1.4425866603851318**
CHECK 299907072

### 16 workers
mchen@linprog5.cs.fsu.edu:~/COP4521/Assignment2>python3 stats_parallel.py --n 6000000 --workers 16 --mode threads_lock --seed 123
MODE threads_lock
N 6000000 WORKERS 16 CHUNKS 16
SUM 299906972
MIN 0 MAX 100
MEAN 49.984495333333335
VAR 849.725158938645
**TIME 1.4479973316192627**
CHECK 299907072

### 32 workers
mchen@linprog5.cs.fsu.edu:~/COP4521/Assignment2>python3 stats_parallel.py --n 6000000 --workers 32 --mode threads_lock --seed 123
MODE threads_lock
N 6000000 WORKERS 32 CHUNKS 32
SUM 299906972
MIN 0 MAX 100
MEAN 49.984495333333335
VAR 849.725158938645
**TIME 1.2236182689666748**
CHECK 299907072

# Performance Evaluation

## MP speedup relative to Serial (Baseline)
### 4 workers
Time = .325 seconds
Speedup = 2.41x

### 8 workers
Time = .227 seconds
Speedup = 3.45x

### 16 workers
Time = .191 seconds
Speedup = 4.10x

### 32 workers
Time = .202 seconds
Speedup = 3.87x

## Threads_Lock speedup relative to Serial (Baseline)
### 4 workers
Time = 1.468 seconds
Speedup = 0.53x

### 8 workers
Time = 1.443 seconds
Speedup = 0.54x

### 16 workers
Time = 1.448 seconds
Speedup = 0.54x

### 32 workers
Time = 1.224 seconds
Speedup = 0.64x

# Conclusion

Given the results of the runtime between serial, multiprocessing, and multithreading with synchronization, we can conclude the following. 
1. In Python, multiprocessing runs faster than multithreading due to GIL (global interpreter lock) which prevents true parallelism in multithreading, while multiprocessing bypasses Python GIL by creating seperate processes (which have their own seperate memory). 
2. We can also see that speedup is not always linear relatie to worker count, as seen in the multiprocessing runtimes, where the jump from 16 to 32 workers actually decreased the speedup by .23x. We can attribute that to the overhead costs of creating seperate processes, communicating through message queues, and context switching. 
3. Threads with proper synchronization is slower than serial, this is due to GIL as seen above and the lock mechanism for synchronization which requires threads to wait to access global variables.
Overall, we can conclude that the best performance out of all the program runs was MP (multiprocessing) with 16 workers, which had a 4.10x speedup over serial. This demonstrates that multiprocessing is the prefrred method for CPU-bound parallel computing in Python given what we have learned so far.
=======
# multithreadingstatisticsengine
>>>>>>> 98f5ad1fa1260a5bf4c5cf35501d9bcd30d9bc2c
