# https://www.redblobgames.com/pathfinding/grids/graphs.html

GRID_SIZE_X = 20
GRID_SIZE_Y = 10

all_nodes = []

obstacles = [[0,0], [0,1]];

for x in range(GRID_SIZE_X):
    for y in range(GRID_SIZE_Y):
        # remove obstacles from grid
        if [x,y] not in obstacles:
            all_nodes.append([x, y])

print(all_nodes)

def neighbors(node):
    # get neighbors north/south/east/west directions of node
    # if game has diagonal movement then might have 8 entries instead of 4
    dirs = [[1,0], [0,1], [-1,0], [0,-1]]
    result = []
    for dir in dirs:
        neighbor = [node[0] + dir[0], node[1] + dir[1]]
        # check that neighbor isn't outside the rectangular grid boundary
        # check that neighbor isn't an obstacle
        if 0 <= neighbor[0] < GRID_SIZE_X and 0 <= neighbor[1] < GRID_SIZE_Y and [neighbor[0], neighbor[1]] not in obstacles:
            result.append(neighbor)

    return result

print(neighbors(all_nodes[0]))
    
