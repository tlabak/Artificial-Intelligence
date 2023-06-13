import common

def minmax_tictactoe(board, turn):
	#put your code here:
	#it must return common.constants.X(1), common.constants.O(2) or common.constants.NONE(0) for tie.
	#use the function common.game_status(board), to evaluate a board
	#it returns common.constants.X(1) if X wins, common.constants.O(2) if O wins or common.constants.NONE(0) if tie or game is not finished
	#the program will keep track of the number of boards evaluated
    # If the game is over, return the winner

    result = common.game_status(board)

    # if there is a winning path, return the winner
    if result != common.constants.NONE:
        print("winning path: ", result)
        return result
    # check for ties
    elif all(val != common.constants.NONE for val in board):
        print("tie: ", result)
        return common.constants.NONE
    # otherwise, search the game tree
    else:
        # maximize
        if turn == common.constants.X:
            v = -float("inf")
            for i in range(len(board)):
                if common.get_cell(board, i // 3, i % 3) == common.constants.NONE:
                    common.set_cell(board, i // 3, i % 3, common.constants.X)
                    v = max(v, minmax_tictactoe(board, common.constants.O))
                    common.set_cell(board, i // 3, i % 3, common.constants.NONE)
            return v
        # minimize
        if turn == common.constants.O:
            v = float("inf")
            for i in range(len(board)):
                if common.get_cell(board, i // 3, i % 3) == common.constants.NONE:
                    common.set_cell(board, i // 3, i % 3, common.constants.O)
                    v = min(v, minmax_tictactoe(board, common.constants.X))
                    common.set_cell(board, i // 3, i % 3, common.constants.NONE)
            return v
    return 2

"""
    result = common.game_status(board)

    # if there is a winning path, return the winner
    if result != common.constants.NONE:
        return result
    # check for ties
    elif all(val != common.constants.NONE for val in board) and result == common.constants.NONE:
        return common.constants.NONE
    # if the board is filled, game ends in a tie
    elif all(val != common.constants.NONE for val in board):
        return result
    # otherwise, search the game tree
    else:
        # maximize
        if turn == common.constants.X:
            v = -float("inf")
            for i in range(len(board)):
                if common.get_cell(board, i // 3, i % 3) == common.constants.NONE:
                    common.set_cell(board, i // 3, i % 3, common.constants.X)
                    v = max(v, minmax_tictactoe(board, common.constants.O))
                    common.set_cell(board, i // 3, i % 3, common.constants.NONE)
            return v
        # minimize
        if turn == common.constants.O:
            v = float("inf")
            for i in range(len(board)):
                if common.get_cell(board, i // 3, i % 3) == common.constants.NONE:
                    common.set_cell(board, i // 3, i % 3, common.constants.O)
                    v = min(v, minmax_tictactoe(board, common.constants.X))
                    common.set_cell(board, i // 3, i % 3, common.constants.NONE)
            return v
"""

def abprun_tictactoe(board, turn):
    #put your code here:
    #it must return common.constants.X(1), common.constants.O(2) or common.constants.NONE(0) for tie.
    #use the function common.game_status(board), to evaluate a board
    #it returns common.constants.X(1) if X wins, common.constants.O(2) if O wins or common.constants.NONE(0) if tie or game is not finished
    #the program will keep track of the number of boards evaluated
    return prune(board, turn, -float("inf"), float("inf"))

def prune(board, turn, alpha, beta):
    result = common.game_status(board)

    # if there is a winning path, return the winner
    if result != common.constants.NONE:
        return result
    # check for ties
    elif all(val != common.constants.NONE for val in board) and result == common.constants.NONE:
        return common.constants.NONE
    # if the board is filled, game ends in a tie
    elif all(val != common.constants.NONE for val in board):
        return result
    # otherwise, search the game tree
    else:
        # maximize
        if turn == common.constants.X:
            v = -float("inf")
            for i in range(len(board)):
                if common.get_cell(board, i // 3, i % 3) == common.constants.NONE:
                    common.set_cell(board, i // 3, i % 3, common.constants.X)
                    r = max(v, prune(board, common.constants.O, alpha, beta))
                    common.set_cell(board, i // 3, i % 3, common.constants.NONE)
                    if r > v:
                        v = r
                    if v >= beta:
                        return v
                    if v > alpha:
                        alpha = v
                    # alpha = max(alpha, v)
            return v
        # minimize
        if turn == common.constants.O:
            v = float("inf")
            for i in range(len(board)):
                if common.get_cell(board, i // 3, i % 3) == common.constants.NONE:
                    common.set_cell(board, i // 3, i % 3, common.constants.O)
                    r = min(v, prune(board, common.constants.X, alpha, beta))
                    common.set_cell(board, i // 3, i % 3, common.constants.NONE)
                    if r < v:
                        v = r
                    if v <= alpha:
                        return v
                    if v < beta:
                        beta = v
                    # beta = min(beta, v)
            return v