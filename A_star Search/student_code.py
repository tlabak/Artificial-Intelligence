import copy

# Goal state
goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]

# Heuristic function (Manhattan distance)
def heuristic(state):
    distance = 0
    for i in range(len(state)):
        if state[i] != 0:
            # Manhattan Distance: |x1 - x2| + |y1 - y2|
            distance += abs(i // 3 - (state[i]-1) // 3) + abs(i % 3 - (state[i]-1) % 3)
    return distance

# Concatenate the board array into one number
def concat_board(board):
    return "".join(str(i) for i in board)

# A* search
def astar(board):
    # Initialize the initial node and the frontier
    initial_node = {"state": board, "depth": 0, "cost": heuristic(board), "action": None}
    frontier = [initial_node]
    # Initialize the explored set and the sequence of actions
    explored = set()
    actions = []

    while frontier:
        # Choose the node with the lowest cost f(n) in the frontier
        node = min(frontier, key=lambda x: (x["cost"], -int(concat_board(x["state"]))))

        # Add node to the explored set
        explored.add(tuple(node["state"]))

        # If the node is the goal state, construct the sequence of actions and return the results
        if node["state"] == goal_state:
            print_board(node["state"])
            while node["action"] is not None:
                actions.append(node["action"])
                node = node["parent"]
            actions.reverse()
            # Return the depth, number of nodes expanded, and the sequence of actions
            return len(actions), len(explored), actions

        # Remove the node from the frontier
        frontier.remove(node)

        # the 'new_state' is the successor/child of a node!
        successors = []
        i = node["state"].index(0) # at what index is "0" in the array (the only tile that can move)
        if i > 2:  # Move up
            j = i - 3 # new index given action
            new_state = node["state"][:] # creates a copy of the list puzzle at the current node
            new_state[i], new_state[j] = new_state[j], new_state[i] # move/swap tile 
            if tuple(new_state) not in explored:
                successors.append({"state": new_state, "depth": node["depth"] + 1, "cost": node["depth"] + 1 + heuristic(new_state), "action": 0, "parent": node})
        if i % 3 < 2:  # Move right
            j = i + 1
            new_state = node["state"][:] 
            new_state[i], new_state[j] = new_state[j], new_state[i]
            if tuple(new_state) not in explored:
                successors.append({"state": new_state, "depth": node["depth"] + 1, "cost": node["depth"] + 1 + heuristic(new_state), "action": 1, "parent": node})
        if i < 6:  # Move down
            j = i + 3
            new_state = node["state"][:] 
            new_state[i], new_state[j] = new_state[j], new_state[i]
            if tuple(new_state) not in explored:
                successors.append({"state": new_state, "depth": node["depth"] + 1, "cost": node["depth"] + 1 + heuristic(new_state), "action": 2, "parent": node})
        if i % 3 > 0:  # Move left
            j = i - 1
            new_state = node["state"][:]
            new_state[i], new_state[j] = new_state[j], new_state[i]
            if tuple(new_state) not in explored:
                successors.append({"state": new_state, "depth": node["depth"] + 1, "cost": node["depth"] + 1 + heuristic(new_state), "action": 3, "parent": node})

        # Add the successor nodes to the frontier
        for successor in successors:
            # Check if the state of the successor node is already in the frontier
            for i, frontier_node in enumerate(frontier):
                if frontier_node["state"] == successor["state"]:
                    # Check if the cost of the successor node is less than that of the node in the frontier
                    if frontier_node["cost"] > successor["cost"]:
                        frontier[i] = successor # update the node in the frontier with the successor node
                    # Break if a matching node is found in the frontier
                    break
            else:
                frontier.append(successor)


    # If the goal state is not found, return None
    return None

#graphic print of board, feel free to use, or not
def print_board(board):
    print("\n")
    print("------------")
    print(
        "{:02d}".format(board[0]),
        "|",
        "{:02d}".format(board[1]),
        "|",
        "{:02d}".format(board[2]),
    )
    print("------------")

    print(
        "{:02d}".format(board[3]),
        "|",
        "{:02d}".format(board[4]),
        "|",
        "{:02d}".format(board[5]),
    )
    print("------------")

    print(
        "{:02d}".format(board[6]),
        "|",
        "{:02d}".format(board[7]),
        "|",
        "{:02d}".format(board[8]),
    )
    print("------------")



