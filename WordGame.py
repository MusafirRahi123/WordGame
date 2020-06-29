# The 6.00 Word Game

import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"

def loadWords():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordList: list of strings
    wordList = []
    for line in inFile:
        wordList.append(line.strip().lower())
    print("  ", len(wordList), "words loaded.")
    return wordList

def getFrequencyDict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def getWordScore(word, n):
    """
    Returns the score for a word. Assumes the word is a valid word.

    The score for a word is the sum of the points for letters in the
    word, multiplied by the length of the word, PLUS 50 points if all n
    letters are used on the first turn.

    Letters are scored as in Scrabble; A is worth 1, B is worth 3, C is
    worth 3, D is worth 2, E is worth 1, and so on (see SCRABBLE_LETTER_VALUES)

    word: string (lowercase letters)
    n: integer (HAND_SIZE; i.e., hand size required for additional points)
    returns: int >= 0
    """
    # TO DO ... <-- Remove this comment when you code this function
    Sum = 0
    Point = 0 
    for letter in word:
        #print(letter)
        Sum = Sum + SCRABBLE_LETTER_VALUES[letter]
    if(len(word) == n):
        Points = Sum * len(word) + 50
    else:
        Points = Sum * len(word)
    return Points

#
# Problem #2: Make sure you understand how this function works and what it does!
#
def displayHand(hand):
    """
    Displays the letters currently in the hand.

    For example:
    >>> displayHand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    for letter in hand.keys():
        for j in range(hand[letter]):
            print(letter,end=' ')       # print all on the same line
    print()                             # print an empty line

#
# Problem #2: Make sure you understand how this function works and what it does!
#
def dealHand(n):
    """
    Returns a random hand containing n lowercase letters.
    At least n/3 the letters in the hand should be VOWELS.

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    hand={}
    numVowels = n // 3
    
    for i in range(numVowels):
        x = VOWELS[random.randrange(0,len(VOWELS))]
        hand[x] = hand.get(x, 0) + 1
        
    for i in range(numVowels, n):    
        x = CONSONANTS[random.randrange(0,len(CONSONANTS))]
        hand[x] = hand.get(x, 0) + 1
        
    return hand

#
# Problem #2: Update a hand by removing letters
#
def updateHand(hand, word):
    """
    Assumes that 'hand' has all the letters in word.
    In other words, this assumes that however many times
    a letter appears in 'word', 'hand' has at least as
    many of that letter in it. 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    # TO DO ... <-- Remove this comment when you code this function
    TempHand = {}
    RemainingHand = {}
    #TempHand.copy(hand)
    for letter in word:
        if(letter in TempHand):
            TempHand[letter] = TempHand[letter] + 1
        else:    
            TempHand[letter] = 1
         
    for element in hand:
        if(element in TempHand):
            RemainingHand[element] = hand[element] - TempHand[element]
        else:
            RemainingHand[element] = hand[element]
    return RemainingHand


#
# Problem #3: Test word validity
#
def isValidWord(word, hand, wordList):
    """
    Returns True if word is in the wordList and is entirely
    composed of letters in the hand. Otherwise, returns False.

    Does not mutate hand or wordList.
   
    word: string
    hand: dictionary (string -> int)
    wordList: list of lowercase strings
    """
    # TO DO ... <-- Remove this comment when you code this function
    Found = 0
    WordusedFrmHand = 0
    ExcessUsage  = 1
    TempHand = {}
    #print(str(word))
    for element in wordList:
        if element == word:
            #print(element)
            Found = 1
            break
    for letter in word:
        if(letter in TempHand):
            TempHand[letter] = TempHand[letter] + 1
        else:    
            TempHand[letter] = 1

    for element in TempHand:
        
        for handy in hand:
            WordusedFrmHand = 0
            if(ExcessUsage == 0):
                break;
            if(element == handy):
                if(TempHand[element] <= hand[handy]):
                    WordusedFrmHand = 1
                    break
                else:
                    WordusedFrmHand = 0
                    ExcessUsage = 0
                    break;
        if(WordusedFrmHand == 0):
            ExcessUsage = 0
    if(WordusedFrmHand == 1 and Found == 1):
        return True
    return False

#
# Problem #4: Playing a hand
#

def calculateHandlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    # TO DO... <-- Remove this comment when you code this function
    Sum = 0
    for element in hand:
        Sum = Sum + hand[element]
                    
    return Sum    



def playHand(hand, wordList, n):
    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    * The user may input a word or a single period (the string ".") 
      to indicate they're done playing
    * Invalid words are rejected, and a message is displayed asking
      the user to choose another word until they enter a valid word or "."
    * When a valid word is entered, it uses up letters from the hand.
    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.
    * The sum of the word scores is displayed when the hand finishes.
    * The hand finishes when there are no more unused letters or the user
      inputs a "."

      hand: dictionary (string -> int)
      wordList: list of lowercase strings
      n: integer (HAND_SIZE; i.e., hand size required for additional points)
      
    """
    # BEGIN PSEUDOCODE <-- Remove this comment when you code this function; do your coding within the pseudocode (leaving those comments in-place!)
    # Keep track of the total score
    
    # As long as there are still letters left in the hand:
    
        # Display the hand
    Input = 'a'    
    Len = calculateHandlen(hand)
    Points = 0
    while(Input != '.' or Len != 0):
        
        print("Current Hand: ",end='')
        displayHand(hand)
        # Ask user for input
        Input = input("Enter word, or a . to indicate that you are finished:")
        # If the input is a single period:
        if(Input == '.'):
            print("Goodbye! Total score: " + str(Points)+ " points.")
            break
            # End the game (break out of the loop)
          
        if(isValidWord(Input, hand,wordList) == False):
            print("Invalid word, please try again.")
        else:
            Points = Points + getWordScore(Input,n)
            print (str(Input) + " earned " + str(getWordScore(Input,n)) + " Points." + " Total: " + str(Points) + " points")
            RemainingHand = updateHand(hand,Input)
            hand = RemainingHand
            Len = calculateHandlen(hand)
            if(Len == 0):
                print("Run out of letters. " + "Total score: " + str(Points))
                break
        # Otherwise (the input is not a single period):
        
            # If the word is not valid:
            
                # Reject invalid word (print a message followed by a blank line)

            # Otherwise (the word is valid):

                # Tell the user how many points the word earned, and the updated total score, in one line followed by a blank line
                
                # Update the hand 
                

    # Game is over (user entered a '.' or ran out of letters), so tell user the total score


#
# Problem #5: Playing a game
# 

def playGame(wordList):
    """
    Allow the user to play an arbitrary number of hands.

    1) Asks the user to input 'n' or 'r' or 'e'.
      * If the user inputs 'n', let the user play a new (random) hand.
      * If the user inputs 'r', let the user play the last hand again.
      * If the user inputs 'e', exit the game.
      * If the user inputs anything else, tell them their input was invalid.
 
    2) When done playing the hand, repeat from step 1    
    """
    # TO DO ... <-- Remove this comment when you code this function
    Input = 'a'
    Reuse_Hand = {}
    while(Input != 'e'):
        Input = input("Enter n to deal a new hand, r to replay the last hand, or e to end game:")
        if(Input == 'n'):
           Reuse_Hand =  dealHand(HAND_SIZE)
           playHand(Reuse_Hand, wordList, HAND_SIZE)
        elif(Input == 'r'):
            if(Reuse_Hand == {}):
                print("You have not played a hand yet. Please play a new hand first!")
                #break
            else:
                playHand(Reuse_Hand, wordList, HAND_SIZE)
        elif(Input == 'e'):
            break
        else:
            print("Invalid Command.")
    #print("playGame not yet implemented.") # <-- Remove this line when you code the function
   



#
# Build data structures used for entire session and play game
#
if __name__ == '__main__':
    wordList = loadWords()
    playGame(wordList)
