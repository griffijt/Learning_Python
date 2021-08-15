# IBM PY0101EN, Module 4, Lab: Writing Files with Open

# Part 1: generate two random files of active and inactive members
# Part 2: write function to remove inactive members from active member list and add them to inactive member list

#---Part 1: This section of code developed by IBM course author/contributor: Joseph Santarcangelo---

# Purpose: generate and view random data for activity (creates txt files with Membership No, Date Joined and Active status)

# Note: comments throughout were added to document my understanding of the code written by the author

# call the random integer function from the Python 3 'random' module rnd 
from random import randint as rnd

# name the files
memReg = 'members.txt'
exReg = 'inactive.txt'

# create a variable to derive if the member is active 
fee =('yes','no')

# define genFiles function used to generate the random data files
def genFiles(current,old):
    
    # create current membership file
    with open(current,'w+') as writefile: 
        # add headers
        writefile.write('Membership No  Date Joined  Active  \n')
        # define substitution string (if anyone can provide more detail around this, please contact me)
        data = "{:^13}  {:<11}  {:<6}\n"
        # for each of 20 rows
        for rowno in range(20):
            # create a random date between 2015 and 2020
            date = str(rnd(2015,2020))+ '-' + str(rnd(1,12))+'-'+str(rnd(1,25))
            # generate random Membership No and Active status (if they've paid fee or not)
            writefile.write(data.format(rnd(10000,99999),date,fee[rnd(0,1)]))

    # create old membership file in similar vain to the above, yet all members are inactive
    with open(old,'w+') as writefile: 
        writefile.write('Membership No  Date Joined  Active  \n')
        data = "{:^13}  {:<11}  {:<6}\n"
        for rowno in range(3):
            date = str(rnd(2015,2020))+ '-' + str(rnd(1,12))+'-'+str(rnd(1,25))
            writefile.write(data.format(rnd(10000,99999),date,fee[1])) # note members didn't pay fee

genFiles(memReg,exReg)

# view files
headers = "Membership No  Date Joined  Active  \n"
with open(memReg,'r') as readFile:
    print("Active Members: \n")
    print(readFile.read())
    
with open(exReg,'r') as readFile:
    print("Inactive Members: \n")
    print(readFile.read())

#---Part 2: Define function to sort through data---

# Purpose: define function to remove inactive members from active file and put them in inactive file

def cleanFiles(currentMem,exMem):
    '''
    currentMem: File containing list of current members
    exMem: File containing list of old members
    
    Removes all rows from currentMem containing 'no' and appends them to exMem
    '''
    with open(currentMem, 'r+') as writeFile:
        with open(exMem, 'a+') as appendFile:
            writeFile.seek(0) # set cursor to beginning
            members = writeFile.readlines() # store members in a list object
            header = members[0] # save header as variable
            members.pop(0) # remove header from members list
            
            # add members to inactive List if not active
            inactive = [member for member in members if ('no' in member)]
            '''
            The above is the same as
            for member in active:
            if 'no' in member:
                inactive.append(member)
            '''
            # go to the beginning of file and add header
            writeFile.seek(0)
            writeFile.write(header)
            
            # loop through members
            for member in members:
                if (member in inactive): # if member is in inactive list created above, then 
                    # write them to the appendFile (exMem)
                    appendFile.write(member)
                else: # otherwise write them to writeFile (currentMem)
                    writeFile.write(member)
            writeFile.truncate() # remove any extra lines

# run cleanFiles function
cleanFiles(memReg,exReg)

# open files
headers = "Membership No  Date Joined  Active  \n"
with open(memReg,'r') as readFile:
    print("Modified Active Members: \n")
    print(readFile.read())
    
with open(exReg,'r') as readFile:
    print("Modified Inactive Members: \n")
    print(readFile.read())
