import numpy as np
from copy import deepcopy
import time



# calculate Manhattan distance for each digit as per goal
def mhd(s, g):
    m = abs(s // 3 - g // 3) + abs(s % 3 - g % 3)
    return sum(m[1:])

# assign each digit the coordinate to calculate Manhattan distance
def coor(s):
    c = np.array(range(9))
    for x, y in enumerate(s):
        c[y] = x
    return c




def all(s):
    #set = '012345678'
    set=string
        
    return 0 not in [c in s for c in set]

# generate board list as per optimized steps in sequence
def stepsoptimal(state):
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

    goalc = coor(goal)
    # initial state values
    parent = -1 #initial parent state
    gn     = 0
    hn     = mhd(coor(board), goalc) #calculating manhattan distance between initial and goal state
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
                
                if ~(np.all(list(state['board']) == succ, 1)).any():#check if new (not repeat)
 
                    hn = mhd(coor(succ), goalc)                         # calculate Manhattan distance
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
    print ("Using Manhattan Distance, solving the 8 puzzle:")
    print("Please enter the goal state: (Please enter a space inbetween numbers)")
    goal = [int(x) for x in input().split()]# read goal state
    
    print('Enter initial board: (Please enter a space inbetween numbers) ')# read initial state
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
    optimal = stepsoptimal(state)
    print('Total optimized steps:', len(optimal) - 1)
    print()
    print(optimal)
    print()
    print ("The algorithm took " + str((t2-t1) * 1000)  + " ms of time.")


################################################################
# Main Program

if __name__ == '__main__':
    main()



