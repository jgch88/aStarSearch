import collections

# deque is a O(1) efficient list
# for appends/pops on either side
# of the deque

# probably a linked list?

class Queue:
    def __init__(self):
        self.elements = collections.deque()

    def empty(self):
        return len(self.elements) == 0

    def put(self, x):
        self.elements.append(x)

    def get(self):
        return self.elements.popleft()

    
