import heapq

class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    # we're using tuples for item e.g. (priority, node)
    def put(self, item, priority):
        # push item onto heap, maintaining heap invariant
        # python3 uses zero indexed minimum heaps
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        # access the node inside the item tuple
        # e.g. item = (priority, node), item[1]
        # we don't want the tuple, just the node
        return heapq.heappop(self.elements)[1]
