class Dequeue:

    def __init__(self, n=10):
        self.arr = []
        self.size = n
        self.head = 0
        self.tail = 0
        self.counter = 0

        if n < 1:
            self.arr = [0] * 10
        else:
            self.arr = [0] * n

    def setSize(self):
        arr2 = [0] * (2 * len(self.arr))

        for i in range(0, len(self.arr)):
            arr2[i] = self.arr[i]
        self.arr = arr2
        self.size = len(self.arr)

    def addLeft(self, value):  # Moving in increasing index
        return None

    def getLeft(self):
        # Counting tail in addRight()
        # Counting head in getLeft()
        temp = 0
        if self.isEmpty():
            raise IndexError("Empty Queue!")

        temp = self.arr[self.head]
        if self.head == (self.size - 1):
            self.head = 0
        else:
            self.head += 1
        self.counter -= 1
        return temp

    def addRight(self, value):  # Moving in decreasing index

        if self.isFull():
            self.setSize()
        self.arr[self.tail] = value
        self.tail += 1
        self.counter += 1

    def getRight(self):
        if self.isEmpty():
            raise IndexError("Empty Queue!")
        else:
            self.counter -= 1
            return self.arr[self.head]

    def isEmpty(self):
        return self.counter == 0

    def isFull(self):
        return self.counter + self.head == self.size


# Part of the test driver below...

def main():
    DEF_SIZE = 10

    # begin TEST_FIFO
    # testing adding from one side and removing from the other

    print("Testing addRight, getLeft FIFO\n")

    bQ = Dequeue(DEF_SIZE)

    if bQ.isEmpty():
        print("Before testing array should be empty and it is\n")
    else:
        print("Before testing array should be empty and it is not\n")

    print("first add left, get right")
    bQ.addRight(1)
    bQ.addRight(2)
    bQ.addRight(3)
    print("  first, sb 1 = " + str(bQ.getLeft()), end="")
    print(" next, sb 2 = " + str(bQ.getLeft()), end="")
    print(" last, sb 3 = " + str(bQ.getLeft()))

    if bQ.isEmpty():
        print("After testing array should be empty and it is\n")
    else:
        print("After testing array should be empty and it is not\n")

    # end TEST_FIFO

    # begin TEST_WRAP
    # test if the queue wraps from left to right and right to left

    dQ = Dequeue(DEF_SIZE)

    print("Testing wrap when right reaches end of array: \n")

    print("Adding 10 even ints to right, removing four from left")
    for i in range(DEF_SIZE):
        dQ.addRight(2 * i)

    print("should be: 0 2 4 6 and are: ", end="")
    for i in range(4):
        print(str(dQ.getLeft()) + " ", end="")

    print("\nAdding 3 more to right (20, 22, 24)")
    for i in range(10, 13):
        dQ.addRight(2 * i)

    print("Now removing all from the left \n should be: 8 10 12 14 16 18 20 22 24")
    print(" they are:  ", end="")
    while not dQ.isEmpty():
        print(str(dQ.getLeft()) + " ", end="")

    print("\nDone with testing wrap on dequeue.\n")

    # end TEST_WRAP

    # begin TEST_EXCEPTIONS
    # testing removing from empty
    print("\nNow testing exceptions \n")

    eQ = Dequeue(DEF_SIZE)

    print("Testing get left on empty queue, should throw exception")
    try:
        eQ.getLeft()
        print("Should thrown exception, did not")
    except IndexError:
        print("Caught error with index error")
    except:
        print("Caught some other exception")

    print("\nDone testing exceptions\n")

    # end TEST_EXCEPTIONS

    # begin TEST_GROW
    # testing adding to full queue
    print("Now testing adding to a full array\n")

    fQ = Dequeue(DEF_SIZE)

    print("Testing overflow when adding to the right\n")
    print("Adding first ten odd integers to right side of Dequeue ")
    for i in range(DEF_SIZE):
        fQ.addRight(2 * i + 1)
        # print("elements in fQ are  ", fQ.getLeft())
    print("and removing three of them \n should be: 1  3  5 ")
    print(" they are:  ", end="")
    for i in range(3):
        print(str(fQ.getLeft()) + "  ", end="")

    print("\nNow adding five more, should cause wrap with growth")
    for i in range(10, 15):
        fQ.addRight(2 * i + 1)
        # print("elements in fQ are  ", fQ.getLeft())
    print("when we remove the remaining values, \n should be: 7 9 11 13 15 17 19 21 23 25 27 29 ")
    print(" they are:  ", end="")
    while not fQ.isEmpty():
        print(str(fQ.getLeft()) + " ", end="")

    print("\nDone testing adding to full dequeue\n")


# end TEST_GROW


if __name__ == '__main__':
    main()
