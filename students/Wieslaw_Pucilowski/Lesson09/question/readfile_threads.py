import threading
import queue
import sys


q = queue.Queue()
threads = []

def read_buff_threads(fh):
        lines = fh.readlines(buffer)
        for i in lines:
            if 'his' in i:
                q.put(i)

def count_word(word, lines):
    word = word.lower()
    global count
    for line in lines:
        if word in line.lower():
            count += 1
    # return count

            
if __name__ == "__main__":

    count = 0
    buffer = 1024
    q = queue.Queue()
    threads = []
    word = 'his'

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
                t = threading.Thread(target=count_word, args=(word, chunk))
                t.start()
                threads.append(t)
                chunk = fh.readlines(buffer)
                
                for t in threads:
                    t.join()
        
    
    print('All threads/requests finished, time to parse titles in the queue\n')
    print(word, "found {} times".format(count))