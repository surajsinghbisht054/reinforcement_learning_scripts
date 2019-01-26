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


 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    Creating Simple Treasur Hunt Game Based On Reinforcement Learning
 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''
import time
import random
import sys

# Configurations
EPSILON  = 0.9                 # Rate Of Changes in EPLISON = (1.0 - RATE_OF_CHANGE_IN_VALUES)
ACTIONS  = ['left', 'right']
ALPHA    = 0.1                 # learning rate
GAMMA    = 0.9                 # discount factor
EPISODES = 20                  # EPISODE
Debug    = False
BIGREWARD = 1.0
SMALLREWARD = 0.1 # small reward 
TIMESLEEP = 0.1
CUTREWARD = 11.0 # divide reward after 11 steps


# Game Track
TRACK = ['-','-','-','-','-','-','-','-','-','-','-','-']
TRACK.append('#') # gold in the end


# show debug status
if Debug: print "[*] Debug Variable Is True"

# print track
if Debug: print "[*] Track : ", ''.join(TRACK) 


# Q Learning Decision Table
Qtable = [
    # left, right
    [ 0,    0 ], # 0
    [ 0,    0 ], # 1
    [ 0,    0 ], # 2

    [ 0,    0 ], # 3
    [ 0,    0 ], # 4
    [ 0,    0 ], # 5

    [ 0,    0 ], # 6
    [ 0,    0 ], # 7
    [ 0,    0 ], # 8

    [ 0,    0 ], # 9
    [ 0,    0 ], # 10
    [ 0,    0 ], # 11
]

BestQTable = {}


# choose action
def choose_action(playerstate):

    # Get Qtable left right 
    tmprow = Qtable[playerstate]

    # limit random value updating using epsilon value
    if ((random.uniform(0.0, 1.0) > EPSILON) or (max(tmprow)==0 )):
        # choice action randomly 
        action = random.choice(ACTIONS)

    else:
        # decide, based on Qtable Decision value
        if tmprow[0]>tmprow[1]:
            action = ACTIONS[0]
        else:
            action = ACTIONS[1]

    # print debugging informations
    if Debug: print "[*] Player State : {} | Action Choice : {} ".format(playerstate, action)
    
    return action

# take player action and return reward
def take_action(playerstate, action, count):
    #
    over = False
    reward = 0

    # if action=left
    if action==ACTIONS[0]:

        # if player back to starting point
        if playerstate==0:
            newstate = playerstate # reach starting point
        else:
            newstate = playerstate - 1

    # action=right
    else:
        newstate = playerstate + 1
        # win
        if playerstate==11:
            over = True # Game Over
            reward = (float(BIGREWARD)/float(count))*CUTREWARD # Give Reward
        else:
            reward = SMALLREWARD # small reward for right, ComeOn! Encourage Agent To Solve it Quickly
    if Debug: print "[*] Take Action > Player At {} | Reward {} | End {}".format(newstate, reward, over)
    return (newstate, reward, over)

# print details over terminal
def print_updates(S, episode, count, end=False):
    tmp = TRACK[:]
    tmp[S]='o'
    if Debug: print "{}".format(''.join(tmp))

    if not Debug: 
        sys.stdout.write("\r{} ".format(''.join(tmp)))
        sys.stdout.flush()

    if end:
        print "\n[*] Numbers of Episode : {}\r".format(episode)
        print "[*] Numbers of Steps   : {}".format(count)

    # to make this process more cool
    time.sleep(TIMESLEEP)


# main function
def main():

    # Iterate Episode
    for episode in range(EPISODES):

        # Intialize variable at Every new iteration
        PS = 0          # Player State In Game
        count = 0       # steps counter
        END = False     # no end
        print_updates(PS, episode, count)
        
        while not END:
            # choose action to take
            AC = choose_action(PS)

            # check feed back
            NS, RW, END = take_action(PS, AC, count)
        
            # update
            print_updates(NS, episode, count, end=END)

            if END:
                qtarget = RW
            else:
                # Formula
                qtarget = RW + GAMMA * max(Qtable[PS])

            # previous value
            prevalue = Qtable[PS][ACTIONS.index(AC)]

            # updated value
            Qtable[PS][ACTIONS.index(AC)] += ALPHA *( qtarget-prevalue)

            count += 1

            PS = NS # new playerstate
    return


if __name__=='__main__':
    main()
    print "\n\n{}\t |\t {}\t |\t {}\n".format(str("No.").rjust(3), 'left'.rjust(18), 'right'.rjust(18))
    for no, row in enumerate(Qtable):
        col1, col2 = row[0], row[1]
        print "{}\t |\t {}\t |\t {}".format(str(no).rjust(3), str(col1).ljust(18), str(col2).ljust(18))

