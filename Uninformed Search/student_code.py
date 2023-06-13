import common

# Find the starting position before the search
def find_start_pos(map):
    for y in range(common.constants.MAP_HEIGHT):
        for x in range(common.constants.MAP_WIDTH):
            if map[y][x] == 2:
                return (y, x)
            
# Find the goal position
def find_goal_pos(map):
    for y in range(common.constants.MAP_HEIGHT):
        for x in range(common.constants.MAP_WIDTH):
            if map[y][x] == 3:
                return (y, x)
                
def df_search(map):
    # access the map using "map[y][x]"
    # y between 0 and common.constants.MAP_HEIGHT-1
    # x between 0 and common.constants.MAP_WIDTH-1
	
    # initialize
    stack = [] #LIFO
    start_pos = find_start_pos(map)
    stack.append(start_pos)

    # track each explored cell
    movements = {}
    movements[start_pos] = None

    # search
    while stack: # explore a path as far as it goes before backtracking to explore other paths
        # Remove the last element from the stack
        y, x = stack.pop() #LIFO: grab last element of list
        if map[y][x] == 3: # GOAL
            # Destination found; mark the path
            map[y][x] = 5
            # backtrack from goal position to start position
            while movements[(y,x)] is not None:
                y, x = movements[(y,x)]
                map[y][x] = 5
            return True
        elif map[y][x] == 0 or map[y][x] == 2:
            # Mark the cell as explored and add unexplored neighbors to stack in desired search order
            map[y][x] = 4
            # Conditions: Edge Case, Wall, If-Explored
            if y > 0 and y - 1 >= 0:
                if map[y-1][x] != 1 and map[y-1][x] != 4:
                    stack.append((y-1, x))
                    movements[(y-1, x)] = (y, x)
            if x > 0 and x - 1 >= 0:
                if map[y][x-1] != 1 and map[y][x-1] != 4:
                    stack.append((y, x-1))
                    movements[(y, x-1)] = (y, x)
            if y < common.constants.MAP_HEIGHT - 1:
                if map[y+1][x] != 1 and map[y+1][x] != 4:
                    stack.append((y+1, x))
                    movements[(y+1, x)] = (y, x)
            if x < common.constants.MAP_WIDTH - 1:
                if map[y][x+1] != 1 and map[y][x+1] != 4:
                    stack.append((y, x+1))
                    movements[(y, x+1)] = (y, x)
    # Destination not found
    return False

def bf_search(map):
    # access the map using "map[y][x]"
    # y between 0 and common.constants.MAP_HEIGHT-1
    # x between 0 and common.constants.MAP_WIDTH-1

    # initialize
    queue = [] #FIFO
    start_pos = find_start_pos(map)
    queue.append(start_pos)

    # track movements
    movements = {}
    movements[start_pos] = None

    # search
    while queue: # continue exploring nodes until we have visited all reachable nodes
        # Remove the first element from the queue
        y, x = queue.pop(0) #FIFO: grab first element of list
        if map[y][x] == 3: # GOAL
            # Destination found; mark the path
            map[y][x] = 5
            # backtrack from goal position to start position
            while movements[(y,x)] is not None:
                y, x = movements[(y,x)]
                map[y][x] = 5
            return True
        elif map[y][x] == 0 or map[y][x] == 2:
            # Mark the cell as explored and add unexplored neighbors to queue
            map[y][x] = 4
            # Conditions: Edge Case, Wall, If-Explored
            if x < common.constants.MAP_WIDTH - 1:
                if map[y][x+1] != 1 and map[y][x+1] != 4:
                    queue.append((y, x+1))
                    movements[(y, x+1)] = (y, x)
            if y < common.constants.MAP_HEIGHT - 1:
                if map[y+1][x] != 1 and map[y+1][x] != 4:
                    queue.append((y+1, x))
                    movements[(y+1, x)] = (y, x)
            if x > 0 and x - 1 >= 0:
                if map[y][x-1] != 1 and map[y][x-1] != 4:
                    queue.append((y, x-1))
                    movements[(y, x-1)] = (y, x)
            if y > 0 and y - 1 >= 0:
                if map[y-1][x] != 1 and map[y-1][x] != 4:
                    queue.append((y-1, x))
                    movements[(y-1, x)] = (y, x)
    # Destination NOT found
    return False