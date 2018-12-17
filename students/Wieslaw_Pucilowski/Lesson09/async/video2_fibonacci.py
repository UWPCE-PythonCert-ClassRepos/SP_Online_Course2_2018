from types import coroutine
import time

@coroutine
def sleep(secs=0):
    start = time.time()
    while time.time() - start < secs:
        # now we need it to yield control
        yield "yielding in sleep diff: %s < secs: %s" % (time.time() - start, secs)
    return "{} seconds have passed".format(time.time() - start)

"""
Now we'll create a little coroutine that calculates something,
"""
async def fib(n):
    """
    Classic fibbonacci number, but with a delay
    """
    if n == 0:
        return 0
    a, b = 0, 1
    for i in range(n-1):
        a, b = b, a + b
    await sleep(0.001) # - is calling awake on sleep before it actually returns the answer,
    return b

class TaskLoop():

    def __init__(self):
        # lsit to hold the tasks
        self.tasks = []

    def add_task(self, task):
        """
        add a task to the loop task must be a coroutine
        """
        self.tasks.append(task)

    def run_all(self):
        """
        This is where the task loop runs
        """
        results = []
        # Keep a loop going until all the tasks are gone:
        i = 0
        while self.tasks:
            i += 1
            time.sleep(0.0)
            print(f"\nOuter loop count: {i}")
            # pop a task off the end
            task = self.tasks.pop()
            # run that task:
            try:
                res = task.send(None)  # TaskLoop.run_all() - do_a_few_things() - count() - yield
                print("returned from send:", res)
                self.tasks.insert(0, task)          # move task to the begining of the list
            except StopIteration as si:             # task completed yield return StopIteration exception
                results.append(si.args[0])
                print("task: {} result >>> {}".format(task, si.args[0]))
        return results

if __name__ == '__main__':
    print("\n\n*** Running the fibonacci loop class\n")

    loop = TaskLoop()
    loop.add_task(fib(3))
    loop.add_task(fib(5))
    loop.add_task(fib(7))

    loop.add_task(fib(10))
    loop.add_task(fib(4))
    loop.add_task(fib(6))
    loop.add_task(fib(9))
    loop.add_task(fib(10))

    start = time.time()
    results = loop.run_all()
    print(f"total run time for {len(results)} tasks : {time.time() - start} seconds")
    print("the results are:", results)
    
