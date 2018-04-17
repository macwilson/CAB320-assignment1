# -*- coding: utf-8 -*-
"""
Created on  Feb 27 2018

@author: frederic

Scaffholding code for CAB320 Assignment One

This is the only file that you have to modify and submit for the assignment.

"""

import numpy as np

import itertools

import generic_search

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

    
    h = s.shape[0]
    w = s.shape[1]
    
    h_diff = g.shape[-2] - (h- 1) # number of positions in this dimension to try (reps)
    w_diff = g.shape[-1] - (w- 1)


    #for all subparts (M) of G that are the same size as S
    for i in range(h_diff):
        for j in range(w_diff):
            m = g[i:i+h, j:j+w]
            #print(m) #debug
            
            # if the part identical to this portion of the goal or 0, TRUE
            if ( (np.logical_or(s==m,s==0)).all() ): 
                return True
    
    # no identity found, FALSE
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
    sp = np.array(some_part)
    gp = np.array(goal_part)
    
#    print("entered") #debug
    

    for i in range(0,4):
#        print(i) #debug
#        print(sp) #debug
        # if appear_as_subpart after i rotations, return i
        if appear_as_subpart(np.rot90(sp, i),gp): 
            return i

        
    # no match regardless of rotation
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
        
        @return 
           the list of all legal drop actions available in the 
            state passed as argument.        
        """
        # EACH COMBINATOIN OF 2 PARTS IS AN ACTION
        # EACH COMBINATION CAN EXIST IN ONE OF TWO ORDERS 
        # EACH COMBINATION CAN EXIST WITH OFFSETS IN ALLOWABLE RANGE
        # RETURN ACTIONS AS A TUPLE: [pa, pu, offset]
        actions = []
        part_list = list(make_state_canonical(state))  #    HINT
        for u in range(0, len(part_list)): #under
            for a in range(0, len(part_list)): #above
                if u != a: # check index isnt the same, because actual part can be
                    pa = part_list[a]
                    pu = part_list[u]
                    offsets = offset_range(pa, pu)
                    for o in range(offsets[0], offsets[1]):
                        actions.append([pa, pu, o])
                    
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
        new_part = TetrisPart(pa,pu,offset)
        assert(new_part.offset is not None) #defense; no new part made here
        new_part_tuple = new_part.get_frozen()
        
        part_list = list(make_state_canonical(state))
        part_list.remove(pu)
        part_list.remove(pa)
        
        part_list.append(new_part_tuple)
        
        return part_list


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
        # RETURN ACTIONS AS A TUPLE: [pa, pu, offset]
        actions = []
        part_list = list(make_state_canonical(state))  #    HINT
        for u in range(0, len(part_list)): #under
            for a in range(0, len(part_list)): #above
                if u != a: # check index isnt the same, because actual part can be
                    pa = part_list[a]
                    pu = part_list[u]
                    offsets = offset_range(pa, pu)
                    for o in range(offsets[0], offsets[1]):
                        # P R U N I N G
                        # COMPUTE NEW PART
                        # IF NEW PART EXISTS IN GOAL, ADD ACTION TO RETURN
                        new_part = TetrisPart(pa,pu,o)
                        if((self.goal is None) or appear_as_subpart(new_part.get_frozen(), self.goal)):
                            actions.append([pa, pu, o])
                    
        return actions
        #returns empty list if the state has no parts


# ---------------------------------------------------------------------------

class AssemblyProblem_3(AssemblyProblem_1):
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

    
    def actions(self, state):
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once.
        
        Rotations are allowed, but no filtering out the actions that 
        lead to doomed states.
        
        """
        #

        raise NotImplementedError

        
    def result(self, state, action):
        """
        Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state).

        The action can be a drop or rotation.        
        """
        # Here a workbench state is a frozenset of parts        
 
        raise NotImplementedError


# ---------------------------------------------------------------------------

class AssemblyProblem_4(AssemblyProblem_3):
    '''
    
    Subclass 'assignment_one.AssemblyProblem3'
    
    * Like for its parent class AssemblyProblem_3, 
      the part rotation action is available for AssemblyProblem_4  *

    AssemblyProblem_4 introduces a simple heuristic function and uses
    action filtering.
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

    def actions(self, state):
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

        raise NotImplementedError
        
        
        
    def h(self, n):
        '''
        This heuristic computes the following cost; 
        
           Let 'k_n' be the number of parts of the state associated to node 'n'
           and 'k_g' be the number of parts of the goal state.
          
        The cost function h(n) must return 
            k_n - k_g + max ("cost of the rotations")  
        where the list of cost of the rotations is computed over the parts in 
        the state 'n.state' according to 'cost_rotated_subpart'.
        
        
        @param
          n : node of a search tree
          
        '''

        raise NotImplementedError

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
    raise NotImplementedError
    
    # assembly_problem = AssemblyProblem_1(initial, goal) # HINT
    

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
    raise NotImplementedError
    

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
    raise NotImplementedError
    
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

    #         raise NotImplementedError
    print('\n++  busy searching in solve_4() ...  ++\n')
    raise NotImplementedError
        
# ---------------------------------------------------------------------------


    
if __name__ == '__main__':
    pass
    
