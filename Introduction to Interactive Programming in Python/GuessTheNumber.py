import math
import random
import simplegui

# initialize the two guess value and one count value
rand_number=0 
guess_number=0
count=1

# the helper functions
def rand100():
    '''
    this function generate the guess number
    '''
    global rand_number, count, game_indicator 
    rand_number=random.randrange(0,100)
    count=7
    game_indicator=0
    print '\n','New Game! Guess range 0-100','\n','Try count remaing is ', count 
    
def rand1000():
    '''
    this function generate the guess number
    '''
    global rand_number, count, game_indicator 
    rand_number=random.randrange(0,1000)
    count=10
    game_indicator=1
    print '\n','New Game! Guess range 0-1000','\n','Try count remaing is ',count    
   
    
def suggestion(input_number):
    ''' 
    this function tells if a right guess is made 
    and calculate the updated count 
    '''
    global rand_number,count,message
    guess_number=float(input_number)
    if guess_number<rand_number and count>=1:
        message= 'Higher!'
        count=count-1
    elif guess_number>rand_number and count>=1:
        message='Lower!'
        count=count-1
    elif guess_number==rand_number and count>=1:
        message= 'Correct!'
        count=0
    else: 
        message=''
        count=0
    print '\n',message
    
def if_new_game(input_number):
    suggestion(input_number)
    print 'Guess is ',input_number
    if message=='Correct!':
        if game_indicator==0:
            rand100() 
        else:
            rand1000()
    elif count<=0 and message is not 'Correct!':
        print 'Try count used up'
        print 'The Number is ', rand_number
        if game_indicator==0:
            rand100() 
        else:
            rand1000()
    elif count>0:
        print 'Try count remaing is ', count
        

        
rand100()   

## contruct the GUI for this game 

# frame 
frame=simplegui.create_frame('Guess The Number',150,150) 
# button-100
frame.add_button('100',rand100,100)
# button-1000
frame.add_button('1000',rand1000,100)
# enter the guess number 
frame.add_input('Your Guess Number',if_new_game,100)

# start the frame 
frame.start()


