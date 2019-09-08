import numpy as np
from copy import deepcopy
import time



def h_misplaced_cost(s, g): # calculating misplaced tiles
        cost = np.sum(s != g)-1
        #print (cost)# minus 1 to exclude the empty tile
        if cost > 0:
            return cost
        else:
            return 0



def all(s):
    #set = '012345678'
    set=string
        
    return 0 not in [c in s for c in set]

# generate board list as per optimized steps in sequence
def genoptimal(state):
    optimal = np.array([], int).reshape(-1, 9)
    last = len(state) - 1
    while last != -1:
        optimal = np.insert(optimal, 0, state[last]['board'], 0)
        last = int(state[last]['parent'])
    return optimal.reshape(-1, 3, 3)

# solve the board
def solve(board, goal):
    #
    moves = np.array(   [   ('u', [0, 1, 2], -3),
                            ('d', [6, 7, 8],  3),
                            ('l', [0, 3, 6], -1),
                            ('r', [2, 5, 8],  1)
                            ],
                dtype=  [  ('move',  str, 1),
                           ('pos',   list),
                           ('delta', int)
                           ]
                        )

    dtstate = [ ('board',  list),
                ('parent', int),
                ('gn',     int),
                ('hn',     int)
                ]

    # initial state values
    parent = -1 #initial parent state
    gn     = 0
    hn     = h_misplaced_cost(board, goal) #calculating misplaced tiles between initial and goal state
    state = np.array([(board, parent, gn, hn)], dtstate) #initializing state

    #priority queue initialization
    dtpriority = [  ('pos', int),
                    ('fn', int)
                    ]

    priority = np.array( [(0, hn)], dtpriority)
    #
    while True:
        priority = np.sort(priority, kind='mergesort', order=['fn', 'pos']) # sort priority queue
        pos, fn = priority[0]                   # pick out first from sorted to explore
        priority = np.delete(priority, 0, 0)    # remove from queue what we are exploring
        board, parent, gn, hn = state[pos]
        board = np.array(board)
        loc = int(np.where(board == 0)[0])      # locate '0' (blank)
        gn = gn + 1                             # increase cost g(n) by 1
        for m in moves:
            if loc not in m['pos']:
                succ = deepcopy(board)          # generate new state as copy of current
                succ[loc], succ[loc + m['delta']] = succ[loc + m['delta']], succ[loc]# do the move
                
                if ~(np.all(list(state['board']) == succ, 1)).any():# check if new (not repeat)
                    hn = h_misplaced_cost(succ, goal)                         # calculate Misplaced tiles
                    q = np.array(   [(succ, pos, gn, hn)], dtstate)     # generate and add new state in the list
                    state = np.append(state, q, 0)
                    fn = gn + hn                                        # calculate f(n)
                    q = np.array([(len(state) - 1, fn)], dtpriority)    # add to priority queue
                    priority = np.append(priority, q, 0)

                    if np.array_equal(succ, goal):                      # is this goal state?
                        print('Goal achieved!')
                        return state, len(priority)
        

    return state, len(priority)


#################################################
def main():
    print()
    alist = []
    print ("Using Misplaced Tiles, solving the 8 puzzle:")
    print("Please enter the goal state: (please enter a space inbetween numbers)")
    alist = [int(x) for x in input().split()]# read goal state
    goal=alist
    print('Enter initial board (please enter a space inbetween numbers): ')# read initial state
    string = [int(x) for x in input().split()]# read goal state

    if len(string) != 9:
        print('incorrect input')
        return

    board = np.array(list(map(int, string)))
    print (board)
    
    
    t1=time.time()
    state, explored = solve(board, goal)
    t2=time.time()
    print()
    print('Total generated:', len(state))
    print('Total explored: ', len(state) - explored)
    print()
    # generate and show optimized steps
    optimal = genoptimal(state)
    print('Total optimized steps:', len(optimal) - 1)
    print()
    print(optimal)
    print()
    print ("The algorithm took " + str((t2-t1) * 1000)  + " ms of time.")


################################################################
# Main Program

if __name__ == '__main__':
    main()


