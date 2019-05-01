from SimpleGraph import SimpleGraph 
from SquareGridGraph import SquareGrid, draw_grid
from GridWithWeights import GridWithWeights
from Queue import Queue
from PriorityQueue import PriorityQueue

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

# implementation 4: dijkstra. 
# the graph needs to know the cost of movement
# the queue needs to return nodes in a prioritised order
# the search needs to keep track of the costs from the graph and queue them in a prioritised manner
def dijkstra_search(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)

    # different from first implementation in that it remembers
    # WHERE we came from, not just that we visited it
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

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
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost
                frontier.put(next, priority)
                came_from[next] = current

    return came_from, cost_so_far

def reconstruct_path(came_from, start, goal):
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path

# in Civilisation (the game), moving through plains/deserts might cost 1 move-point
# but moving through forests costs 5
# and moving through water costs 10. 
# even on a grid, distance != cost of movement!
# https://www.redblobgames.com/pathfinding/a-star/introduction.html

civilisation_map = GridWithWeights(10, 10)
civilisation_map.walls = [(1, 7), (1, 8), (2, 7), (2, 8), (3, 7), (3, 8)]

# generates a dictionary of tuple: 5
# for 'forest' locations
civilisation_map.weights = {loc: 5 for loc in [(3, 4), (3, 5), (4, 1), (4, 2),
                                       (4, 3), (4, 4), (4, 5), (4, 6), 
                                       (4, 7), (4, 8), (5, 1), (5, 2),
                                       (5, 3), (5, 4), (5, 5), (5, 6), 
                                       (5, 7), (5, 8), (6, 2), (6, 3), 
                                       (6, 4), (6, 5), (6, 6), (6, 7), 
                                       (7, 3), (7, 4), (7, 5)]}

civ_start = (1,4)
civ_end = (8,5)
came_from, cost_so_far = dijkstra_search(civilisation_map, civ_start, civ_end)
draw_grid(civilisation_map, point_to=came_from, start=civ_start, goal=civ_end, width=3)
draw_grid(civilisation_map, number=cost_so_far, start=civ_start, goal=civ_end, width=3)
draw_grid(civilisation_map, path=reconstruct_path(came_from, start=civ_start, goal=civ_end), start=civ_start, goal=civ_end, width=3)


# implementation 5: A* Search
# use both a heuristic function and ordering from dijkstra's algorithm.
# (using only the heuristic without dikjstra's weights is the same as Greedy Best-First search)

# our heuristic is the "manhattan distance" between two points on a grid
def heuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)

def a_star_search(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)

    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break

        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next) # reduce priority for positions further away from goal
                frontier.put(next, priority)
                came_from[next] = current

    return came_from, cost_so_far

came_from, cost_so_far = a_star_search(civilisation_map, civ_start, civ_end)
draw_grid(civilisation_map, point_to=came_from, start=civ_start, goal=civ_end, width=3)
draw_grid(civilisation_map, number=cost_so_far, start=civ_start, goal=civ_end, width=3)
draw_grid(civilisation_map, path=reconstruct_path(came_from, start=civ_start, goal=civ_end), start=civ_start, goal=civ_end, width=3)
