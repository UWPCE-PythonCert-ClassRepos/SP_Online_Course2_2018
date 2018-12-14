from multiprocessing import Process, Lock
import queue
import sys


q = queue.Queue()

def count_word(l, word, lines):
    l.acquire()
    word = word.lower()
    global count
    for line in lines:
        # print(line)
        if word in line.lower():
            count += 1
        print("count %s" % count)
    l.release()
    return count

            
if __name__ == "__main__":

    count = 0
    buffer = 2048
    q = queue.Queue()
    processes = []
    word = 'his'
    
    lock = Lock()

    if len(sys.argv) != 2:
        print(
            """tail script execution:
            python3 {} <file>
            """.format(sys.argv[0])  
        )
        sys.exit(1)
    else:
        with open(sys.argv[1], 'r') as fh:
            chunk = fh.readlines(buffer)
            while chunk:
                p = Process(target=count_word, args=(lock, word, chunk))
                p.start()
                processes.append(p)
                chunk = fh.readlines(buffer)
                
    print(processes)     
    for p in processes:
                    p.join()
                    
    print(processes)
    print('All processes finished, time to parse titles in the queue\n')
    print(word, "found {} times".format(count)) # <--- Why count not increamented here?