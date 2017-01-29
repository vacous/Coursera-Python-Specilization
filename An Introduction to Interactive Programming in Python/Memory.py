# -*- coding: utf-8 -*-
"""
Created on Sat Jan 28 23:18:14 2017

@author: Administrator
"""

# implementation of card game - Memory

import simplegui
import random

last_two_value=[]
last_two_position=[]



point_list=[]
turn_count=0
value=range(16)
for n in range(0,16):
    point_list.append([value[n],0,0])
# there are 3 values in for each data point [value, click_ind, match_ind]
# generate the list for all the points 
# when mouse click the card, the click indicator becomes 1 
# when two card number matches, the match indicator becomes 1 
# click indicators of all points are reseted after 2 clicks


# helper function to initialize globals
def new_game():
    global point_list,value,turn_count
    turn_count=0
    label.set_text('Turn='+str(turn_count))
    point_list=[]
    value=range(8)*2
    value_list=random.shuffle(value) 
    for n in range(0,16):
        point_list.append([value[n],0,0])
     
def mouseclick(pos):
    global click_count,last_two_value,last_two_position,point_list,turn_count,a
    point_location=int(pos[0]) // 50
    clicked_point=point_list[point_location]
    active_count=0
    for point in point_list:
        if point[1]==1:
            active_count +=1
    
    
    if clicked_point[2]!=1:
        last_two_value.append(clicked_point[0])
        last_two_position.append(point_location)
    
    if len(last_two_position)<2:            
        if clicked_point[2]!=1:
            clicked_point[1]=1

            
    elif len(last_two_position)==2: 
        if last_two_position[0] != last_two_position[1] and clicked_point[2]!=1:
            clicked_point[1]=1
            if last_two_value[0]==last_two_value[1]:
                point_list[last_two_position[0]][2]=1
                point_list[last_two_position[1]][2]=1
            turn_count+=1          
        elif last_two_position[0] == last_two_position[1]:
            last_two_position.pop(-1)
            last_two_value.pop(-1)
    elif len(last_two_position)>2:
        for point in point_list:
            point[1]=0
            last_two_value=[clicked_point[0]]
            last_two_position=[point_location]
            if clicked_point[2]!=1:
                point_list[point_location][1]=1

        
    
            
                
                      

    label.set_text('Turn='+str(turn_count))
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    for n in range(0,16):
        canvas.draw_text(str(value[n]), ((n)*50+25, 50), 15, 'Red')
        if point_list[n][1]!=1 and point_list[n][2]!=1:  
            canvas.draw_polygon([((n)*50, 0), ((n)*50, 100), ((n+1)*50, 100),((n+1)*50,0)], 1, 'black','green')
        # create frame and add a button and labels
        
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)

label = frame.add_label('Turn='+str(turn_count))

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric