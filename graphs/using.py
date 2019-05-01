from SimpleGraph import SimpleGraph 
from SquareGridGraph import SquareGrid, draw_grid
from Queue import Queue

# an arbitrary graph
example_graph = SimpleGraph()
example_graph.edges = {
        'A': ['B'],
        'B': ['A', 'C', 'D'],
        'C': ['A'],
        'D': ['E', 'A'],
        'E': ['B'],
        'F': []
}

# implementation 1: grid traversal
def breadth_first_search_1(graph, start):
    frontier = Queue()
    frontier.put(start)

    visited = {}
    visited[start] = True

    while not frontier.empty():
        # from front of the queue
        current = frontier.get()
        print("Visiting ", current)

        # get neighbors of current node
        # add it to back of frontier queue if not yet visited
        for next in graph.neighbors(current):
            if next not in visited:
                frontier.put(next)
                visited[next] = True

# prints the order in which the entire graph is visited
# works even if graph isn't completely connected,
# it just traces through nodes connected to starting node
breadth_first_search_1(example_graph, 'B')


# a grid graph
g = SquareGrid(30,15)
g.walls = [
        (21,0), (21, 1), (21,2),
        (22,0), (22, 1), (22,2),
        (23,0), (23, 1), (23,2),
        ]

draw_grid(g)
start = (0,0)
breadth_first_search_1(g, start)

# implementation 2: remembering path taken while exploring grid via bfs
def breadth_first_search_2(graph, start):
    frontier = Queue()
    frontier.put(start)

    # different from first implementation in that it remembers
    # WHERE we came from, not just that we visited it
    came_from = {}
    came_from[start] = None

    while not frontier.empty():
        # from front of the queue
        current = frontier.get()
        # print("Visiting ", current)

        # get neighbors of current node
        # add it to back of frontier queue if not yet visited
        for next in graph.neighbors(current):
            if next not in came_from:
                frontier.put(next)
                came_from[next] = current

    return came_from

parents = breadth_first_search_2(g, start)
draw_grid(g, point_to=parents, start=start)


# implementation 3: stopping the algorithm once goal is reached
# notice the additional goal parameter
def breadth_first_search_3(graph, start, goal):
    frontier = Queue()
    frontier.put(start)

    # different from first implementation in that it remembers
    # WHERE we came from, not just that we visited it
    came_from = {}
    came_from[start] = None

    while not frontier.empty():
        # from front of the queue
        current = frontier.get()
        # print("Visiting ", current)

        # main difference from implementation 2
        if current == goal:
            break

        # get neighbors of current node
        # add it to back of frontier queue if not yet visited
        for next in graph.neighbors(current):
            if next not in came_from:
                frontier.put(next)
                came_from[next] = current

    return came_from

end = (24, 0)
parents = breadth_first_search_3(g, start, end)
draw_grid(g, point_to=parents, start=start)
