

'''

A few functions to do some basic test on  your submission (file 'my_solver.py')

** Note that the markers will use many other examples to assess your code **



'''
import time
import numpy as np

import random

from assignment_one import (TetrisPart, AssemblyProblem, offset_range, display_state, 
                            make_state_canonical, play_solution, 
                            load_state, make_random_state)

from my_solver import (appear_as_subpart, cost_rotated_subpart,
                       AssemblyProblem_1, solve_1,
                       AssemblyProblem_2, solve_2,
                       AssemblyProblem_3, solve_3,
                       AssemblyProblem_4, solve_4
                       )


# ---------------------------------------------------------------------------

def test_appear_as_subpart(): #USER EDITED
    '''
    Test 'appear_as_subpart' function on some examples
    
    '''

    # no
    pa_1 =   ( (2, 2, 2),
             (0, 3, 0),
             (1, 2, 0))
    # yes
    pa_2 =   ( (2, 2, 2),
             (0, 2, 0),
             (1, 2, 0))

    # yes
    pa_3 =   ( (0, 2),
             (0, 2),
             (1, 1))
    
    # should be no
    pa_4 = ((0, 0),
            (0, 0),
            (9, 9))
    
    # yes
    pa_5 = ((0, 0, 0, 0, 2),
            (1, 1, 1, 1, 2))
    
    #no
    pa_6 = ((1, 0, 1, 2, 2),
            (1, 1, 1, 0, 2))

    pb =   ((9, 9, 9, 9, 9, 0, 0, 0),
   (0, 0, 0, 0, 1, 2, 2, 2),
   (0, 0, 0, 0, 1, 0, 2, 0),
   (0, 0, 1, 1, 1, 1, 2, 0),
   (0, 0, 0, 1, 0, 1, 1, 0))
    
#    pprint.pprint(pa)
#    pprint.pprint(pb)

    ta_1 = TetrisPart(pa_1) 
    ta_2 = TetrisPart(pa_2) 
    ta_3 = TetrisPart(pa_3) 
    ta_4 = TetrisPart(pa_4)
    ta_5 = TetrisPart(pa_5)
    ta_6 = TetrisPart(pa_6)
    tb = TetrisPart(pb)
    tb.display('\nPart b')
    ta_1.display('\nSubpart of part b?  No')
    ta_2.display('\nSubpart of part b?  Yes')
    ta_3.display('\nSubpart of part b?  Yes')
    ta_4.display('\nSubpart of part b?  No (without rotation)')
    ta_5.display('\nSubpart of part b?  Yes')
    ta_6.display('\nSubpart of part b?  No')


    test_passed =  (  
            appear_as_subpart(pa_2, pb)
            and 
            appear_as_subpart(pa_3, pb)
            and 
            appear_as_subpart(pa_5, pb)
            and 
            not  appear_as_subpart(pa_1, pb) 
            and
            not  appear_as_subpart(pa_4, pb)
            and
            not  appear_as_subpart(pa_6, pb)
            )
    
    return test_passed


# ---------------------------------------------------------------------------

def test_cost_rotated_subpart(): #USER ADDED
    '''
    Test 'cost_rotated_subpart' function on some examples
    
    '''

    # 2
    pa_1 = ((0, 0),
            (0, 0),
            (9, 9))
    # 0
    pa_2 =   ((1, 2, 2),
              (1, 0, 2),
              (1, 1, 2))

    # infinity
    pa_3 =   ((6, 6),
              (1, 8))
    
    # 1
    pa_4 = ((0, 1),
            (1, 2))
    
    # 3
    pa_5 = ((2, 2, 2, 1),
            (2, 0, 1, 1))

    pb =   ((9, 9, 9, 9, 9, 0, 0, 0),
            (0, 0, 0, 0, 1, 2, 2, 2),
            (0, 0, 0, 0, 1, 0, 2, 0),
            (0, 0, 1, 1, 1, 1, 2, 0),
            (0, 0, 0, 1, 0, 1, 1, 0))
    
#    pprint.pprint(pa)
#    pprint.pprint(pb)

    ta_1 = TetrisPart(pa_1) 
    ta_2 = TetrisPart(pa_2) 
    ta_3 = TetrisPart(pa_3) 
    ta_4 = TetrisPart(pa_4)
    ta_5 = TetrisPart(pa_5)
    tb = TetrisPart(pb)
    tb.display('\nPart b')
    ta_1.display('\nExists after 2 rotations.')
    ta_2.display('\nExists after 0 rotations.')
    ta_3.display('\nDoes not exist.')
    ta_4.display('\nExists after 1 rotation.')
    ta_5.display('\nExists after 3 rotations.')

    test_passed =  (  
            cost_rotated_subpart(pa_1,pb), 
            cost_rotated_subpart(pa_2,pb),
            cost_rotated_subpart(pa_3,pb),
            cost_rotated_subpart(pa_4,pb),
            cost_rotated_subpart(pa_5,pb)
            )
    
    #print(test_passed)
    
    return test_passed == (
                           2, 
                           0, 
                           np.inf, 
                           1, 
                           3)


# ---------------------------------------------------------------------------

def test_solve_1():
    '''
    Test function  'my_solver.solve_1'
    '''

    initial_state = load_state('workbenches/wb_05_i.txt')        
    goal_state_no = load_state('workbenches/wb_01_i.txt')        

    goal_state_yes = load_state('workbenches/wb_05_g.txt')        
    
    display_state(initial_state,'Initial state')
    
    display_state(goal_state_no,'\nUnreachable goal state')
    t0 = time.time()
    
    La_no = solve_1(initial_state,goal_state_no)
    t1 = time.time()
    print ('Unreachable Search solve_1 took {0} seconds'.format(t1-t0))
    print('\n\n')
    

    display_state(goal_state_yes,'\nReachable goal state')
    t0 = time.time()
    La_yes = solve_1(initial_state,goal_state_yes)
    t1 = time.time()
    print ('Successful Search solve_1 took {0} seconds'.format(t1-t0))
#    print(La_yes)
#    print(La_no)
    
    test_passed =  (#1  
            La_no == 'no solution'
            and 
            (#2
                    La_yes ==  [(((5, 5, 5),), ((1, 1, 3, 1, 0), (0, 1, 0, 1, 1)), 1), 
                        (((1, 1, 3, 1, 0), (0, 1, 0, 1, 1), (0, 5, 5, 5, 0)), ((1, 2),), -2)]
                or
                    La_yes ==  [
                                ( ((1, 1, 3, 1, 0),(0, 1, 0, 1, 1)), ((1, 2),), -2) ,                            
                                ( ((5, 5, 5),),  ((0, 0, 1, 2, 0),(1, 1, 3, 1, 0),(0, 1, 0, 1, 1)), 1)
                                ]                
            )#2
        )#1
    
    
    return test_passed
    

# ---------------------------------------------------------------------------

def test_solve_2():
    '''
    Test function  'my_solver.solve_2'
    '''

    initial_state = load_state('workbenches/wb_05_i.txt')        
    goal_state_no = load_state('workbenches/wb_01_i.txt')        

    goal_state_yes = load_state('workbenches/wb_05_g.txt')        
    
    display_state(initial_state,'Initial state')
    
    display_state(goal_state_no,'Goal state "no"')
    
    La_no = solve_2(initial_state,goal_state_no)
    print('\n\n')

    display_state(goal_state_yes,'Goal state "yes"')
    La_yes = solve_2(initial_state,goal_state_yes)
#    print(La_yes)
    
    test_passed =  (#1  
            La_no == 'no solution'
            and 
            (#2
                    La_yes ==  [(((5, 5, 5),), ((1, 1, 3, 1, 0), (0, 1, 0, 1, 1)), 1), 
                                (((1, 1, 3, 1, 0), (0, 1, 0, 1, 1), (0, 5, 5, 5, 0)), ((1, 2),), -2)]
                or
                    La_yes ==  [
                                ( ((1, 1, 3, 1, 0),(0, 1, 0, 1, 1)), ((1, 2),), -2) ,                            
                                ( ((5, 5, 5),),  ((0, 0, 1, 2, 0),(1, 1, 3, 1, 0),(0, 1, 0, 1, 1)), 1)
                                ]                
            )#2
        )#1
    
    return test_passed

# ---------------------------------------------------------------------------

def test_solve_3a():
    '''
    Test function  'my_solver.solve_3'
    '''

    print('\n First test example \n')
    initial_state = load_state('workbenches/wb_06_i.txt')        
    goal_state_no = load_state('workbenches/wb_01_i.txt')        
    
    display_state(initial_state,'Initial state')

    goal_state_yes = load_state('workbenches/wb_06_g1.txt')    

    display_state(goal_state_no,'\nUneachable Goal State')    
    display_state(goal_state_yes,'\nReachable Goal State')

    
    t0 = time.time()
    La = solve_3(initial_state, goal_state_no)
    ok_2 = La=='no solution'
    t1 = time.time()
    
    print ('Unreachable Search solve_3 took {0} seconds'.format(t1-t0))
    print('\n\n')
    
    t0 = time.time()
    La = solve_3(initial_state, goal_state_yes)    
    ok_1 = La!='no solution'
    t1 = time.time()
    print ('Reachable Search solve_3 took {0} seconds'.format(t1-t0))
    print('\n\n')
    
    test_passed = ok_1 and ok_2
    
    return test_passed
# ---------------------------------------------------------------------------

def test_solve_3b():
    '''
    Test function  'my_solver.solve_3'
    '''

    initial_state = load_state('workbenches/wb_06_i.txt')        
    goal_state = load_state('workbenches/wb_06_g3.txt')        
    
    display_state(initial_state,'Initial state')
    display_state(goal_state,'\nGoal state')
    
    t0 = time.time()
    La = solve_3(initial_state,goal_state) 
    t1 = time.time()
    
    #print(La)
    print ('Solve_3 took {0} seconds'.format(t1-t0))
    print('\n\n')
    
    return t1-t0 #test_passed

# ---------------------------------------------------------------------------

def test_solve_4():
    '''
    Test function  'my_solver.solve_4'
    '''

    print('\n First test example \n')
    initial_state = load_state('workbenches/wb_06_i.txt')        
    goal_state = load_state('workbenches/wb_06_g2.txt')        
    
    display_state(initial_state,'Initial state')
    display_state(goal_state,'\nGoal state')
    
    t0 = time.time()
    La = solve_4(initial_state,goal_state)    
    t1 = time.time()
    
    print('\n\n Solve_4 took {0} seconds \n'.format(t1-t0))
    print('\n\n')
    
    #


# ---------------------------------------------------------------------------

#    Below are some functions to help you debug your programs 

# ---------------------------------------------------------------------------
    
def gen_prob(ap, num_op, display=True):
    '''
    Given an assembly problem 'ap', generate a goal state by choosing 
    a sequence of random actions.
    
    Return the reachable goal state and a sequence of actions that lead
    to this goal state
    
    '''
    current_state = ap.initial
    display_state(current_state,"\nInitial state")
    
    for i in range(num_op):
        la = ap.actions(current_state)
        #print("Num Actions Now: ", len(la))
        if len(la)==0:
            break
        ra = random.choice(la)
        '''
        if len(ra)==2: print("ROTATE ", ra[1]*90)
        elif len(ra)==3: 
            print("DROP ")
            print("Part Above:")
            print(ra[0])
            print("Part Under: ")
            print(ra[1])
            print("Offset: ", ra[2])
        '''
        current_state = ap.result(current_state, ra)
        if display:
            print('\n')
            
            display_state(current_state,"After action {} ".format(i+1))
            
    return current_state

# ---------------------------------------------------------------------------

def test_action_result_deep():   #USER ADDED
    '''
    Load some parts, and keep building randomly until only one part exists.
    '''
    
    initial_state = load_state('workbenches/wb_08_i.txt')        
    ap = AssemblyProblem_3(initial_state)
    
    state = initial_state
    display_state(state, "INITIAL: ")
    assert(state == initial_state)
    i = 1
    
    while len(make_state_canonical(state)) is not 1:
        
        actions = ap.actions(state)
        action = random.choice(actions)
        
        if len(action)==3:
            pa, pu, offset = action
            pa_ = TetrisPart(pa)
            pu_ = TetrisPart(pu)
            print("\n\nACTION #", i, ", DROP")
            print("Part Above:")
            pa_.display()
            print("Part Under:")
            pu_.display()
            print("Offset: ", offset)
        elif len(action)==2:
            p, r = action
            part = TetrisPart(p)
            print("\n\nACTION #",i, ", ROTATION")
            print("Part:")
            part.display()
            print("Rotate: ", r*90)
        
        new_state = ap.result(state, action)
        assert(new_state != state)
        display_state(new_state, "Result: ")
        state = new_state
        i +=1
        
    print("\n\nFully Built.")
    test_passed = len(state) == 1
    print("Test Action and Result Passed: ", test_passed)


# ---------------------------------------------------------------------------

def test_action_result_broad():   #USER ADDED
    '''
    Load some parts, choose first actions and see results. Visually inspect 
    
    '''
    initial_state = load_state('workbenches/wb_06_i.txt')        
    ap = AssemblyProblem_3(initial_state)
    actions = ap.actions(initial_state)
    display_state(initial_state, "INITIAL: ")
    print("Num Actions: ", len(actions))
    
    for i in range(0, len(actions)):
        if i >-10: #can limit how many to show, here
            if len(actions[i])==3:
                pa, pu, offset = actions[i]
                pa_ = TetrisPart(pa)
                pu_ = TetrisPart(pu)
                print("\n\nACTION #", i)
                print("Part Above:")
                pa_.display()
                print("Part Under:")
                pu_.display()
                print("Offset: ", offset)
                
            elif len(actions[i])==2:
                part, r = actions[i]
                p = TetrisPart(part)
                print("\n\nACTION #", i)
                print("Part: ")
                p.display()
                print("Rotation: ", r*90)
            new_state = ap.result(initial_state, actions[i])
            display_state(new_state, "Result:")
            
                
    
# ---------------------------------------------------------------------------

def test_solve_rand_1():
    '''
    Generate a problem and attempt to solve it
    
    '''
    initial_state = load_state('workbenches/wb_09_i.txt')        
    ap_1 = AssemblyProblem_1(initial_state)
    print("\n\nNumber of Actions: ", len(ap_1.actions(initial_state)))
    
    # num_op=3 is fine
    goal_state = gen_prob(ap_1, num_op=6)
    
    t0 = time.time()

    La = solve_1(initial_state, goal_state)

    t1 = time.time()
    
    print ('Search solve_1 took {0} seconds'.format(t1-t0))

# ---------------------------------------------------------------------------

def test_solve_rand_2():
    '''
    Generate a problem
    
    '''
    initial_state = load_state('workbenches/wb_09_i.txt')        
    ap_2 = AssemblyProblem_2(initial_state)
    print("\n\nNumber of Actions: ", len(ap_2.actions(initial_state)))

    goal_state = gen_prob(ap_2, num_op=3)
    
    La = solve_2(initial_state, goal_state)
    
    
# ---------------------------------------------------------------------------

def test_solve_rand_3(): #USER ADDED
    '''
    Generate a problem and attempt to solve it
    
    '''
    initial_state = load_state('workbenches/wb_06_i.txt')        
    ap_3 = AssemblyProblem_3(initial_state)
    print("\n\nNumber of Actions: ", len(ap_3.actions(initial_state)))
    
    # num_op=3 is fine
    goal_state = gen_prob(ap_3, num_op=3)
    
    t0 = time.time()

    La = solve_3(initial_state, goal_state)

    t1 = time.time()
    
    print ('Search solve_1 took {0} seconds'.format(t1-t0))

# ---------------------------------------------------------------------------

def test_solve_rand_2a(): #USER ADDED
    '''
    Generate a random goal using ap1 
    
    '''
    initial_state = load_state('workbenches/wb_08_i.txt')        
    ap_1 = AssemblyProblem_1(initial_state)
    goal_state = gen_prob(ap_1, num_op=6)
    
    ap_2 = AssemblyProblem_2(initial_state, goal=goal_state)
    print("\n\nNumber of Actions: ", len(ap_2.actions(initial_state)))
    
    
    t0 = time.time()

    La = solve_2(initial_state, goal_state)

    t1 = time.time()
    
    print ('Search solve_1 took {0} seconds'.format(t1-t0))

# ---------------------------------------------------------------------------


def test_solve_rand_4a(): #USER ADDED
    '''
    Generate a random goal using ap3
    
    '''
    initial_state = load_state('workbenches/wb_06_i.txt')        
    ap_3 = AssemblyProblem_3(initial_state)
    goal_state = gen_prob(ap_3, num_op=3)
    
    ap_4 = AssemblyProblem_4(initial_state, goal=goal_state)
    print("\n\nNumber of Actions: ", len(ap_4.actions(initial_state)))
    display_state(initial_state, message="Initial:")
    print(ap_4.actions(initial_state))
    
    
    t0 = time.time()

    La = solve_4(initial_state, goal_state)

    t1 = time.time()
    
    print ('Search solve_1 took {0} seconds'.format(t1-t0))

# ---------------------------------------------------------------------------

def test_solve_1a():
    '''

    Run 'solve_1' on  
        initial_state : 'workbenches/wb_09_i.txt'
        goal_state : 'workbenches/wb_09_g1.txt'
    
    Computation takes about 20 minutes on my aging PC
    
    '''
    initial_state = load_state('workbenches/wb_01_i.txt')    

    goal_state  = load_state('workbenches/wb_01_g1.txt')
        
    t0 = time.time()
    
    La = solve_1(initial_state, goal_state)
    
    t1 = time.time()
    
    print ('Search solve_1 took {0} seconds'.format(t1-t0))
    
# ---------------------------------------------------------------------------

def test_solve_2a():
    '''

    Run 'solve_2' on  
        initial_state : 'workbenches/wb_09_i.txt'
        goal_state : 'workbenches/wb_09_g1.txt'
    
 
    Computation takes about a tenth of a second on my aging PC
   
    '''
    initial_state = load_state('workbenches/wb_08_i.txt')    

    goal_state  = load_state('workbenches/wb_08_g1.txt')
    ap_2 = AssemblyProblem_2(initial_state, goal_state)
    display_state(initial_state, "INITIAL: ")
    display_state(goal_state, "Goal: ")
    
    t0 = time.time()
    
    La = solve_2(initial_state, goal_state)
    
    t1 = time.time()
    
    print ('Search solve_2 took {0} seconds'.format(t1-t0))
    

       
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    print(
'''
\n\n
This is *NOT* the script that will be used to mark your assignment.
Other examples will be used!
But, if your program does not pass the test functions provided in this file,
then it will not pass the test functions the markers will use.
\n\n
''')

#    print('"test_appear_as_subpart" has been passed ', test_appear_as_subpart() )

#    print('"test_cost_rotated_subpart" has been passed ', test_cost_rotated_subpart() )
    
#    print('\n"test_solve_1" has been passed ', test_solve_1() )

#    print('\n"test_solve_2" has been passed ', test_solve_2() )

#    print('\ntest_solve_3a has been passed ', test_solve_3a() )

 #   print('\ntest_solve_3b took {0} seconds'.format(test_solve_3b()) )

#    test_solve_4()

#    pass
    



#    test_solve_1a()
    
#    test_solve_rand_1() 
#    test_solve_rand_2() 
#    test_solve_rand_2a() 
#    test_solve_rand_3()
#    test_solve_rand_4a()
#    test_action_result_broad()
#    test_solve_2a()
#    test_solve_3a()
#    test_solve_3b()
    test_solve_4()

    