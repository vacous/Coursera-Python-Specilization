"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    max_score = 0
    for ele in hand:
        if hand.count(ele) * ele > max_score:
            max_score = hand.count(ele) * ele
    return max_score
    


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    rolling_possible = gen_all_sequences( range(1, num_die_sides+1 ), num_free_dice)
    total_value = 0.0
    for ele in rolling_possible:
        temp = list(held_dice)
        temp.extend( ele )
        total_value += score(temp)
    
    expect = total_value / len(rolling_possible)
    return expect

def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    possible_hold = set([()])
    for num in range( 1, len(hand)+1 ):
        update_set = gen_all_sequences(hand, num)
        for ele in update_set:
            temp = list(ele)
            for each in ele:
                if temp.count(each) > hand.count(each):
                    temp = []  
            temp.sort()        
            possible_hold.add( tuple(temp) )    
                
    return possible_hold



def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    expect_value = 0 
    dice_hold = ()
    for ele in gen_all_holds(hand):
        temp = expected_value(ele, num_die_sides, len(hand)-len(ele))
        if temp > expect_value:
            expect_value = temp
            dice_hold = ele
    return expect_value, dice_hold

def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 3, 5)
    print score(hand)
    print gen_all_holds(hand)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
  
run_example()


#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)
                                       
    
    
    



