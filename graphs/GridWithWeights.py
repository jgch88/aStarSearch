from SquareGridGraph import SquareGrid

class GridWithWeights(SquareGrid):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.weights = {}

    def cost(self, from_node, to_node):
        # dictionary's get() method's 2nd parameter is
        # the value to return IF key isn't found
        # i.e. default cost is 1
        return self.weights.get(to_node, 1)
