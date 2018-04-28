# -*- coding: utf-8 -*-
"""
Created on  Feb 27 2018

@author: frederic

Scaffholding code for CAB320 Assignment One

This is the only file that you have to modify and submit for the assignment.

"""

import numpy as np

import itertools

import generic_search as gs

from assignment_one import (TetrisPart, AssemblyProblem, offset_range, 
                            display_state, 
                            make_state_canonical, play_solution, 
                            load_state, make_random_state
                            )

# ---------------------------------------------------------------------------

def print_the_team():                                                   #DONE
    '''
    Print details of the members of your team 
    (full name + student number)
    '''
    
    print("Team 095:")
    print('Mackenzie Wilson, 10155856')
    print('Nicole Barritt, 10157182')
    
# ---------------------------------------------------------------------------
        
def appear_as_subpart(some_part, goal_part):                            #DONE
    '''    
    Determine whether the part 'some_part' appears in another part 'goal_part'.
    
    Formally, we say that 'some_part' appears in another part 'goal_part',
    when the matrix representation 'S' of 'some_part' is a a submatrix 'M' of
    the matrix representation 'G' of 'goal_part' and the following constraints
    are satisfied:
        for all indices i,j
            S[i,j] == 0 or S[i,j] == M[i,j]
            
    During an assembly sequence that does not use rotations, any part present 
    on the workbench has to appear somewhere in a goal part!
    
    @param
        some_part: a tuple representation of a tetris part (a list of lists)
        goal_part: a tuple representation of another tetris part
        
    @return
        True if 'some_part' appears in 'goal_part'
        False otherwise    
    '''
    #assumption: we dont care how many times the part appears, just if.
    s = np.array(some_part)  # HINT
    g = np.array(goal_part)

    
    #assert that not all of s is zero
    
    h = s.shape[0]
    w = s.shape[1]
    
    
    num_y_pos = g.shape[-2] - (h - 1) # number of positions in this dimension to try (reps)
    num_x_pos = g.shape[-1] - (w - 1)


    #for all subparts (M) of G that are the same size as S
    for i in range(num_y_pos):
        for j in range(num_x_pos):
            # Sometimes goal parts have 3 dimensions, sometimes 2
            # If it only has one part, it will be passed directly and 
            #   will have 3 dimensions. 
            if g.ndim == 3:
                m = g[:,i:i+h, j:j+w]
            elif g.ndim ==2:
                m = g[i:i+h, j:j+w]
            else:
                assert(False)
            #print("\nSubpart: \n", m) #debug
            
            # if the part identical to this portion of the goal or 0, TRUE
            if ( (np.logical_or(s==m,s==0)).all() ): 
                return True
    
    # no identical part found, FALSE
    return False
        


# ---------------------------------------------------------------------------
        
def cost_rotated_subpart(some_part, goal_part):                         #DONE
    '''    
    Determine whether the part 'some_part' appears in another part 'goal_part'
    as a rotated subpart. If yes, return the number of 'rotate90' needed, if 
    no return 'np.inf'
    
    The definition of appearance is the same as in the function 
    'appear_as_subpart'. -> call this function for all rotations of some_part
                   
    @param
        some_part: a tuple representation of a tetris part
        goal_part: a tuple representation of another tetris part
    
    @return
        the number of rotation needed to see 'some_part' appear in 'goal_part'
            0, 1, 2, 3 or infinity (np.inf)
        np.inf  if no rotated version of 'some_part' appear in 'goal_part'
    
    '''
    
    #USING HIS METHOD
    # Make a tetris part of all parts, rotate some part n times, test 
    # appear_as_subpart for each rotation, if true return n. If all rotations 
    # tested and returned false, return inf because no solution. 
    sp = TetrisPart(some_part)
    gp = TetrisPart(goal_part)
    
    
    for num_rot in range(0,4):
        if appear_as_subpart(sp.get_frozen(), gp.get_frozen()):
            return num_rot
        sp.rotate90()
    
    return np.inf
    
    
# ---------------------------------------------------------------------------

class AssemblyProblem_1(AssemblyProblem):                               #DONE
    '''
    
    Subclass of 'assignment_one.AssemblyProblem'
    
    * The part rotation action is NOT available for AssemblyProblem_1 *

    The 'actions' method of this class simply generates
    the list of all legal actions. The 'actions' method of this class does 
    *NOT* filter out actions that are doomed to fail. In other words, 
    no pruning is done in the 'actions' method of this class.
        
    '''

    def __init__(self, initial, goal=None):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal.  Your subclass's constructor can add
        other arguments."""
        # Call the parent class constructor.
        # Here the parent class is 'AssemblyProblem' 
        # which itself is derived from 'generic_search.Problem'
        super(AssemblyProblem_1, self).__init__(initial, goal, use_rotation=False)
    
    def actions(self, state):                                           #DONE
        """
        Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once.
        
        @param
          state : a state of an assembly problem.
        
        @return i
           the list of all legal drop actions available in the 
            state passed as argument.   
           the individual actions are tuples, contained in a list. 
        """
        # EACH COMBINATOIN OF 2 PARTS IS AN ACTION
        # EACH COMBINATION CAN EXIST IN ONE OF TWO ORDERS 
        # EACH COMBINATION CAN EXIST WITH OFFSETS IN ALLOWABLE RANGE
        # RETURN AS A LIST OF TUPLES: (pa, pu, offset)
        actions = []
        part_list = list(make_state_canonical(state))  #    HINT
        
        #cemetary:
        for u in range(0, len(part_list)): #under
            for a in range(0, len(part_list)): #above
                if u != a: # check index isnt the same, because actual part can be
                    pa = part_list[a]
                    pu = part_list[u]
                    offsets = offset_range(pa, pu)
                    for o in range(offsets[0], offsets[1]):
                        new_part = TetrisPart(pa,pu,o)
                        # No pruning, but check for valid offset value
                        if new_part.offset is not None:
                            actions.append((pa, pu, o)) #tuple
        '''
                            
        # using itertools -> SLOWER, didnt use. 
        for part1, part2 in itertools.combinations(part_list, 2):
            for pa, pu in itertools.permutations((part1, part2)):
                offsets = offset_range(pa, pu)
                for o in range(offsets[0], offsets[1]):
                    new_part = TetrisPart(pa,pu,o)
                    # Ensure valid offset value
                    if new_part.offset is not None:
                        actions.append((pa,pu,o)) #tuple
        '''
        return actions
        #returns empty list if the state has no parts


    def result(self, state, action):                                    #DONE
        """
        Return the state (as a tuple of parts in canonical order)
        that results from executing the given
        action in the given state. The action must be one of
        self.actions(state).

        Actions are just drops.
        
        @return
          a state in canonical order
        """
        # USE THE ACTION GIVEN TO MAKE A NEW PART FROM PU AND PA
        # REMOVE PA AND PU FROM STATE, REPLACE WITH NEW PART
        # COMPUTE AND RETURN NEW STATE
        assert(action in self.actions(state)) #defense 
        
        pa, pu, offset = action # HINT
        new_part = TetrisPart(pa,pu,offset) #was checked as valid before
        new_part_tuple = new_part.get_frozen()
        part_list = list(state)
        part_list.remove(pu)
        part_list.remove(pa)
        part_list.append(new_part_tuple)
        
        return make_state_canonical(part_list) #tuple, in canonical order


# ---------------------------------------------------------------------------

class AssemblyProblem_2(AssemblyProblem_1):                             #DONE
    '''
    
    Subclass of 'assignment_one.AssemblyProblem'
        
    * Like for AssemblyProblem_1,  the part rotation action is NOT available 
       for AssemblyProblem_2 *

    The 'actions' method of this class  generates a list of legal actions. 
    But pruning is performed by detecting some doomed actions and 
    filtering them out.  That is, some actions that are doomed to 
    fail are not returned. In this class, pruning is performed while 
    generating the legal actions.
    However, if an action 'a' is not doomed to fail, it has to be returned. 
    In other words, if there exists a sequence of actions solution starting 
    with 'a', then 'a' has to be returned.
        
    '''

    def __init__(self, initial, goal=None):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal.  Your subclass's constructor can add
        other arguments."""
        # Call the parent class constructor.
        # Here the parent class is 'AssemblyProblem' 
        # which itself is derived from 'generic_search.Problem'
        super(AssemblyProblem_2, self).__init__(initial, goal)
    
    def actions(self, state):                                           #DONE
        """
        Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once.
        
        A candidate action is eliminated if and only if the new part 
        it creates does not appear in the goal state.

        Actions are just drops
        """
        # EACH COMBINATOIN OF 2 PARTS IS AN ACTION
        # EACH COMBINATION CAN EXIST IN ONE OF TWO ORDERS 
        # EACH COMBINATION CAN EXIST WITH OFFSETS IN ALLOWABLE RANGE
        # RETURN ACTIONS AS A TUPLE: (pa, pu, offset)
        actions = []
        part_list = list(make_state_canonical(state))  #    HINT
        for part1, part2 in itertools.combinations(part_list, 2):
            for pa, pu in itertools.permutations((part1, part2)):
                offsets = offset_range(pa, pu)
                for o in range(offsets[0], offsets[1]):
                    new_part = TetrisPart(pa,pu,o)
                    # Check valid offset and not a duplicate
                    if (new_part.offset is not None and (pa, pu, o) not in actions):
                        # P R U N I N G
                        # Check new part exists in goal, and action is unique
                        for part in self.goal:
                            if appear_as_subpart(new_part.get_frozen(), part):
                                actions.append((pa, pu, o)) #tuple
                                break #do not keep checking and appending
                    
        return actions
        #returns empty list if the state has no parts


# ---------------------------------------------------------------------------

class AssemblyProblem_3(AssemblyProblem_1):                             #DONE
    '''
    
    Subclass 'assignment_one.AssemblyProblem'
    
    * The part rotation action is available for AssemblyProblem_3 *

    The 'actions' method of this class simply generates
    the list of all legal actions including rotation. 
    The 'actions' method of this class does 
    *NOT* filter out actions that are doomed to fail. In other words, 
    no pruning is done in this method.
        
    '''

    def __init__(self, initial, goal=None):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal.  Your subclass's constructor can add
        other arguments."""
        # Call the parent class constructor.
        # Here the parent class is 'AssemblyProblem' 
        # which itself is derived from 'generic_search.Problem'
        super(AssemblyProblem_3, self).__init__(initial, goal)
        self.use_rotation = True

    
    def actions(self, state):                                           #DONE
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once.
        
        Rotations are allowed, but no filtering out the actions that 
        lead to doomed states.
        
        """
        # EACH COMBINATION OF 2 PARTS AND AN OFFSET, OR 
            # A PART AND A ROTATION IS AN ACTION
        # EACH DROP CAN EXIST WITH OFFSETS IN ALLOWABLE RANGE
        # RETURN LIST OF TUPLES: (pa, pu, offset) or (part, rotation)
        actions = []
        part_list = list(make_state_canonical(state))  #    HINT
        for u in range(0, len(part_list)): #under
            for a in range(0, len(part_list)): #above
                if u == a: # APPEND A ROTATION
                    p = part_list[u]
                    for rot in range(1,4):
                        actions.append((p, rot))
                else: # APPEND A DROP
                    pa = part_list[a]
                    pu = part_list[u]
                    offsets = offset_range(pa, pu)
                    for o in range(offsets[0], offsets[1]):
                        new_part = TetrisPart(pa,pu,o)
                        # No pruning, but check valid offset value
                        if new_part.offset is not None:
                            actions.append((pa, pu, o)) #tuple
                    
        return actions
        #returns empty list if the state has no parts


        
    def result(self, state, action):                                    #DONE
        """
        Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state).

        The action can be a drop or rotation.        
        """
        # Here a workbench state is a frozenset of parts        
        assert(action in self.actions(state)) #defense 

        part_list = list(make_state_canonical(state))
        
        if len(action)==2: #THIS IS A ROTATION
            part, offset = action
            num_rot = offset
            assert (num_rot in range(1,4)) #defense
            
            # ROTATE PART NUM_ROT TIMES 90 DEGREES 
            # REMOVE PART FROM PART LIST 
            # APPEND ROTATED PART TO PART LIST
            new_part = TetrisPart(part)
            for i in range(0, num_rot):
                new_part.rotate90()
    
            new_part_tuple = new_part.get_frozen() 
            part_list.remove(part)
            part_list.append(new_part_tuple)
            
            
        elif len(action) == 3: # THIS IS A DROP
            # USE THE ACTION GIVEN TO MAKE A NEW PART FROM PU AND PA
            # REMOVE PA AND PU FROM STATE, REPLACE WITH NEW PART
            # COMPUTE AND RETURN NEW STATE
            pa, pu, offset = action
            new_part = TetrisPart(pa,pu,offset)
            new_part_tuple = new_part.get_frozen()
            part_list.remove(pu)
            part_list.remove(pa)
            part_list.append(new_part_tuple)
            
        return part_list
        


# ---------------------------------------------------------------------------

class AssemblyProblem_4(AssemblyProblem_3):                           #DONE
    '''
    
    Subclass 'assignment_one.AssemblyProblem3'
    
    * Like for its parent class AssemblyProblem_3, 
      the part rotation action IS available for AssemblyProblem_4  *

    AssemblyProblem_4 introduces a simple HEURISTIC function and uses
    action filtering. -> PRUNING
    See the details in the methods 'self.actions()' and 'self.h()'.
    
    '''

    def __init__(self, initial, goal=None):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal.  Your subclass's constructor can add
        other arguments."""
        # Call the parent class constructor.
        # Here the parent class is 'AssemblyProblem' 
        # which itself is derived from 'generic_search.Problem'
        super(AssemblyProblem_4, self).__init__(initial, goal)

    def actions(self, state):                                       #DONE
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once.
        
        Filter out actions (drops and rotations) that are doomed to fail 
        using the function 'cost_rotated_subpart'.
        A candidate action is eliminated if and only if the new part 
        it creates does not appear in the goal state.
        This should  be checked with the function "cost_rotated_subpart()'.
                
        """
        # EACH COMBINATION OF 2 PARTS AND AN OFFSET, OR 
            # A PART AND A ROTATION IS AN ACTION
        # EACH DROP CAN EXIST WITH OFFSETS IN ALLOWABLE RANGE
        # EACH ROTATION CAN EXIST WITH ROTATIONS 1, 2, OR 3 
        # RETURN LIST OF TUPLES: (pa, pu, offset) or (part, rotation)
        actions = []
        part_list = list(make_state_canonical(state))  #    HINT
        for u in range(0, len(part_list)): #under
            for a in range(0, len(part_list)): #above
                if u == a:                  # APPEND A ROTATION
                    p = part_list[u]
                    t = TetrisPart(p)
                    # P R U N I N G
                    # FOR EVERY POSSIBLE ROTATION (NOT 0), CHECK IF ROTATED
                        # PART APPEARS IN GOAL AND IS UNIQUE
                        # IF YES, APPEND ACTION WITH THAT ROTATION
                    for r in range(1,4):
                        t.rotate90()
                        for part in self.goal:
                            if (appear_as_subpart(t.get_frozen(), part) 
                                and (p,r) not in actions):
                                actions.append((p,r))
                                break #do not keep appending
                       
                        
                        
                else:                       # APPEND A DROP
                    pa = part_list[a] # u!= a
                    pu = part_list[u]
                    offsets = offset_range(pa, pu)
                    for o in range(offsets[0], offsets[1]):
                        # P R U N I N G
                        # COMPUTE NEW PART
                        # IF NEW PART EXISTS IN GOAL, APPEND THE ACTION
                        # ROTATION IS ALLOWED (COST != INF)
                        new_part = TetrisPart(pa,pu,o)
                        if (new_part.offset is not None and (pa, pu, o) not in actions):
                            # P R U N I N G
                            # NEW PART EXISTS IN GOAL (C_R_S != INF)
                            for part in self.goal:
                                if (cost_rotated_subpart(new_part.get_frozen(), part) < 5):
                                    actions.append((pa, pu, o)) #tuple
                                    break #do not keep checking and appending
        
        return actions
        
        
        
    def h(self, n):                                             #DONE
        '''
        This heuristic computes the following cost; 
        
           Let 'k_n' be the number of parts of the state associated to node 'n'
           and 'k_g' be the number of parts of the goal state. (self.goal)
          
        The cost function h(n) must return 
            k_n - k_g + max ("cost of the rotations")  
        where the list of cost of the rotations is computed over the parts in 
        the state 'n.state' according to 'cost_rotated_subpart'.
        
        
        @param
          n : node of a search tree
          
        '''
        # Save current state and goal state as lists
        state_list = list(make_state_canonical(n.state))
        #state_list = n
        goal_list = list(make_state_canonical(self.goal))
        
        # Num parts is the length of the state lists
        k_n = len(state_list)
        print(k_n)
        k_g = len(goal_list)
        print(k_g)
                 
        # For all the parts in current state, get the cost_rotated_subpart
        r_costs = [] #make it a list, and append as we calculate
        for i in range(0, k_g): # for all the goal parts
            for j in range(0, k_n): # check all the current parts
                r_costs.append(cost_rotated_subpart(state_list[j], goal_list[i]))

        print(r_costs)
        return k_n - k_g + max(r_costs)
    
# ---------------------------------------------------------------------------
        
def solve_1(initial, goal):
    '''
    Solve a problem of type AssemblyProblem_1
    
    The implementation has to 
    - use an instance of the class AssemblyProblem_1
    - make a call to an appropriate functions of the 'generic_search" library
    
    @return
        - the string 'no solution' if the problem is not solvable
        - otherwise return the sequence of actions to go from state
        'initial' to state 'goal'
    
    '''

    print('\n++  busy searching in solve_1() ...  ++\n')
    ap1 = AssemblyProblem_1(initial, goal)
    ip = gs.InstrumentedProblem(ap1)
    
    # soln will be None for unreachable goal state
    # soln will be the goal node
    soln = gs.depth_first_graph_search(ip)
    print(ip)
    
    if soln is None: #No solution, unreachable goal state, or timed out
        return 'no solution'
    else: 
        i = 0
        for a in soln.solution():
            print("\n\nAction ", i+1)
            print(soln.solution()[i])
            i+=1
            
        return soln.solution() #see definition in Node documentation
        
# ---------------------------------------------------------------------------
        
def solve_2(initial, goal):
    '''
    Solve a problem of type AssemblyProblem_2
    
    The implementation has to 
    - use an instance of the class AssemblyProblem_2
    - make a call to an appropriate functions of the 'generic_search" library
    
    @return
        - the string 'no solution' if the problem is not solvable
        - otherwise return the sequence of actions to go from state
        'initial' to state 'goal'
    
    '''

    print('\n++  busy searching in solve_2() ...  ++\n')
    
    ap2 = AssemblyProblem_2(initial, goal)
    ip = gs.InstrumentedProblem(ap2)
    
    # soln will be None for unreachable goal state
    # soln will be the goal node
    soln = gs.depth_first_tree_search(ip)
    print(ip)
    
    if soln is None: #No solution, unreachable goal state, or timed out
        return 'no solution'
    else: 
        return soln.solution() #see definition in Node documentation
    
    

# ---------------------------------------------------------------------------
        
def solve_3(initial, goal):
    '''
    Solve a problem of type AssemblyProblem_3
    
    The implementation has to 
    - use an instance of the class AssemblyProblem_3
    - make a call to an appropriate functions of the 'generic_search" library
    
    @return
        - the string 'no solution' if the problem is not solvable
        - otherwise return the sequence of actions to go from state
        'initial' to state 'goal'
    
    '''

    print('\n++  busy searching in solve_3() ...  ++\n')
    ap3 = AssemblyProblem_3(initial, goal)
    ip = gs.InstrumentedProblem(ap3)
    
    # soln will be None for unreachable goal state
    # soln will be the goal node
    soln = gs.depth_first_graph_search(ip)
    print(ip)
    
    if soln is None: #No solution, unreachable goal state, or timed out
        return 'no solution'
    else: 
        return soln.solution() #see definition in Node documentation
    
# ---------------------------------------------------------------------------
        
def solve_4(initial, goal):
    '''
    Solve a problem of type AssemblyProblem_4
    
    The implementation has to 
    - use an instance of the class AssemblyProblem_4
    - make a call to an appropriate functions of the 'generic_search" library
    
    @return
        - the string 'no solution' if the problem is not solvable
        - otherwise return the sequence of actions to go from state
        'initial' to state 'goal'
    
    '''
    # USE INFORMED SEARCH, BECAUSE WE HAVE A HEURISTIC!
    
    
    print('\n++  busy searching in solve_4() ...  ++\n')
    ap4 = AssemblyProblem_4(initial, goal)
    ip = gs.InstrumentedProblem(ap4)
    
    # soln will be None for unreachable goal state
    # soln will be the goal node
    soln = gs.astar_graph_search(ip, ap4.h())
    print(ip)
    
    if soln is None: #No solution, unreachable goal state, or timed out
        return 'no solution'
    else: 
        return soln.solution() #see definition in Node documentation
        
# ---------------------------------------------------------------------------


    
if __name__ == '__main__':
    pass
    
