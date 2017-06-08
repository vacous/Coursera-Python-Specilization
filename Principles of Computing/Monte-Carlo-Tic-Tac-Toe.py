"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 100         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player
    
# Add your functions here.

def mc_trial(board, player):
    ''' 
    Play the game until it ends 
    '''
    while board.check_win() == None:
        ava_loc = board.get_empty_squares()
        next_move_loc = random.choice(ava_loc)
        board.move(next_move_loc[0],next_move_loc[1],player) 
        player = provided.switch_player(player)
        
def mc_update_scores(scores, board, player):
    '''
    update the score
    '''
    result = board.check_win()
    print player
    print scores 
    print ''
         
    if result != provided.DRAW:
        for index_height in range( board.get_dim() ):
            for index_width in range( board.get_dim() ):
                if board.square(index_height, index_width) == result:
                    scores[index_height][index_width] += SCORE_CURRENT
                elif board.square(index_height, index_width) == provided.switch_player(result): 
                    scores[index_height][index_width] -=  SCORE_OTHER
                   
    print board
    print player,result
    print scores
            
                
            
def get_best_move(board, scores):
    '''
    find the best move
    '''
    if board.get_empty_squares != []:
        max_score = -100
        max_loc = []
        # for all the grids 
        for index_height in range( board.get_dim() ):
            for index_width in range( board.get_dim() ):
                # if belong to a empty grid 
                if (index_height,index_width) in board.get_empty_squares():
                    # add location to the array if equals to the max
                    if scores[index_height][index_width] == max_score:
                        max_loc.append((index_height,index_width))
                    # replace the max if larger, and remove the old loc array    
                    elif scores[index_height][index_width] > max_score:  
                        max_loc = []
                        max_loc.append((index_height,index_width))
                        max_score = scores[index_height][index_width]
                
    return random.choice(max_loc)


def mc_move(board, player, trials):
    '''
    make a move
    '''
    scores = [[0]*board.get_dim()] * board.get_dim()
    for _ in range(trials):
        clone_board = board.clone()
        mc_trial(clone_board,player)
        mc_update_scores(scores, clone_board, player)
        
    
    print board
    print scores
    return get_best_move(board,scores)


# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

#provided.play_game(mc_move, NTRIALS, False)        
#poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)

get_best_move(provided.TTTBoard(3, False, [[provided.EMPTY, provided.PLAYERX, provided.EMPTY], [provided.PLAYERO, provided.PLAYERX, provided.EMPTY], [provided.PLAYERO, provided.EMPTY, provided.EMPTY]]), [[-3, 6, -2], [8, 0, -3], [3, -2, -4]]) 
