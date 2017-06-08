# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400     
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
time=[0,0]
time_inc=[0.005,0.005]

right=[1,-1]
left=[-1,-1]

ball_pos=[300,200]
ball_vel=[0,0]

left_pad_vel=0
right_pad_vel=0

left_pad_pos=[HALF_PAD_WIDTH,HALF_PAD_HEIGHT]
right_pad_pos=[WIDTH-HALF_PAD_WIDTH,HALF_PAD_HEIGHT]

temp_pos=0

col_indicator=0
pad_in=0
pad_speed=3.5

right_point=0
left_point=0

initial_direction=[1,-1]

# help function
def list_add(list1,list2):
        result_list=[0]*len(list1)
        for i in range (0,len(list1)):
            result_list[i]=list1[i]+list2[i]
        return result_list 
    
def list_multiply(list1,list2):
        result_list=[0]*len(list1)
        for i in range (0,len(list1)):
            result_list[i]=list1[i]*list2[i]
        return result_list 
    
    
def restart():
    global ball_pos, ball_vel,right_point,left_point
    timer.stop()
    ball_pos=[300,200]
    ball_vel=[0,0]
    right_point=0
    left_point=0
    timer.stop()
    new_game()
    return
    
def timer_handler():
    global ball_pos, ball_vel, time
    time=list_add(time,time_inc)
    collide()
    ball_pos=list_add(ball_pos,list_multiply(ball_vel,time_inc))

def paddle_hit():
    global ball_vel, left_point, right_point,ball_pos, initial_direction 
    # for the left paddle 
    if col_indicator== -1:
        if ball_pos[1]<=left_pad_pos[1]+HALF_PAD_HEIGHT and ball_pos[1]>=left_pad_pos[1]-HALF_PAD_HEIGHT:
            left_point = left_point+1 
            ball_vel=list_multiply(ball_vel,[1.1,1.1])
            initial_direction=left
        else: 
            ball_pos=[300,200]
            ball_vel=[random.randrange(120, 240),random.randrange(60, 180)]
            ball_vel=list_multiply(ball_vel,initial_direction)
            right_point = right_point+1
            initial_direction=right
            timer.start()
            
    if col_indicator== 1:
        if ball_pos[1]<=right_pad_pos[1]+HALF_PAD_HEIGHT and ball_pos[1]>=right_pad_pos[1]-HALF_PAD_HEIGHT:
            right_point = right_point+1
            ball_vel=list_multiply(ball_vel,[1.1,1.1])
            initial_direction=right
        else: 
            ball_pos=[300,200]
            ball_vel=[random.randrange(120, 240),random.randrange(60, 180)]
            ball_vel=list_multiply(ball_vel,initial_direction)
            left_point = left_point+1
            initial_direction=left
            timer.start()
           
    #print right_point,initial_direction,ball_vel
    
# button hold timer

def timer_left_w():
    global left_pad_pos, left_pad_vel
    left_pad_vel= -pad_speed
    if left_pad_pos[1]-HALF_PAD_HEIGHT+left_pad_vel >= 0:  
            left_pad_pos[1]=left_pad_pos[1]+ left_pad_vel               
    return 

def timer_left_s():
    global left_pad_pos, left_pad_vel
    left_pad_vel= pad_speed
    if left_pad_pos[1]+HALF_PAD_HEIGHT-left_pad_vel <= HEIGHT:
            left_pad_pos[1]=left_pad_pos[1]+ left_pad_vel     
    return 

def timer_right_up():
    global right_pad_pos, right_pad_vel
    right_pad_vel= -pad_speed
    if right_pad_pos[1]-HALF_PAD_HEIGHT+right_pad_vel >= 0:
            right_pad_pos[1]=right_pad_pos[1]+ right_pad_vel                
    return 

def timer_right_down():
    global right_pad_pos, right_pad_vel
    right_pad_vel= pad_speed
    if right_pad_pos[1]+HALF_PAD_HEIGHT-right_pad_vel <= HEIGHT:
        right_pad_pos[1]=right_pad_pos[1]+ right_pad_vel
    return 

timer=simplegui.create_timer(2,timer_handler)  
timer_left_s=simplegui.create_timer(1,timer_left_s)
timer_left_w=simplegui.create_timer(1,timer_left_w)

timer_right_up=simplegui.create_timer(1,timer_right_up)
timer_right_down=simplegui.create_timer(1,timer_right_down)

timer_point=simplegui.create_timer(2,paddle_hit)


def keydown(key):
    global left_pad_vel, right_pad_vel, left_pad_pos, right_pad_pos, temp_pos 

    if key == simplegui.KEY_MAP["w"]:
        timer_left_w.start()
    elif key == simplegui.KEY_MAP["s"]:
        timer_left_s.start()
    elif key == simplegui.KEY_MAP["up"]:
        timer_right_up.start()
    elif key == simplegui.KEY_MAP["down"]:
        timer_right_down.start()
    return 

def keyup(key):
    global left_pad_vel,right_pad_vel
    if key == simplegui.KEY_MAP["w"]:
        timer_left_w.stop()
    elif key == simplegui.KEY_MAP["s"]:
        timer_left_s.stop()
    elif key == simplegui.KEY_MAP["up"]:
        timer_right_up.stop()
    elif key == simplegui.KEY_MAP["down"]:
        timer_right_down.stop()
    return 


# define the collide function 
def collide():
    global ball_pos, col_indicator
    # boundary collision
    if (ball_pos[1]+BALL_RADIUS) > HEIGHT or (ball_pos[1]-BALL_RADIUS) < 0:
        ball_vel[1]=-ball_vel[1]
    elif (ball_pos[0]+BALL_RADIUS) > (WIDTH-PAD_WIDTH):
        ball_vel[0]=-ball_vel[0]
        col_indicator=1 #right
    elif (ball_pos[0]-BALL_RADIUS) < PAD_WIDTH:
        ball_vel[0]=-ball_vel[0]
        col_indicator=-1 #left
    else: 
        col_indicator=0
    #print col_indicator
    
    

# initialize ball_pos and ball_vel for new bal in middle of table


# define event handlers
def new_game():
    global ball_pos, ball_vel  # these are numbers
    ball_vel=[random.randrange(120, 240),random.randrange(60, 180)]
    initial_direction=random.choice([left,right])
    ball_vel=list_multiply(ball_vel,initial_direction)
    timer.start()
    
    

def draw(canvas):
    global score1, score2, right_pad_pos, left_pad_pos, ball_pos, ball_vel
    canvas.draw_circle(ball_pos,20,1,'white','blue')
    
    
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_text(str(left_point), (40, 40), 30, 'Red')
    canvas.draw_text(str(right_point), (550, 40), 30, 'Red')

    #left_pad_pos[1]=left_pad_pos[1]+ left_pad_vel
    #right_pad_pos[1]=right_pad_pos[1]+ right_pad_vel
            
    canvas.draw_polygon([(left_pad_pos[0]-HALF_PAD_WIDTH, left_pad_pos[1]+HALF_PAD_HEIGHT), (left_pad_pos[0]+HALF_PAD_WIDTH, left_pad_pos[1]+HALF_PAD_HEIGHT), (left_pad_pos[0]+HALF_PAD_WIDTH, left_pad_pos[1]-HALF_PAD_HEIGHT), (left_pad_pos[0]-HALF_PAD_WIDTH, left_pad_pos[1]-HALF_PAD_HEIGHT)], 1, 'Green','green')
    canvas.draw_polygon([(right_pad_pos[0]-HALF_PAD_WIDTH, right_pad_pos[1]+HALF_PAD_HEIGHT), (right_pad_pos[0]+HALF_PAD_WIDTH, right_pad_pos[1]+HALF_PAD_HEIGHT), (right_pad_pos[0]+HALF_PAD_WIDTH, right_pad_pos[1]-HALF_PAD_HEIGHT), (right_pad_pos[0]-HALF_PAD_WIDTH, right_pad_pos[1]-HALF_PAD_HEIGHT)], 1, 'Green','green')   


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.add_button('new game',new_game,100)
frame.add_button('Restart',restart,100)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)


# start frame
frame.start()
timer_point.start()
