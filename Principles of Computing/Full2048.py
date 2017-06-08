"""
Clone of 2048 game.
"""

import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def list_add(list_1, list_2):
    '''
    Add two list together 
    '''
    result_list = []
    for index in range(len(list_1)):
        result_list.append(list_1[index]+list_2[index])
        
    return tuple(result_list)
        


def reshape(line):
    '''
    Reshape the line: 
    For example [2,2,0,2] ==> [2,2,2,0]
    '''
    tail_list = []
    while 0 in line:
        line.remove(0)
        tail_list.append(0)
    
    line.extend(tail_list) 


def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    result_line = list(line) 
    reshape(result_line)

    temp_index = 0 
    while temp_index + 1 < len(result_line):
        if result_line[temp_index] == result_line[temp_index +1]:
            result_line[temp_index] = 2 * result_line[temp_index]
            result_line[temp_index+1] = 0 
        temp_index += 1         
                
    reshape(result_line)        

    return result_line

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self._height_ = grid_height 
        self._width_ = grid_width 
        self._info_ = {UP: [ (0,0) , LEFT, 1, self._width_, self._height_],
                         DOWN: [ (-1,0) , LEFT, 1, self._width_, self._height_],
                         LEFT: [ (0,0) , UP, 0, self._height_, self._width_],
                         RIGHT: [ (0,-1) , UP, 0, self._height_, self._width_]}
        self._grid_ =[ [ 0 for _ in range(self._width_)] 
                    for _ in range(self._height_) ]
        self._indicator_ = True 
                
    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
         
        
        self.new_tile()
        self.new_tile()
        
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        return str(self._grid_) 

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._height_

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._width_

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        
         #{UP: [ (0,0) , LEFT, 1, self._width_],
         #DOWN: [ (-1,0) , LEFT, 1, self._width_],
         #LEFT: [ (0,0) , UP, 0, self._height_],
         #RIGHT: [ (0,-1) , UP, 0, self._height_]}
        """
        
        
        first_cell = self._info_[direction][0]
        
        while first_cell[self._info_[direction][2]] < self._info_[direction][3]:
            
            add_cell = first_cell 
            index_cell = [add_cell] 
            
            line = [self.get_tile(first_cell[0],first_cell[1])]
            
            first_cell = list_add(first_cell, OFFSETS[self._info_[direction][1]])
            
            while len(line) < self._info_[direction][4]:
                add_cell = list_add(add_cell,OFFSETS[direction])
                line.append(self.get_tile(add_cell[0],add_cell[1]))
                index_cell.append(add_cell)
            
            
            print line == merge(line)
            self._indicator_ = self._indicator_ and (line == merge(line))          
            
            line = merge(line)
            
            for count in range(len(line)):
                self.set_tile(index_cell[count][0],index_cell[count][1], line[count])
                
            
            #print line 
            # print index_cell
        
        #print self.change_indicator 
        
        print self._grid_
        
        if self._indicator_ == False:
            self.new_tile()
        print '_____________________'
        
        self.get_empty()
        self._indicator_ = True 
     
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        ava_initial = [4] + [2] * 9
    
        empty_list = self.get_empty()
        new_tile = random.choice(ava_initial)
        temp_grid = random.choice(empty_list)
        self.set_tile(temp_grid[0],temp_grid[1],new_tile)
                

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        # replace with your code
        self._grid_[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._grid_[row][col]
    
    def get_empty(self):
        '''
        Return the empty indicies for adding new tile
        '''
        empty_list = []
        for row_index in range(self._height_):
            if 0 in self._grid_[row_index]:
                for col_index in range(self._width_):
                    if self._grid_[row_index][col_index] == 0:
                        empty_list.append([row_index,col_index])
                    
        return empty_list
        
        
poc_2048_gui.run_gui(TwentyFortyEight(4, 4))


