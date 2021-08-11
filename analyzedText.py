# Exercise from IBM PY0101EN on edX

# Build a tool that can analyze text by creating class with the following:
# - Constructor: takes argument 'text', makes it lower case and removes all punctation (in this case: '.', '!', ',' and '?')
# - freqAll: returns a dictionary of all unique words in the text and their frequency
# - freqOf: returns the frequency of the word

class analyzedText(object):
    
    # Constructor
    def __init__ (self, text):
        
        # make lower case
        formattedText = text.lower()
        
        # remove punctuation
        formattedText = formattedText.replace('.','').replace('!','').replace(',','').replace('?','')
        
        # define data attribute
        self.fmtText = formattedText
    
    # Method
    def freqAll(self):        
        
        # extract words from fmtText
        wordList = self.fmtText.split(' ')
        
        # define dictionary
        freqMap = {}
        for word in wordList:
            freqMap[word] = wordList.count(word)
        
        return freqMap
    
    # Method
    def freqOf(self,word):
        
        # get frequency dictionary
        freqDict = self.freqAll()
        
        # find word in dictionary and return its frequency if available
        if word in freqDict:
            return freqDict[word]
        else:
            return 0


# TEST CODE

# sys module is a set of functions that provide crucial information about 
# how the Python script is interacting with host system
import sys

# define solution dictionary
sampleMap = {'eirmod': 1,'sed': 1, 'amet': 2, 'diam': 5, 'consetetur': 1, 'labore': 1, 'tempor': 1, 'dolor': 1, 'magna': 2, 'et': 3, 'nonumy': 1, 'ipsum': 1, 'lorem': 2}

# create function that tests each of the methods and prints the result
def testMsg(passed):
    if passed: #is True
       return 'Test Passed'
    else : # is False
       return 'Test Failed'

# test constructor of analyzedText class
print("Constructor: ")
try:
    # input latin phrase into analyzedText
    samplePassage = analyzedText("Lorem ipsum dolor! diam amet, consetetur Lorem magna. sed diam nonumy eirmod tempor. diam et labore? et diam magna. et diam amet.")
    
    # if output equals manually typed input, set testMsg = True via if statement defined above
    print(testMsg(samplePassage.fmtText == "lorem ipsum dolor diam amet consetetur lorem magna sed diam nonumy eirmod tempor diam et labore et diam magna et diam amet"))

except:
    # if output doesn't match, return custom error message
    print("Error detected. Recheck your function " )

# test freqAll method
print("freqAll: ")
try:
    # use method on samplePassage and store in new variable
    wordMap = samplePassage.freqAll()

    # if output equals manually typed input, set testMsg = True via if statement defined above
    print(testMsg(wordMap==sampleMap))

except:
    print("Error detected. Recheck your function " )

# test freqOf method
print("freqOf: ")
try:
    
    passed = True
    
    # check each word using .freqOf from Class vs solution dictionary defined above
    for word in sampleMap:
        if samplePassage.freqOf(word) != sampleMap[word]:
            passed = False
            break
    print(testMsg(passed))
    
except:
    print("Error detected. Recheck your function  " )
