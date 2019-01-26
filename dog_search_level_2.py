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
'''

import random
import time
import os

# Configuration
ALPHA = 0.1
GAMMA = 0.9
EPLISON  = 0.5
EPISODES = 10
ACTIONS = ['left', 'right', 'top', 'bottom']
TIMESLEEP = 0.01
MINUSPOINT = -0.5
PLUSPOINT = 1.0
Debug = False
IValue = [1,1,1,1]


# (ALPHA*(( reward + GAMMA * pre_calculated_possibility) - pre_calculated_possibility) + pre_calculated_possibility)


tmpboard = []

# Column = 14
#  Row   = 14
GROUND = [
    ['#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ],
    ['#', '_' ,'_' ,'_' ,'_' ,'_' ,'_' ,'_' ,'_' ,'_' ,'_' ,'_' ,'_' , '#' ],
    ['#', '_' ,'_' ,'#' ,'_' ,'_' ,'_' ,'_' ,'_' ,'_' ,'_' ,'#' ,'#' , '#' ],
    ['#', '_' ,'_' ,'#' ,'_' ,'_' ,'_' ,'_' ,'_' ,'_' ,'_' ,'#' ,'#' , '#' ],
    ['#', '_' ,'_' ,'#' ,'_' ,'_' ,'#' ,'_' ,'_' ,'#' ,'_' ,'#' ,'_' , '#' ],
    ['#', '_' ,'_' ,'#' ,'_' ,'_' ,'#' ,'_' ,'_' ,'#' ,'_' ,'#' ,'_' , '#' ],
    ['#', '_' ,'_' ,'#' ,'#' ,'#' ,'#' ,'_' ,'_' ,'#' ,'_' ,'_' ,'_' , '#' ],
    ['#', '_' ,'_' ,'_' ,'_' ,'_' ,'#' ,'_' ,'_' ,'_' ,'_' ,'_' ,'_' , '#' ],
    ['#', '_' ,'_' ,'_' ,'_' ,'_' ,'_' ,'_' ,'_' ,'_' ,'#' ,'_' ,'_' , '#' ],
    ['#', '_' ,'_' ,'_' ,'_' ,'_' ,'_' ,'_' ,'_' ,'_' ,'_' ,'_' ,'_' , '#' ],
    ['#', '_' ,'#' ,'#' ,'#' ,'_' ,'_' ,'_' ,'_' ,'_' ,'#' ,'_' ,'_' , '#' ],
    ['#', '_' ,'_' ,'_' ,'#' ,'_' ,'_' ,'_' ,'_' ,'_' ,'_' ,'_' ,'_' , '#' ],
    ['#', '_' ,'_' ,'_' ,'#' ,'_' ,'_' ,'_' ,'_' ,'_' ,'_' ,'_' ,'^' , '#' ],
    ['#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ],
]


# Qtable
Qtable = {
}

# check Qtable state
def check_state(PS):
    ps = [str(i) for i in PS]
    key = '_'.join(ps)

    if key not in Qtable.keys():
        if Debug: print "[*] Adding new state : ", key
        #           left right top bottom
        Qtable[key] = IValue[:]

    return key


# print board
def print_status(PS, episode, count, end):
    if not Debug: os.system('clear')
    ctmp = GROUND[:]

    for n,row in enumerate(ctmp):
        row = row[:]
        if n==PS[0]:
            row[PS[1]]='0'
            
        print ' '.join(row)
    for i in tmpboard:
        print i
    print "[ Episode  : {} | Steps : {} ]".format(episode, count)
    if end:
        tmpboard.append("[ Episode  : {} | Steps : {} ]".format(episode, count))
    time.sleep(TIMESLEEP)
    return

# choose action
def choose_action(PS):
    key = check_state(PS)

    # limit value updating rate
    if (random.uniform(0.0, 1.0) > EPLISON) or (max(Qtable[key])==0):
        action = random.choice(ACTIONS)
        if Debug: print "[+] Random Action Selecting", action
    else:
        p = max(Qtable[key])
        action = ACTIONS[Qtable[key].index(p)]
        if Debug: print "[*] Choosing Action Based On Q Table Probability.", action
        
    return action

# get feedback
def get_feedback(PS, AC):
    # default values
    RW = 0
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

def learner(PS, RW, AC, END):
    key = check_state(PS)

    if END:
        qtarget = RW
    else:
        qtarget = RW + GAMMA * max(Qtable[key])
    pre_value = Qtable[key][ACTIONS.index(AC)]

    # update value
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
            learner(PS, RW, AC, END)
            PS = _PS
            print_status(PS, episode, count, END)
            count += 1
    return

# trigger 
if __name__ == '__main__':
    main()

