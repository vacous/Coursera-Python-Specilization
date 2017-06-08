# The stop watch game 

import simplegui

# initialize the variables 
# clock a:bc.d
a=0
b=0
c=0
d=0
count=0
message='0:00.0'
count_success=0
count_attempt=0
repeat_indicator=0

# helper function 
def digit_inc():
    global a,b,c,d,count, message 
    d=count % 10
    if d==9:
        c=c+1
    if c==10:
        b=b+1
        c=0
    if b==6:
        a=a+1
        b=0
    message= str(a)+':'+str(b)+str(c)+'.'+str(d) 
    return
        
# button handler 
# start - new timer 
# stop - stop the timer 
# reset - all value to zero 
# canvas, 1. clock 2. success/attempt


def timer_action():
    global count 
    count=count+1
    digit_inc()
    return 


def start():
    global repeat_indicator
    timer.start()
    repeat_indicator=0
    return

def stop():
    global count_success, count_attempt, repeat_indicator
    timer.stop()
    
    if d==0: 
        if repeat_indicator !=1 and sum([a,b,c,d])!=0:
            count_success +=1 
    else:
        if repeat_indicator !=1:
            count_attempt +=1
    repeat_indicator=1
    return

def reset():
    global a,b,c,d,count,count_success,count_attempt,message
    a=0
    b=0
    c=0
    d=0
    count=0
    count_success=0
    count_attempt=0
    message='0:00.0'
    timer.stop()
    return 


def disp(canvas):
    canvas.draw_text(message, (125, 275), 100, 'Red')
    canvas.draw_text(str(count_success)+'/'+str(count_attempt), (350, 100), 80, 'Green')

# reg
timer = simplegui.create_timer(100, timer_action)    
    
frame=simplegui.create_frame('Stop Clock',500,500)
frame.add_button('Start',start,100)
frame.add_button('Stop',stop,100)
frame.add_button('Reset',reset,100)


frame.set_draw_handler(disp)

# start 
frame.start()


    
    