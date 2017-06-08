"""
Cookie Clicker Simulator
"""

import simpleplot
import math

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(100)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._total_cookies = 0.0
        self._cps = 1.0
        self._game_time = 0.0
        self._produced_cookies = 0.0

        self._history = [(0.0, None, 0.0, 0.0)] 
        
    def __str__(self):
        """
        Return human readable state
        """
        result = '\n'+'Time:' + str(self.get_time())  + '\n' + 'Current Cookies:' + str(self.get_cookies()) + '\n' +'CPS:' + str(self.get_cps())  + '\n' +'History' + str(self.get_history()) + '\n'+'Total Cookies: ' + str(self._produced_cookies)
        return result 
            
                  
                        
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._total_cookies 
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._game_time 
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        return self._history

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        
        if cookies >= self._total_cookies:
            
            cookies_diff = cookies - self._total_cookies
            time_wait = cookies_diff / self._cps 
            return math.ceil(time_wait)
        else:
            return 0.0
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time > 0:
            
            self._game_time += time 
            self._total_cookies += time * self._cps 
            self._produced_cookies += time * self._cps
        
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        
        if cost <= self._total_cookies:
        # record the game info when new item is added 
            self._history.append( (self.get_time(), item_name, cost, self._produced_cookies ))
                                 
            # update the state 
            self._cps += additional_cps
            self._total_cookies -= cost
            
        
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """
    item_class = build_info.clone()
    game_class = ClickerState()
    # print game_class.get_time() # temp
    game_time = game_class.get_time()
    
    while duration >= game_time:
            
        
        item = strategy(game_class.get_cookies(),
                      game_class.get_cps(),
                      game_class.get_history(),
                      duration - game_class.get_time(),
                      item_class)    
        if item == None:
            game_class.wait( duration - game_time )
            break 
            
        item_cost = item_class.get_cost(item)
        item_cps = item_class.get_cps(item)
        wait_time = game_class.time_until( item_cost )
        
        if duration - game_time >= wait_time: 
            #print game_time, item, item_cost, duration
            game_class.wait( wait_time )
            game_class.buy_item( item, item_cost, item_cps )
            item_class.update_item( item )
            game_time = game_class.get_time()
            
        else:
            game_class.wait( duration - game_time )
            game_time = game_class.get_time() 
            break
        
    return game_class


def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    item_class = build_info.clone()
    ava_item = build_info.build_items()
    item_cost = []
    
    for ele in ava_item:
        item_cost.append( item_class.get_cost(ele) )
        
    min_cost = min(item_cost)
    if cookies + time_left * cps >= min_cost:
        item = ava_item[ item_cost.index(min_cost) ]
    else:
        item = None
     
    return item
        

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    item_class = build_info.clone()
    ava_item = build_info.build_items()
    item_cost = []
    item = None
    for ele in ava_item:
        item_cost.append( item_class.get_cost(ele) )
        
    possible_cookies = cookies + time_left * cps
    
    
    for idx in range(len(item_cost)):
        if item_cost[idx] <= possible_cookies:
            item = ava_item[ idx ]   
    return item   
        
    
      
        

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    item_class = build_info.clone()
    ava_item = build_info.build_items()
    cps_cost = []
    aff_item = []
    
    possible_cookies = cookies + time_left * cps
    
    
    for ele in ava_item:
        if item_class.get_cost(ele) <= possible_cookies:
            aff_item.append(ele)
            cps_cost.append( item_class.get_cps(ele) / item_class.get_cost(ele))
    
    if aff_item != []:
        
        idx_max_cps_cost = cps_cost.index( max(cps_cost) )
        item = aff_item[idx_max_cps_cost]
    
    else:
        
        item = None 
    return item 
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    # history = state.get_history()
    # history = [(item[0], item[3]) for item in history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    run_strategy("Cursor", SIM_TIME, strategy_none)
   
    # Add calls to run_strategy to run additional strategies
    run_strategy("Cheap", SIM_TIME, strategy_cheap)
    run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)
    
run()

