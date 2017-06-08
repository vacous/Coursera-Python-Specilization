"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
    def __str__(self):
        output = 'Human: ' + str(self._human_list) + '/n'
        output += 'Zombie: ' + str(self._zombie_list) + '/n'
        
        return output 
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        self._human_list = []
        self._zombie_list = []
        poc_grid.Grid.clear(self)
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append( (row,col) )
           
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len( self._zombie_list )       
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        for zom in self._zombie_list:
            yield zom
        

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append( (row,col) )
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len( self._human_list )
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        for hum in self._human_list:
            yield hum
        
        
    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        
        # initialize the distance field and visited array 
        visited = []
        distance_field= []
        for _ in range(self._grid_height):
            dist_inner=[]
            visited_inner = []
            for _ in range(self._grid_width):
                dist_inner.append( self._grid_width * self._grid_height )
                visited_inner.append(False)

            distance_field.append(dist_inner)
            visited.append(visited_inner)

         
        # which entity
        if entity_type == HUMAN:
            entity = self._human_list 
            #neb_func = self.eight_neighbors
        elif entity_type == ZOMBIE:
            entity= self._zombie_list 
            #neb_func = self.four_neighbors
            
        # initialize boundary, vistied and distance_field 
        boundary = poc_queue.Queue()
        for ele in entity:
            boundary.enqueue(ele)
            visited[ele[0]][ele[1]] = True
            distance_field[ele[0]][ele[1]] = 0
            
        # BFS search
        while [ ele for ele in boundary] !=  []:
            cell = boundary.dequeue()
            neighbors = self.four_neighbors(cell[0],cell[1])
            for neighbor in neighbors:
                if visited[neighbor[0]][neighbor[1]] == False:
                    if self.is_empty(neighbor[0],neighbor[1]):
                        visited[neighbor[0]][neighbor[1]] = True
                        boundary.enqueue(neighbor)
                        #if self.is_empty(neighbor[0],neighbor[1]):
                        distance_field[neighbor[0]][neighbor[1]] = distance_field[cell[0]][cell[1]] + 1 
   
        return distance_field
    
    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        
        print 'old'
        print self._human_list
        print '' 
        
        for human in self._human_list:
            neighbors = self.eight_neighbors(human[0],human[1])
            dist = zombie_distance_field[human[0]][human[1]]
            replace = human 
                 
            for neighbor in neighbors:
                if self.is_empty(neighbor[0],neighbor[1]):
                    if zombie_distance_field[neighbor[0]][neighbor[1]] > dist:
                        dist = zombie_distance_field[neighbor[0]][neighbor[1]]
                        replace = neighbor 
                        
            self._human_list[ self._human_list.index(human) ] = replace 

        return  
    
    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        for zombie in self._zombie_list:
            neighbors = self.four_neighbors(zombie[0],zombie[1])
            dist = human_distance_field[zombie[0]][zombie[1]]
            replace = zombie 

            
            for neighbor in neighbors:
                if self.is_empty(neighbor[0],neighbor[1]):
                    if human_distance_field[neighbor[0]][neighbor[1]] < dist:
                        dist = human_distance_field[neighbor[0]][neighbor[1]]
                        replace = neighbor 
                        
            self._zombie_list[ self._zombie_list.index( zombie ) ] = replace  
        return 

# Start up gui for simulation - You will need to write some code above
# before this will work without errors

poc_zombie_gui.run_gui(Apocalypse(15, 5))
