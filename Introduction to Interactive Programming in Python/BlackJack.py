# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# All possible combination: the cards available
CARD_POOL_AVA=[]

for suit in SUITS:
    for rank in RANKS:
        CARD_POOL_AVA.append([rank,suit])
        
CARD_POOL_ALL=tuple(CARD_POOL_AVA)        

# event indicators 
end_indicator = 0
stand_indicator =0 

player_score=0
dealer_score=0

message= 'Deal Cards?'

# define card class
class Card:
    def __init__(self, card):
        if (card[1] in SUITS) and (card[0] in RANKS):
            self.suit = card[1]
            self.rank = card[0]
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)

# define hand class
class Hand:
    def __init__(self):
        self.hold = [] # the card already in hand 
        self.value = 0 # the total value of the card in hand 
        
    def __str__(self):
        output = self.hold 
        return output 
    
    def add_card(self):
        new_card = random.choice(CARD_POOL_AVA)
        CARD_POOL_AVA.remove(new_card)
        self.hold.append(new_card) 
        return self.hold 

    def get_value(self):
        value_hold=[]
        total_value=0
        
        for card in self.hold:
            value_hold.append(VALUES[card[0]])    
        total_value= sum(value_hold)
                
        if total_value <= 11 and (1 in value_hold):
            total_value = total_value + 10
        
        self.value = total_value
        return self.value    
    
    def reset(self):
        self.hold = []
        self.value = 0
   
    def draw(self, canvas,i):
        for card in self.hold:
            index = self.hold.index(card)
            Cards = Card(card)
            Cards.draw(canvas, [50+index*50, 100*i])


# Two side, player and the dealer 
player = Hand()
dealer = Hand()
   
    
# helper function 
def judge(value1,value2):
    global dealer_score, player_score, message
    global end_indicator 
    
    if value1>21:
        dealer_score +=1
        message = 'You busted, You lost, Deal?'
        end_indicator = 1 
    elif value2>21:
        player_score +=1
        message = 'Dealer busted, You won, Deal?'
        end_indicator = 1
    elif value1<=21 and value2<=21:
        if value1>value2:
            player_score +=1
            message = 'You won this round, Deal?'
            end_indicator = 1
        else:
            dealer_score +=1 
            message = 'You lost this round, Deal?'
            end_indicator = 1
        
        
    
  
# event handler 

def new_game(): 
    global dealer_score
    global CARD_POOL_AVA, message
    global stand_indicator, end_indicator 
    
    # if game is still on the dealer get score
    if end_indicator ==0 and player.get_value() !=0:
        dealer_score += 1
        message = 'Deal in the middle of game, Dealer got 1 point'
    else: 
        message='Hit or Stand?'
     
    
    CARD_POOL_AVA = list(CARD_POOL_ALL)
    stand_indicator = 0
    end_indicator = 0 
 
    player.reset()
    dealer.reset()
    
    player.add_card()
    dealer.add_card()
    player.add_card()
    dealer.add_card()
    
        

def hit():
    if end_indicator == 0 and player.get_value() !=0 :
        player.add_card()
        judge(player.get_value(),dealer.get_value)

def stand():
    global stand_indicator 
    
    # have card and stand not pressed 
    if stand_indicator == 0 and end_indicator ==0 and player.get_value() != 0:
        stand_indicator = 1 
        
        while dealer.get_value()<17:
            dealer.add_card()
        judge(player.get_value(),dealer.get_value())
    
    
    
    
        


def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    
    #available card
    card = Card(random.choice(CARD_POOL_AVA))
    card.draw(canvas, [480, 480])
    
    

    
    
    
    
    player.draw(canvas,4)
    dealer.draw(canvas,1)
    
    # cover card 
    if end_indicator == 0 and player.get_value()!=0:
        pos=[50,100]
        card_loc = (CARD_CENTER[0], CARD_CENTER[1])
        canvas.draw_image(card_back, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
    
    # title 
    canvas.draw_text('BlackJack', (220, 50), 30, 'Red')
    
    # message	   
    canvas.draw_text(str(message), (20, 80), 15, 'Red')
    canvas.draw_text('Available Cards', (460, 450), 15, 'Red')
    
    # scores
    canvas.draw_text('Player Score  '+str(player_score), (440, 40), 12, 'red')
    canvas.draw_text('Dealer Score  '+str(dealer_score), (440, 60), 12, 'red')
    
    # Dealer or Player
    canvas.draw_text('Dealer', (20, 230), 15, 'white')
    canvas.draw_text('Player', (20, 520), 15, 'white')
    
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("black")
frame.add_button("Deal", new_game, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)

frame.set_draw_handler(draw)
frame.start()