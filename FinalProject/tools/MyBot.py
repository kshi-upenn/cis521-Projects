#!/usr/bin/env python
from ants import *
from Queue import Queue

# define a class with a do_turn method
# the Ants.run method will parse and update bot input
# it will also run the do_turn method for us
class MyBot:
    def __init__(self):
        # define class level variables, will be remembered between turns
        pass
    
    # do_setup is run once at the start of the game
    # after the bot has received the game settings
    # the ants class is created and setup by the Ants.run method
    def do_setup(self, ants):
        # initialize data structures after learning the game settings
        pass
    
    # do turn is run once per turn
    # the ants class has the game state and is updated by the Ants.run method
    # it also has several helper methods to use
    def do_turn(self, ants):

        fighting_ants = []
        #do alpha-beta pruning for ants near enemy ants
        for enemy_ant in ants.enemy_ants():
            #find nearby friendly ants
            q = Queue()
            q.put(enemy_ant)
            while (not q.empty()):
                loc = q.get()
                directions = ('n','e','w','s')
                for direction in directions:
                    new_loc = ants.destination(loc, direction)
                    if (new_loc in ants.my_ants):
                        fightng_ants.append(new_loc)
                    if (ants.distance(new_loc, enemy_ant) < 5):
                        q.put(new_loc)

        #pick groups of fighting ants
        while (not fighting_ants.empty()):
            


        #do BFS for food
        food_ants = []
        for food_loc in ants.food():
            ant_found = False
            q = Queue()
            q.put(food_loc)
            while (not q.empty() and not ant_found):
                loc = q.get()
                directions = ('n','e','w','s')
                for direction in directions:
                    new_loc = ants.destination(loc, direction)                    
                    if (new_loc in ants.enemy_ants):
                        break #too close to action, stop bfsing for food
                    elif (new_loc in ants.myants()):
                        ants.issue_order(new_loc, directions[3 - directions.index(direction)])
                        ant_found = True                        
                    elif (ants.passable(new_loc)):
                        q.put(new_loc)
            


        # loop through all ants not assigned to food/fighting and give exploration orders
        # the ant_loc is an ant location tuple in (row, col) form
        for (ant_loc in ants.my_ants() and not in fighting_ants and not in food_ants):
            # try all directions in given order
            directions = ('n','e','s','w')
            for direction in directions:
                # the destination method will wrap around the map properly
                # and give us a new (row, col) tuple
                new_loc = ants.destination(ant_loc, direction)
                # passable returns true if the location is land
                if (ants.passable(new_loc)) and (ants.unoccupied(new_loc) and new_loc not in orders):
                    # an order is the location of a current ant and a direction
                    ants.issue_order((ant_loc, direction))
                    # stop now, don't give 1 ant multiple orders
                    break
            # check if we still have time left to calculate more orders
            if ants.time_remaining() < 10:
                break
            
if __name__ == '__main__':
    # psyco will speed up python a little, but is not needed
    try:
        import psyco
        psyco.full()
    except ImportError:
        pass
    
    try:
        # if run is passed a class with a do_turn method, it will do the work
        # this is not needed, in which case you will need to write your own
        # parsing function and your own game state class
        Ants.run(MyBot())
    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')
