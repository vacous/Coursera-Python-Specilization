"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(100)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}


def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    best_moves = []
    result_value = []
    
    player_sign = player/abs(player)
    for ele in board.get_empty_squares():
        copy_board = board.clone()
        copy_board.move(ele[0],ele[1],player) 


        if copy_board.check_win() == provided.PLAYERX:
            board_value = 1 * player_sign
            best = ele 
            result = board_value
            if player_sign == -1:
                break
        elif copy_board.check_win() == provided.PLAYERO:
            board_value = -1 * player_sign
            best = ele 
            result = board_value
            if player_sign == 1:
                break 
        elif copy_board.check_win() == provided.DRAW:
            board_value = 0 
            best = ele
            result = board_value
            #print copy_board
        else:
            result, best = mm_move( copy_board , provided.switch_player(player)  )
            
    best_moves.append(best)
    result_value.append(result)
    
    best_result_value = max(result_value)
    best_move = best_moves[ result_value.index(best_result_value)]
     
    #print best_move 
    return best_result_value, best_move

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    # the next possible move:
    move = mm_move(board, player)
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

#provided.play_game(move_wrapper, 1, False)        
#poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)
#board = provided.TTTBoard(3)
#board.move(1,1,provided.PLAYERX)
#board.move(1,0,provided.PLAYERO)
#
#
#print board 
#print mm_move(board, provided.PLAYERX)
#print counter 

