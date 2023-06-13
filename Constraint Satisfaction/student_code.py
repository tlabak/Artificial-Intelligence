import common

# helpful, but not needed
class variables:
    counter = 0

def find_empty_cell(sudoku):
    for y in range(9):
        for x in range(9):
            if sudoku[y][x] == 0:
                return y, x
    return -1, -1

def get_domain(sudoku, y, x):
    domain = set(range(1, 10))
    for i in range(9):
        domain.discard(sudoku[y][i])
        domain.discard(sudoku[i][x])
        domain.discard(sudoku[int(y / 3) * 3 + int(i / 3)][int(x / 3) * 3 + i % 3])
    return domain

def get_min_domain_cell(sudoku):
    min_domain = set(range(1, 10))
    min_domain_cell = None
    for y in range(9):
        for x in range(9):
            if sudoku[y][x] == 0:
                domain = get_domain(sudoku, y, x)
                if len(domain) < len(min_domain):
                    min_domain = domain
                    min_domain_cell = (y, x)
    return min_domain_cell, min_domain

# Backtracking

def sudoku_backtracking(sudoku):
    variables.counter = 0
    helper_backtracking(sudoku)
    return variables.counter

def helper_backtracking(sudoku):
    variables.counter += 1
    # Find the next empty cell
    y, x = find_empty_cell(sudoku)
    if y == -1 and x == -1:
        # Board is filled, stop recursion
        return True
    # Try values from 1 to 9
    for z in range(1, 10):
        if common.can_yx_be_z(sudoku, y, x, z):
            # Fill the empty cell with the valid value
            sudoku[y][x] = z
            # Recursively call to fill the next empty cell
            if helper_backtracking(sudoku):
                return True
            # Backtrack if the current value did not lead to a solution
            sudoku[y][x] = 0
    return False

# Forward-Checking

def sudoku_forwardchecking(sudoku):
    variables.counter = 0
    helper_forwardchecking(sudoku)
    return variables.counter

def helper_forwardchecking(sudoku):
    variables.counter += 1
    # find the cell with the smallest domain
    min_domain_cell, min_domain = get_min_domain_cell(sudoku)
    # if there is no empty cell, the board is complete
    if min_domain_cell is None:
        return True

    # select the next empty cell
    y, x = min_domain_cell
    # try all possible values in the cell's domain
    for z in min_domain:
        # if the value is valid for the cell, assign it and move on to the next cell
        if common.can_yx_be_z(sudoku, y, x, z):
            sudoku[y][x] = z
            if helper_forwardchecking(sudoku):
                return True
            # if assigning the value doesn't lead to a solution, undo the assignment
            sudoku[y][x] = 0

    # if no value in the domain leads to a solution, backtrack
    return False