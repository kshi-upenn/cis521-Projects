
#!/usr/bin/env python
from ants import *
from random import shuffle

class MBot():
    def do_turn(self, ants):
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
                    if (new_loc in ants.enemy_ants()):
                        break #too close to action, stop bfsing for food
                    if (new_loc in ants.myants()):
                        ants.issue_order(new_loc, directions[3 - directions.index(direction)])
                        food_ants.append(new_loc)
                        ant_found = True                        
                    elif (ants.passable(new_loc)):
                        q.put(new_loc)

        destinations = []
        for a_row, a_col in ants.my_ants():
            if (a_row,a_col) not in food_ants:
                # try all directions randomly until one is passable and not occupied
                directions = AIM.keys()
                shuffle(directions)
                for direction in directions:
                    (n_row, n_col) = ants.destination(a_row, a_col, direction)
                    if (not (n_row, n_col) in destinations and
                            ants.passable(n_row, n_col)):
                        ants.issue_order((a_row, a_col, direction))
                        destinations.append((n_row, n_col))
                        break
                else:
                    destinations.append((a_row, a_col))


if __name__ == '__main__':
    try:
        import psyco
        psyco.full()
    except ImportError:
        pass
    try:
        Ants.run(MBot())
    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')
