class Iterator_2:

    def __init__(self, start, stop, step=1):
        self.index = start
        self.stop = stop
        self.step = step

    def __iter__(self):
        return self
    
    def __next__(self):
        self.index += self.step
        if self.index < self.stop:
            return self.index
        else:
            raise StopIteration

if __name__ == "__main__":

    print("Testing Iterator_2")
    qwerty = Iterator_2(0,40,2)
    for i in qwerty:
        print(i)
        if i == 16:
            break
    print("This is Iterator_2 after the break.")
    for i in qwerty:
        print(i)     