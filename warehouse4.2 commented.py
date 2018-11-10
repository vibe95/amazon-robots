#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the warehouse domain.  

'''
warehouse STATESPACE 
'''
#   You may add only standard python imports---i.e., ones that are automatically
#   available on CDF.
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

from search import *
from random import randint

##################################################
# The search space class 'warehouse'             #
# This class is a sub-class of 'StateSpace'      #
##################################################

class warehouse(StateSpace):
    def __init__(self, action, gval, products, stations, current_time, open_orders, robots, parent = None):
#IMPLEMENT
        """Initialize a warehouse search state object."""
        StateSpace.__init__(self, action, gval, parent)       #intialize the state space
        
        #initialize the time to 0 and the products, stations, orders, robots, current time to given values 
        self.products = products
        self.stations = stations
        self.current_time = current_time
        self.open_orders = open_orders
        self.robots = robots

       
    def successors(self): 
        #IMPLEMENT
        '''Return list of warehouse objects that are the successors of the current object'''
        
        #Function to get new robot and order lists after an deliver action is called
        def change_robots(self,robo_count,order_count,robo_loc):
            
            #copy current order, robots list and make a new list for new orders
            current_order = self.open_orders[order_count] 
            robots = self.robots[:]            
            new_orders = []
            
            #find order's, product location and save location in prod_loc
            for product in self.products:
                if (product[0] == current_order[0]):
                    prod_loc = product[1]
            
            #look for the correct station
            for station in self.stations:   
                if (current_order[1] == station[0]):
                    station_loc = station[1]
            
            #change current robot to do this job
            distance = abs(robo_loc[0]-prod_loc[0]) + abs(robo_loc[1]-prod_loc[1]) + abs(station_loc[0]-prod_loc[0]) +  abs(station_loc[1]-prod_loc[1]) + self.gval
            robots[robo_count]=[robots[robo_count][0],"on_delivery",station[1],distance]
            
            #remove order from open_order list 
            for order in self.open_orders:
                if order != current_order:
                    new_orders.append(order)
                    
            return (robots,new_orders)     
        
        #iniatilize possible states list, a counter for robot in list and a varaible on_delivery_time (which stores the smallest delivery time)
        possible_states = []
        robo_count = 0
        on_delivery_time = 11111111111
        
        #Check if robot idle; if so give it a job, if not move time forward so they will finish
        for robo in self.robots:    #go through all the robots
            if (robo[1]=='idle'):   #if robot is idle assign it a job and add that path to possible states
                order_count = 0     #counter for where in order list
                for order in self.open_orders:  #go through all the jobs to find all combos with this robot
                    action ="deliver("+ robo[0]+","+ order[0]+"," + order[1]+")"        #save the action
                    changes = change_robots(self, robo_count, order_count,robo[2])      #save out from the fucntion changes
                    possible_states.append (warehouse(action, (self.gval), self.products, self.stations, self.current_time, changes[1], changes[0], self)) #add to states list
                    order_count=order_count+1
                    
            elif (robo[1] == 'on_delivery'):    # if the robot is on delivery just increase time and gval to point when it finshes 
                if (robo[3] < on_delivery_time):                    # if this the first robot to finsh then save it to updated robotlist
                    action1 ="move_forward("+ str(robo[3])+")"      #save action
                    on_delivery_time = robo[3]                      
                    new_robots = self.robots[:]
                    robo_delivery = robo[3]                    
                    new_robots[robo_count] = [robo[0],'idle',robo[2]]      #save that robots updated info to the new robot list
                elif (robo[3] == on_delivery_time):                         #case where this robot also has the lowest time then add it's changes to the list too
                    action1 ="move_forward("+ str(robo[3])+")"                    
                    new_robots = new_robots[:]
                    new_robots[robo_count] = [robo[0],'idle',robo[2]]
                
            robo_count=robo_count+1
            
        #only add states with action move_forward by checking if deilivery time has changed      
        if (on_delivery_time != 11111111111):
            possible_states.append (warehouse(action1, (robo_delivery), self.products, self.stations, (robo_delivery), self.open_orders, new_robots, self))        
         
        return possible_states
    

    def hashable_state(self):
        #IMPLEMENT
        '''Return a data item that can be used as a dictionary key to UNIQUELY represent the state.'''
        
        # Generates a unique tuple with the gval in the first spot and the time to completion of each robot in the other slots
        unique_list = [self.gval]   #add gval to list
        for robo in self.robots:    #add each robots time to completion into the list 
            if (robo[1] == 'idle'):
                unique_list.append(0)      
            else:
                unique_list.append(robo[3])
            
        return tuple(unique_list)
            
        # how many
    def print_state(self):
        #DO NOT CHANGE THIS FUNCTION---it will be used in auto marking
        #and in generating sample trace output. 
        #Note that if you implement the "get" routines below properly, 
        #This function should work irrespective of how you represent
        #your state. 

        if self.parent:
            print("Action= \"{}\", S{}, g-value = {}, (From S{})".format(self.action, self.index, self.gval, self.parent.index))
        else:
            print("Action= \"{}\", S{}, g-value = {}, (Initial State)".format(self.action, self.index, self.gval))
            
        print("Time = {}".format(self.get_time()))
        print("Unfulfilled Orders")
        for o in self.get_orders():
            print("    {} ==> {}".format(o[0], o[1]))
        print("Robot Status")
        for rs in self.get_robot_status():
            print("    {} is {}".format(rs[0], rs[1]), end="")
            if rs[1] == 'idle':
                print(" at location {}".format(rs[2]))
            elif rs[1] == 'on_delivery':
                print(" will be at location {} at time {}".format(rs[2], rs[3]))

#Data accessor routines.

    def get_robot_status(self):
        #IMPLEMENT
            
        '''Return list containing status of each robot
           This list has to be in the format: [rs_1, rs_2, ..., rs_k]
           with one status list for each robot in the state. 
           Each robot status item rs_i is itself a list in the format [<name>, <status>, <loc>, <ftime>]
           Where <name> is the name of the robot (a string)
                 <status> is either the string "idle" or the string "on_delivery"
                 <loc> is a location (a pair (x,y)) 
                       if <status> == "idle" then loc is the robot's current location
                       if <status> == "on_delivery" then loc is the robot's future location
                <ftime> 
                       if <status> == "idle" this item is missing (i.e., the list is of 
                                      length 3)
                       if <status> == "on_delivery" then this is a number that is the 
                                      time that the robot will complete its current delivery
        '''
        return self.robots

    def get_time(self):
        #IMPLEMENT
        '''Return the current time of this state (a number)'''
        return self.current_time

    def get_orders(self):
        #IMPLEMENT
        '''Return list of unfulfilled orders of this state
           This list is in the format [o1, o2, ..., om]
           one item for each unfulfilled order. 
           Each oi is itself a list [<product_name>, <packing_station_name>]
           where <product_name> is the name of the product to be delivered
           and  <packing_station_name> is the name of the packing station it is to be delivered to'''
        return self.open_orders

#############################################
# heuristics                                #
#############################################
    
def heur_zero(state):
    '''Zero Heuristic use to make A* search perform uniform cost search'''
    return 0

def heur_min_completion_time(state):
    #IMPLEMENT
    '''warehouse heuristic'''
    #We want an admissible heuristic. Since the aim is to delivery all
    #of the products to their packing station in as short as a time as
    #possible. 
    #NOTE that we want an estimate of the ADDED time beyond the current
    #     state time.
    #Consider all of the possible delays in moving from this state to
    #a final delivery of all orders.
    # 1. All robots have to finish any current delivery they are on.
    #    So the earliest we could finish is the 
    #    maximum over all robots on delivery of 
    #       (robot's finish time - the current state time)
    #    we subtract the current state time because we want time
    #    beyond the current time required to complete the delivery
    #    Let this maximum be TIME1.
    #    Clearly we cannot finish before TIME1
    #
    # 2. For all unfulfilled orders we need to pick up the product of
    #    that order with some robot, and then move it to the right
    #    packing station. However, we could do many of these
    #    deliveries in parallel. So to get an *admissible* heuristic
    #    we take the MAXIMUM of a MINUMUM time any unfulfilled order
    #    can be completed. There are many different minimum times that
    #    could be computed...of varying complexity. For simplicity we
    #    ignore the time required to get a robot to package, and
    #    instead take the time to move the package from its location
    #    to the packing station location as being a suitable minimum.
    #    So we compute these minimums, then take the maximum of these
    #    minimums Call this max TIME2
    #    Clearly we cannot finish before TIME2
    #
    # Finally we return as a the heuristic value the MAXIMUM of ITEM1 and ITEM2

    #stores a list of times for robots to complete and time to go from package to station
    list_of_times =[]
    
    #store robot completion times
    for robo in state.robots:
        if (robo[1] == 'idle'):     #idle case time to completion is 0
            list_of_times.append(0)
        else:
            list_of_times.append(robo[3])
            
    #go through open orders and find the product and station location and save the distance (i.e. time) into the list of times        
    for order in state.open_orders:
        for product in state.products:  #find product
            if (product[0] == order[0]):
                prod_loc = product[1]

        for station in state.stations:  # find station
            if (order[1] == station[0]):
                station_loc = station[1]
                
        distance = abs(station_loc[0]-prod_loc[0]) +  abs(station_loc[1]-prod_loc[1])   #find distance between product and station
        list_of_times.append(distance)  #append that list to distance 
        
    if (len(list_of_times) == 0): #if list is empty then 0 is the max
        return 0
    else:   #return the max of all the times in the list
        return max(list_of_times)
        
    
        
def warehouse_goal_fn(state):
#IMPLEMENT
    
    '''Have we reached the goal when all orders have been delivered. Returns 
    true if all order of current state are done else it return false'''
    completion = 0 # if completion is equal to (1+num of robots) then robots have finshed and orders are done
    
    #check if all orders are done if so increase completion by 1
    if (len(state.open_orders) == 0):
        completion  += 1
        
    # check if all robots are idle if so increase completion by 1 for each idle robot
    for robo in state.robots:
        if (robo[1] == 'idle'):
            completion  += 1
            
    if (completion == len(state.robots)+1):    # check if orders are done and robots are idle if so return True, else return false
        return True
    else:
        return False
            
    

def make_init_state(product_list, packing_station_list, current_time, open_orders, robot_status):
#IMPLEMENT
    '''Input the following items which specify a state and return a warehouse object 
       representing this initial state.
         The state's its g-value is zero
         The state's parent is None
         The state's action is the dummy action "START"
       product_list = [p1, p2, ..., pk]
          a list of products. Each product pi is itself a list
          pi = [product_name, (x,y)] where 
              product_name is the name of the product (a string) and (x,y) is the
              location of that product.
       packing_station = [ps1, ps2, ..., psn]
          a list of packing stations. Each packing station ps is itself a list
          pi = [packing_station_name, (x,y)] where 
              packing_station_name is the name of the packing station (a string) and (x,y) is the
              location of that station.
       current_time = an integer >= 0
          The state's current time.
       open_orders = [o1, o2, ..., om] 
          a list of unfulfilled (open) orders. Each order is itself a list
          oi = [product_name, packing_station_name] where
               product_name is the name of the product (a string) and
               packing_station_name is the name of the packing station (a string)
               The order is to move the product to the packing station
        robot_status = [rs1, rs2, ..., rsk]
          a list of robot and their status. Each item is itself a list  
          rsi = ['name', 'idle'|'on_delivery', (x, y), <finish_time>]   
            rsi[0] robot name---a string 
            rsi[1] robot status, either the string "idle" or the string
                  "on_delivery"
            rsi[2] robot's location--if "idle" this is the current robot's
                   location, if "on_delivery" this is the robots final future location
                   after it has completed the delivery
            rsi[3] the finish time of the delivery if the "on_delivery" 
                   this element of the list is absent if robot is "idle" 

   NOTE: for simplicity you may assume that 
         (a) no name (robot, product, or packing station is repeated)
         (b) all orders contain known products and packing stations
         (c) all locations are integers (x,y) where both x and y are >= 0
         (d) the robot status items are correctly formatted
         (e) the future time for any robot on_delivery is >= to the current time
         (f) the current time is >= 0
             def __init__(self, action, gval, products, stations, current_time, open_orders, robots, parent = None):

    '''
    #use the variables given and run a new warehouse object and return it 
    current_warehouse = warehouse("START", 0, product_list, packing_station_list, current_time, open_orders, robot_status)
    return current_warehouse
########################################################
#   Functions provided so that you can more easily     #
#   Test your implementation                           #
########################################################

def make_rand_init_state(nprods, npacks, norders, nrobots):
    '''Generate a random initial state containing 
       nprods = number of products
       npacks = number of packing stations
       norders = number of unfulfilled orders
       nrobots = number of robots in domain'''

    prods = []
    for i in range(nprods):
        ii = int(i)
        prods.append(["product{}".format(ii), (randint(0,50), randint(0,50))])
    packs = []
    for i in range(npacks):
        ii = int(i)
        packs.append(["packing{}".format(ii), (randint(0,50), randint(0,50))])
    orders = []
    for i in range(norders):
        orders.append([prods[randint(0,nprods-1)][0], packs[randint(0,npacks-1)][0]])
    robotStatus = []
    for i in range(nrobots):
        ii = int(i)
        robotStatus.append(["robot{}".format(ii), "idle", (randint(0,50), randint(0,50))])
    return make_init_state(prods, packs, 0, orders, robotStatus)


def test(nprods, npacks, norders, nrobots):
    s0 = make_rand_init_state(nprods, npacks, norders, nrobots)
    se = SearchEngine('astar', 'full')
    #se.trace_on(2)
    final = se.search(s0, warehouse_goal_fn, heur_min_completion_time)
