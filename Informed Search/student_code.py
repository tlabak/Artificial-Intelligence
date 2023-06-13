QUEENS = 10

# Count the number of queens that can attack each other
def count_attacks(board):
    count = 0
    # x - col no., y - row no.
    for x in range(len(board)):
        for y in range(len(board)):
            if board[y][x] == 1:
                # Check horizontal attacks
                for i in range(len(board)):
                    if board[y][i] == 1 and i != x:
                        count += 1
                # Check vertical attacks
                for j in range(len(board)):
                    if board[j][x] == 1 and j != y:
                        count += 1
                # Check diagonal attacks
                # from top-left to bottom-right
                for i, j in zip(range(x-1, -1, -1), range(y-1, -1, -1)):
                    if board[j][i] == 1:
                        count += 1
                # from bottom-right to top-left
                for i, j in zip(range(x+1, len(board)), range(y+1, len(board))):
                    if board[j][i] == 1:
                        count += 1
                # from top-right to bottom-left
                for i, j in zip(range(x-1, -1, -1), range(y+1, len(board))):
                    if board[j][i] == 1:
                        count += 1
                # from bottom-left to top-right
                for i, j in zip(range(x+1, len(board)), range(y-1, -1, -1)):
                    if board[j][i] == 1:
                        count += 1
    # Each attack is counted twice, so divide by 2 to get the actual number of attacks
    return count // 2

def gradient_search(board):
	# Compute the initial number of attacks between queens
    current_attacks = count_attacks(board)

    while True:
        # Initialize
        best_move = None
        best_attacks = current_attacks # Number of attacks in current configuration

        # Iterate over all queens
        for x in range(len(board)):
            for y in range(len(board)):
                # if (x,y) is a Queen
                if board[y][x] == 1:
                    # Moving the queen up and down in its column
                    for new_y in range(len(board)):
                        # Don't want to be at 'old' position
                        if new_y != y:
                            # Create a new board configuration by moving the queen
                            new_board = [row[:] for row in board] # Create a new board configuration without modifying the original board
                            new_board[new_y][x] = 1 # Queen is at new position along its column
                            new_board[y][x] = 0 # old position is no longer where the Queen is at 

                            # Compute the number of attacks in the new board configuration
                            new_attacks = count_attacks(new_board)
                            # Choose the move with the lowest number of attacks, immediately - greedy
                            if new_attacks < best_attacks:
                                best_move = (x, y, new_y)
                                best_attacks = new_attacks
                            # *Tie-breaking Handling*
                            elif new_attacks == best_attacks and best_move is not None:
                                # Choose the queen with the lowest x value
                                if x < best_move[0]:
                                    best_move = (x, y, new_y)
                                # If the x values are the same, choose the queen with the lowest y value
                                elif x == best_move[0] and new_y < best_move[2]:
                                    best_move = (x, y, new_y)

        # If there is no move that reduces the number of attacks, STOP
        if best_move is None:
            break

        # Make the best move, immediately, and update board
        x, old_y, new_y = best_move
        board[new_y][x] = 1 # Queen @ new position
        board[old_y][x] = 0 # Queen no longer at old position
        current_attacks = best_attacks

    # Check if the final configuration is a solution; check if the board is a solution
    if count_attacks(board) == 0:
        return True
    else:
        return False