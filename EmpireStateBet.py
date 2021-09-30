"""
From: DataCamp Intermediate Python Course, Part 5: Hacker Statistics
Author: Hugo Bowne-Anderson
Source: https://www.datacamp.com/courses/intermediate-python

Modified by: Justin Griffith

Purpose: Write a scrypt that models and solves the problem below.

Scenario: 
You're at the Empire State building with a friend and you decide to throw a die one hundred times.
If it's 1 or 2 you'll go one step down. If it's 3, 4, or 5, you'll go one step up.
If you throw a 6, you'll throw the die again and will walk up the resulting number of steps.
And also, you admit that you're a bit clumsy and have a chance of 0.1% of falling down the stairs when you make a move. 
Falling down means that you have to start again from step 0. 
With all of this in mind, you bet your friend that you'll reach 60 steps high.
What is the chance that you will win this bet?
"""

# Import libraries
import numpy as np
import matplotlib.pyplot as plt

# set random seed
np.random.seed(123)

# initialize all walks list
all_walks = []

# simulate random walk 10,000 times
for i in range(10000) :
    
    # start random walk at step 0
    random_walk = [0]

    # play the game 100 times
    for x in range(100) :
        step = random_walk[-1] # start at previous step
        dice = np.random.randint(1,7) # roll the die
        if dice <= 2 : # if roll less than 2, step down
            step = max(0, step - 1) # assume no basement (i.e. floor 0 is min)
        elif dice <= 5 : # if roll between 3 and 5, step up
            step = step + 1
        else : # if roll a six, roll again and walk up that many steps
            step = step + np.random.randint(1,7)
        
        # implement probability of falling down stairs (to floor 0)
        if np.random.rand() <= 0.001 : # simulate a random number, if less that 0.1%, fall to ground floor
            step = 0
        
        # add result of roll/steps to list
        random_walk.append(step)
    
    # save the result of the game
    all_walks.append(random_walk)

# create np array of game results
np_aw_t = np.transpose(np.array(all_walks))

# select last row from np_aw_t: ends
ends = np_aw_t[-1,:]

# Plot histogram of ends, display plot
plt.hist(ends)
plt.show()

# calculate probability of being greater than step 60
print(sum(ends>60)/10000)
