"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui


# helper function 
def unroll(list1):
    '''
    return the unroll list
    '''
    output = [] 
    for ele in list1:
        output.extend(ele)
    return output     

def find(list1,ele):
    '''
    find the idx and jdx for a target ele
    '''
    for idx in range( len(list1) ):
        for jdx in range(len(list1[idx])):
            if list1[idx][jdx] == ele:
                result = [idx,jdx]
    return result              
                            


class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]
        
        # the solved array 
        self._solve = [ [[] for _ in range(self._width)] for _ in range(self._height) ]
        for num in range(self._height * self._width):
            self._solve[num // self._width][num % self._width] = num
            
                
    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]
    
    def get_solve(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._solve[row][col]
    
    
    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value
    
    def set_solve(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._solve[row][col] = value
    
    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction
        
        
    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        if self._grid[target_row][target_col] == 0:    
            for idx in range(target_row * self._width + target_col + 1, self._height * self._width):
                if unroll(self._grid)[idx] != unroll(self._solve)[idx]: 
                    return False 
        else:
            return False 
        return True 

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        move_made = ''
        move_value = self._solve[target_row][target_col]
        pos_value = find(self._grid,move_value)
        
        
        # move the tile to the target value position
        for _ in range(target_row - pos_value[0]):
            self.update_puzzle('u')
            move_made += 'u'     
            
        if pos_value[1] - target_col < 0:
            for _ in range(target_col - pos_value[1]):
                self.update_puzzle('l')
                move_made += 'l'
            for _ in range(target_col - pos_value[1] - 1):
                if pos_value[0] > 0:
                    self.update_puzzle('urrdl')
                    move_made += 'urrdl' 
                else:
                    self.update_puzzle('drrul')
                    move_made += 'drrul'
            for idx in range(target_row - pos_value[0]):
                if idx == 0:
                    self.update_puzzle('dru')
                    move_made += 'dru'
                else:
                    self.update_puzzle('lddru')
                    move_made += 'lddru'  
                    
        elif pos_value[1] - target_col > 0:
            for _ in range(pos_value[1] - target_col):
                self.update_puzzle('r')
                move_made += 'r'
                
            for _ in range(pos_value[1] - target_col - 1):
                if pos_value[0] > 0:
                    self.update_puzzle('ulldr')
                    move_made += 'ulldr'  
                else:
                    self.update_puzzle('dllur')
                    move_made += 'dllur'
            for idx in range(target_row - pos_value[0]):
                if idx == 0:
                    if pos_value[0] > 0:
                        self.update_puzzle('ullddru')
                        move_made += 'ullddru'    
                    else:
                        self.update_puzzle('dlu')
                        move_made += 'dlu'
                else:
                    self.update_puzzle('lddru')
                    move_made += 'lddru'  
        else:
            for _ in range(target_row - pos_value[0] -1):
                self.update_puzzle('lddru')
                move_made += 'lddru'
                
        # move the tile back to position
        if self.lower_row_invariant(target_row, target_col-1) == False:
                self.update_puzzle('ld')
                move_made += 'ld'
        return move_made

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
#        """
       
        move_made = ''
        self.update_puzzle('u')
        move_made += 'u'
        
        if self._solve[target_row][0] != self._grid[target_row][0]:
            if self._solve[target_row][0] != self._grid[target_row-1][1]:
                self.update_puzzle('r')
                move_made += 'r'      

                temp_board = self.clone()
                temp_board.set_solve(target_row - 1 ,1, temp_board.get_solve(target_row,0) ) 
                temp_move = temp_board.solve_interior_tile(target_row - 1, 1)
            
                self.update_puzzle(temp_move)
                move_made += temp_move
                print move_made
                
            self.update_puzzle('ruldrdlurdluurddlur')
            move_made += 'ruldrdlurdluurddlur'

            for _ in range(self._width - 2):
                self.update_puzzle('r')
                move_made += 'r'
            return move_made
        else:
            for _ in range(self._width - 1):
                self.update_puzzle('r')
                move_made += 'r'
            return move_made

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if self._grid[0][target_col] == 0:
            temp_board = self.clone()
            if target_col > 0:
                invariant_pos = [1,target_col-1]
            else:
                invariant_pos =[0,temp_board.get_width()-1]

            temp_board.set_number(invariant_pos[0],invariant_pos[1],0)    
            return temp_board.lower_row_invariant(invariant_pos[0],invariant_pos[1])
        else:
            return False 
        
    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        return self.lower_row_invariant(1, target_col)

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        move_made = ''
        self.update_puzzle('ld')
        move_made += 'ld'
        if self._grid[0][target_col] != self._solve[0][target_col] :   
                        
            temp_board = self.clone()
            temp_board.set_solve(1,target_col - 1, temp_board.get_solve(0,target_col))
            temp_move = temp_board.solve_interior_tile(1, target_col - 1)
            self.update_puzzle(temp_move)
            move_made += temp_move

            self.update_puzzle('urdlurrdluldrruld')
            move_made += 'urdlurrdluldrruld'
            
        return move_made

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        move_made = ''
        move_made += self.solve_interior_tile(1, target_col)
        self.update_puzzle('ur')
        move_made += 'ur'
        return  move_made

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        move_made = ''
        while self._grid[1][0] != self._width:
            self.update_puzzle('lurd')
            move_made += 'lurd'
                
        self.update_puzzle('ul') 
        move_made += 'ul'
        return move_made

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        if self._grid == self._solve:
            return ''
        
        move_made = ''
        ini_pos = find(self._grid,0)
        for _ in range(self._height - ini_pos[0] - 1):
            self.update_puzzle('d')
            move_made += 'd'
        for _ in range(self._width - ini_pos[1] - 1):
            self.update_puzzle('r')
            move_made += 'r'
        
        for jdx in range(self._height - 1 , 1 ,-1):
            for idx in range(self._width - 1,-1,-1): 
                if idx > 0:
                    move_made += self.solve_interior_tile(jdx,idx)
                else:
                    move_made += self.solve_col0_tile(jdx)
                print self._grid
    
        tile_pos = self._width-1 
        for _ in range(self._width-2):
            move_made += self.solve_row1_tile(tile_pos)
            move_made += self.solve_row0_tile(tile_pos)
            tile_pos -= 1
            
        move_made += self.solve_2x2()
        return move_made

