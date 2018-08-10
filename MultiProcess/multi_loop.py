from multiprocessing import Pool, Process, Lock
import time

def f0(i, n, m):
    #i = inp[0]
    #n = inp[1]
    #print('hello world0', i)
    #j += i
    time.sleep(0.02)
    #return i*i

def wrapper_f0(args):
    return f0(*args) 

def f(l, i, j):
    l.acquire()
    #print('hello world', i)
    j = 0
    l.release()

if __name__ == '__main__':
    N = 100
    j = 0
    
    a = []
    start_time = time.time()
    for num in range(N):
        a.append(f0(num , 1, 1))
    elapsed_time=time.time() - start_time
    print 'Elapsed time: ' + str(elapsed_time)
    
    p = Pool(10)
    start_time = time.time()
    p.map(wrapper_f0,[[i,1,1] for i in range(N)])
    elapsed_time=time.time() - start_time
    print 'Elapsed time: ' + str(elapsed_time)
      
    
