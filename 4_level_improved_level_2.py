#!/usr/bin/python


'''
Author: 
        Suraj Singh Bisht
        surajsinghbisht054@gmail.com
        www.bitforestinfo.com


Description:
        This Script is Part of https://github.com/surajsinghbisht054/reinforcement_learning_scripts Project.
        I Wrote this script just for Educational and Practise Purpose Only.
        
==================================================================================
                Please Don't Remove Author Initials
==================================================================================

You Can Use These Codes For Anything But You Just Have To Mention Author Initial With
The Codes. And yes! This is Compulsory.


+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                    Game :  Dog have to find bone
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Rules:
        Dog  looks like this  'O'
        Bone looks like this  '^'
        walls looks like this '#'
        floor looks like this '_'

Description:
    Using Negative Reward at every step dog spend to find bone
    And, Important Improvement is, Negative Reward only applies if one path
    is visited by agent more than one times.
'''

# import modules
import random
import time
import os
import cPickle

os.system('test')


# Configuration
ALPHA    = 0.5    # learning rate 
GAMMA    = 0.9    # discount factor
EPLISON  = 0.9    # limit the changes <-- Random Decision Rate
EPISODES = 10     # total episodes to try
ACTIONS  = [      # supported actions
        'left', 
        'right', 
        'top', 
        'bottom'
    ]

TIMESLEEP       = 0.01    # refresh sleep time
MINUSPOINT      = -5     # can set minus point, when hit the walls [Heavy Penatly] 
PLUSPOINT       = 10     # plus point, in the end <-- Not that much important, because we are using negative reward approach
LATEMINUSPOINT  = -1    # because of time 
Debug           = False   # debug feature
IValue          = [       # initial values
                    0,0,
                    0,0
                    ]
BACKUP          = '' #'test/dog_search_coordinates.qtable'
OUTPUT          = False
NEUTRAL         = 1
# Keep Record of Paths
path_record = []

# 
if not OUTPUT:
    TIMESLEEP = 0


# board to collect episode print data
tmpboard = []



# Column = 14
#  Row   = 14
GROUND = [
    ['#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ],
    ['#', '_' ,'#' ,'#' ,'_' ,'_' ,'#' ,'_' ,'_' ,'_' ,'_' ,'_' ,'_' , '#' ],
    ['#', '_' ,'#' ,'_' ,'_' ,'_' ,'#' ,'_' ,'#' ,'#' ,'_' ,'#' ,'_' , '#' ],
    ['#', '_' ,'#' ,'_' ,'#' ,'_' ,'#' ,'_' ,'_' ,'#' ,'_' ,'#' ,'_' , '#' ],
    ['#', '_' ,'#' ,'_' ,'#' ,'_' ,'#' ,'#' ,'_' ,'#' ,'_' ,'#' ,'_' , '#' ],
    ['#', '_' ,'#' ,'_' ,'#' ,'_' ,'#' ,'#' ,'_' ,'#' ,'#' ,'#' ,'_' , '#' ],
    ['#', '_' ,'#' ,'_' ,'#' ,'_' ,'#' ,'_' ,'_' ,'#' ,'_' ,'#' ,'_' , '#' ],
    ['#', '_' ,'#' ,'_' ,'#' ,'_' ,'#' ,'_' ,'#' ,'#' ,'#' ,'_' ,'_' , '#' ],
    ['#', '_' ,'#' ,'_' ,'#' ,'_' ,'#' ,'_' ,'_' ,'_' ,'#' ,'_' ,'_' , '#' ],
    ['#', '_' ,'#' ,'_' ,'#' ,'_' ,'#' ,'_' ,'_' ,'_' ,'#' ,'_' ,'#' , '#' ],
    ['#', '_' ,'#' ,'_' ,'#' ,'_' ,'#' ,'#' ,'_' ,'#' ,'#' ,'_' ,'#' , '#' ],
    ['#', '_' ,'#' ,'_' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' , '#' ],
    ['#', '_' ,'_' ,'_' ,'_' ,'_' ,'_' ,'_' ,'_' ,'_' ,'_' ,'_' ,'^' , '#' ],
    ['#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ],
]

if os.path.exists(BACKUP):
    tmpboard.append('[*] Using Pre-Calculated Weight.')
    # load pre-calculated tables
    Qtable = cPickle.load(open(BACKUP, 'r'))

else:
    tmpboard.append('[*] New Weight Calculation.')
    # Qtable
    Qtable = {
    }

# check Qtable state
def check_state(PS):

    # convert int list into string list
    ps = [str(i) for i in PS]

    # join list values
    key = '_'.join(ps)

    # check if its new key
    if key not in Qtable.keys():

        if Debug: print "[*] Adding new state : ", key

        #           left right top bottom
        Qtable[key] = IValue[:]

    return key


# print board
def print_status(PS, episode, count, end):

    if not Debug: os.system('clear')

    # copy ground
    ctmp = GROUND[:]

    # iterate 
    for n,row in enumerate(ctmp):
        row = row[:]
        if n==PS[0]:
            row[PS[1]]='0'
            
        print ' '.join(row)

    # print board data
    for i in tmpboard[-10:]:
        print i

    print "[ Episode  : {} | Steps : {} ]".format(episode, count)

    # print end game message banner
    if end:
        tmpboard.append("[ Episode  : {} | Steps : {} ]".format(episode, count))

    # wait
    time.sleep(TIMESLEEP)
    return

# choose action
def choose_action(PS):

    key = check_state(PS)

    # limit value updating rate
    if ((random.uniform(0.0, 1.0) > EPLISON) or (max(Qtable[key])==0)):
        action = random.choice(ACTIONS)
        if Debug: print "[+] Random Action Selecting", action

    else:
        p = max(Qtable[key])
        action = ACTIONS[Qtable[key].index(p)]
        if Debug: print "[*] Choosing Action Based On Q Table Probability.", action
        
    return action

# get feedback
def get_feedback(PS, AC):

    if PS in path_record:
        # value when, path is already visited in past
        RW = LATEMINUSPOINT

    else:
        RW = NEUTRAL #NEUTRALPOINT
        path_record.append(PS)

   
    END = False

    _PS = PS[:]

    x,y = PS[0], PS[1]
    # left
    if AC==ACTIONS[0]:
        if GROUND[x][y-1]=='#':
            RW = MINUSPOINT
        else:
            _PS = [x, y-1]
    # right
    elif AC==ACTIONS[1]:
        if GROUND[x][y+1]=='#':
            RW = MINUSPOINT
        else:
            _PS = [x, y+1]
    # top
    elif AC==ACTIONS[2]:
        if GROUND[x-1][y]=="#":
            RW = MINUSPOINT
        else:
            _PS = [x-1, y]
    
    # bottom
    elif AC==ACTIONS[3]:
        if GROUND[x+1][y]=="#":
            RW = MINUSPOINT
        else:
            _PS = [x+1, y]
    else:
        print "[*] Misconfiguration detected into ACTIONS variable and get_feedback function."

    # dog found bone
    if GROUND[_PS[0]][_PS[1]]=="^":
        END = True
        RW = PLUSPOINT

    return (_PS, RW, END)

def learner(PS, RW, AC, _PS ,END):
    # PS = previous state player status
    # RW = Reward
    # AC = Action
    # _PS = New state player status
    # END = episode end or not
    key = check_state(_PS)

    if END:
        qtarget = RW
    else:
        qtarget = RW + (GAMMA * max(Qtable[key]))

    # get previous state value
    pre_value = Qtable[check_state(PS)][ACTIONS.index(AC)]

    # update new state value
    Qtable[key][ACTIONS.index(AC)] += ALPHA * (qtarget - pre_value)

    return

# main function
def main():
    for episode in range(EPISODES):
        # initialise values
        # Player Location (x, y) 
        PS = [1, 1]
        count = 0
        END = False
        
        # training loop
        while not END:
            AC = choose_action(PS)
            _PS, RW, END = get_feedback(PS, AC)
            learner(PS, RW, AC,_PS, END)
            PS = _PS
            if OUTPUT:
                print_status(PS, episode, count, END)
            count += 1
        print_status(PS, episode, count, END)
    return

# trigger 
if __name__ == '__main__':
    main()
    if BACKUP:
        f = open(BACKUP, 'w')
        cPickle.dump(Qtable, f)
        f.close()
    for key, val in Qtable.items():
        x,y = key.split('_')
        print "[*] X {} [ROW] | Y {} [Column] ".format(x, y) 
        for a,b in zip(ACTIONS, val):
            print "----> Action {} Value {} ".format(a, b)
