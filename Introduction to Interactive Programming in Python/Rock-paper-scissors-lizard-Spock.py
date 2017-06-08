# import module
import random


# first part convert name to number 
def name_to_number(inputstr):
    output_number=[ "rock", "Spock", "paper", "lizard", "scissors"].index(inputstr) # index number is the output value 
    return output_number 
    
# second part and third part        
def rpsls(inputstr):
    output_number=name_to_number(inputstr)
    pc_choice_str=random.choice([ "rock", "Spock", "paper", "lizard", "scissors"]) # pc move
    pc_choice_value=name_to_number(pc_choice_str) # return the pc choice with coresponding value in [0,1,2,3,4]
    # calculate win or lose 
    dif=pc_choice_value-output_number 
    reminder=dif % 5 

    if reminder==1 or reminder==2:
        result='Computer wins!'
    elif reminder==0:
        result = 'Player and computer tie!' 
    else:
        result='Player wins!' 
    print  'Player chooses '+inputstr+'\n'+'Computer chooses ' + pc_choice_str+'\n'+result+'\n'
        
# test your code - THESE CALLS MUST BE PRESENT IN YOUR SUBMITTED CODE
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")