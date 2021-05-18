from sense_hat import SenseHat, ACTION_RELEASED #Importing Predefined module from sense_hat
import time #importing time module from sense_hat

mySense = SenseHat()                                              #creating object from SenseHat() with the variable mySense
mySense.clear()                                                         #clearing the Raspberry Pi matrix (Dead cells are displayed as LEDs turned off. The game starts with a blank board (all cells are "dead")
global cursor_position_x, cursor_position_y, start_pts, press_count, total_run, start_play              #declaring Global Variables to be used throughout the program
cursor_position_x = 0                                                #cursor_position_x to give the x-coordinate of the cell
cursor_position_y = 0                                                #cursor_position_y to give the y-coordinates of the cell
start_pts = [[],[]]                                                          # for cells with which we are initially choosing as live
press_count = 0                                                         #for counting the number of times the user presses on the LED(Once the player pushes the joystick down three times in succession,simulation should start)
total_run = 0                                                               #flag for checking if the joystick is pressed down while the simulation is going on so that the program can be terminated
start_play = 0                                                             #flag for checking if the simulation has started.

red = [255,0,0]                                                          #RGB Values 
green = [0,255,0]
black = [0,0,0]

# Start of the game with the "cursor" on the pixel at the top left corner of the LED matrix as red.
mySense.set_pixel(cursor_position_x,cursor_position_y,red)

#this function is used throughout the program for checking all the points on the 8x8 LED matrix to see if that particular cell is already present within the set of all_pts or not.
#It is first iterating the loop for the rows .If the row is present, it checks for the corresponding  point for column from the matrix values
#If it is present, the is_there flag is reinitialized to True and returned back to the calling function.

def check_if_green(position_x,position_y,all_pts):
  is_there = False
  if 0<= position_x <= 7 and 0<= position_y <= 7:
    for i in range(len(all_pts[0])):
      if position_x == all_pts[0][i]:
        if position_y == all_pts[1][i]:
          is_there = True
  return is_there



#if the user presses the joystick left,this function is called.
def cursor_left(event):

  if event.action != ACTION_RELEASED:
    global cursor_position_x, cursor_position_y, start_pts, press_count
    press_count = 0
    if not check_if_green(cursor_position_x,cursor_position_y,start_pts):
      mySense.set_pixel(cursor_position_x,cursor_position_y,black)              #if the present point is not green already, it will be visualized as black,if it is green, there will be no change.
    cursor_position_x = cursor_position_x - 1                                                  
    if cursor_position_x < 0 :                                                                          
      cursor_position_x = 7                                                                                   #wrapping around the position of the cursor
    if not check_if_green(cursor_position_x,cursor_position_y,start_pts):      
      mySense.set_pixel(cursor_position_x,cursor_position_y,red)                  #if the new point is green, the cursor will not be visible, if not green, it will appear as a red dot.


#if the user presses the joystick right,this function is called.
#structure is same as cursor_left(event)
def cursor_right(event):

  if event.action != ACTION_RELEASED:
    global cursor_position_x, cursor_position_y, start_pts, press_count
    press_count = 0
    if not check_if_green(cursor_position_x,cursor_position_y,start_pts):
      mySense.set_pixel(cursor_position_x,cursor_position_y,black)
    cursor_position_x = cursor_position_x + 1
    if cursor_position_x > 7 :
      cursor_position_x = 0
    if not check_if_green(cursor_position_x,cursor_position_y,start_pts):
      mySense.set_pixel(cursor_position_x,cursor_position_y,red)


#if the user presses the joystick down,this function is called.
#structure is same as cursor_left(event)

def cursor_down(event):
   if event.action != ACTION_RELEASED:
    global cursor_position_x, cursor_position_y, start_pts, press_count
    press_count = 0
    if not check_if_green(cursor_position_x,cursor_position_y,start_pts):
      mySense.set_pixel(cursor_position_x,cursor_position_y,black)
    cursor_position_y = cursor_position_y + 1
    if cursor_position_y > 7 :
      cursor_position_y = 0
    if not check_if_green(cursor_position_x,cursor_position_y,start_pts):
      mySense.set_pixel(cursor_position_x,cursor_position_y,red)

#if the user presses the joystick up,this function is called.
#structure is same as cursor_left(event)

def cursor_up(event):

  if event.action != ACTION_RELEASED:
    global cursor_position_x, cursor_position_y, start_pts, press_count
    press_count = 0
    if not check_if_green(cursor_position_x,cursor_position_y,start_pts):
      mySense.set_pixel(cursor_position_x,cursor_position_y,black)
    cursor_position_y = cursor_position_y - 1
    if cursor_position_y < 0 :
      cursor_position_y = 7
    if not check_if_green(cursor_position_x,cursor_position_y,start_pts):
      mySense.set_pixel(cursor_position_x,cursor_position_y,red)

#this function helps in recognizing the neighbouring green cells around any particular point.The number of green cells is then appended to n_count.
#There are total 8 cells around a point and hence 8 coordinates are checked.

def find_neig_count(x,y,live_cells):
    n_count = 0

    if check_if_green(x+1,y,live_cells):
        n_count = n_count + 1

    if check_if_green(x-1,y,live_cells):
        n_count = n_count + 1

    if check_if_green(x,y+1,live_cells):
        n_count = n_count + 1

    if check_if_green(x,y-1,live_cells):
        n_count = n_count + 1

    if check_if_green(x+1,y+1,live_cells):
        n_count = n_count + 1

    if check_if_green(x+1,y-1,live_cells):
        n_count = n_count + 1

    if check_if_green(x-1,y-1,live_cells):
        n_count = n_count + 1

    if check_if_green(x-1,y+1,live_cells):
        n_count = n_count + 1

    return n_count

# This function starts the simulation and is called recursively to keep the simulation running.

def play_game(live_cells):
  global total_run, start_play, press_count
  death_list = []                                                    #stores the index of the dead cell
  birth_list = [[],[]]                                                 #stores the coordinates of live cells
  start_play = 1

  for i in range(len(live_cells[0])):
      x = live_cells[0][i]
      y = live_cells[1][i]
      n_count = find_neig_count(x,y,live_cells)
      if (n_count < 2) or (n_count > 3):                #Any live cell with less than 2 and more than 3 live neighbours dies
          death_list.append(i)

  n_count =  0
  for i in range(len(live_cells[0])):
      x = live_cells[0][i]
      y = live_cells[1][i]


      n_count = find_neig_count(x+1,y,live_cells)   #checking the neighbouring 8 points around one point except that particular point.There are 8 if statements.
      if n_count ==3:                                                 #It then appends the coordinates of the point which will be born based on the value of n_count.A dead cell with three live neighbours becomes a live cell
          if not check_if_green(x+1,y,birth_list):
              birth_list[0].append(x+1)
              birth_list[1].append(y)


      n_count = find_neig_count(x-1,y,live_cells)
      if n_count ==3:
          if not check_if_green(x-1,y,birth_list):
              birth_list[0].append(x-1)
              birth_list[1].append(y)


      n_count = find_neig_count(x,y+1,live_cells)
      if n_count ==3:
          if not check_if_green(x,y+1,birth_list):
              birth_list[0].append(x)
              birth_list[1].append(y+1)

      n_count = find_neig_count(x,y-1,live_cells)
      if n_count ==3:
          if not check_if_green(x,y-1,birth_list):
              birth_list[0].append(x)
              birth_list[1].append(y-1)


      n_count = find_neig_count(x+1,y+1,live_cells)
      if n_count ==3:
          if not check_if_green(x+1,y+1,birth_list):
              birth_list[0].append(x+1)
              birth_list[1].append(y+1)

      n_count = find_neig_count(x+1,y-1,live_cells)
      if n_count ==3:
          if not check_if_green(x+1,y-1,birth_list):
              birth_list[0].append(x+1)
              birth_list[1].append(y-1)

      n_count = find_neig_count(x-1,y-1,live_cells)
      if n_count ==3:
          if not check_if_green(x-1,y-1,birth_list):
              birth_list[0].append(x-1)
              birth_list[1].append(y-1)

      n_count = find_neig_count(x-1,y-1,live_cells)
      if n_count ==3:
          if not check_if_green(x-1,y-1,birth_list):
              birth_list[0].append(x-1)
              birth_list[1].append(y-1)

  for i in range(len(live_cells[0])):   #if the cell is not in death_list or in the new birth_list are appended to the birth_list.(for cells which are live and will continue to live in the next generation.
    if i not in death_list:

        birth_list[0].append(live_cells[0][i])
        birth_list[1].append(live_cells[1][i])

  mySense.clear()                           #The simulation proceeds with one new generation/tick once every second,

  for i in range(len(birth_list[0])):
    new_X = birth_list[0][i]
    new_Y = birth_list[1][i]
    mySense.set_pixel(new_X,new_Y,green)   #lighting up the cells

  time.sleep(1)
  for event1 in mySense.stick.get_events():


    if (event1.direction == 'middle') and (event1.action == 'pressed'):    #The simulation ends only once the player presses the joystick down again.
      total_run = 1
  if total_run == 1:

    birth_list = [[],[]]                                                 #if flag value changes,screen and birth_list is cleared.
    mySense.clear()
    press_count = 0
    
  else:
    if len(birth_list[0]) != 0:

        play_game(birth_list)                                    #calls recursively



def single_press(event):

  if event.action != ACTION_RELEASED:
    global cursor_position_x, cursor_position_y,start_pts, press_count, start_play, total_run
    if start_play == 0:
      press_count = press_count + 1
      if press_count == 1:


        if check_if_green(cursor_position_x,cursor_position_y,start_pts) :
           for i in range(len(start_pts[0])):

            if cursor_position_x == start_pts[0][i]:
              if cursor_position_y == start_pts[1][i]:

                del start_pts[0][i]                                             #This is an additional feature.If the player goes back to a live cell selected previously and clicks again 
                del start_pts[1][i]                                                         #the cell will be unselected and turn dead again
                mySense.set_pixel(cursor_position_x,cursor_position_y,red)
                break
        else:
          mySense.set_pixel(cursor_position_x,cursor_position_y,green)
          start_pts[0].append(cursor_position_x)
          start_pts[1].append(cursor_position_y)
      if press_count == 3:                                                         # game starts after 3 presses on a single point.

        play_game(start_pts)
    else:
      mySense.clear()
      total_run = 1



#takes joystick input

mySense.stick.direction_left = cursor_left
mySense.stick.direction_right = cursor_right
mySense.stick.direction_down = cursor_down
mySense.stick.direction_up = cursor_up
mySense.stick.direction_middle = single_press


while True:                                    #endless loop
  if press_count != 3:
    time.sleep(2)
    press_count = 0

  temp = 0

  if total_run == 1:     #breaks the loop and terminates the program when the value of flag which is responsible for checking the press from the joystick while simulation is running,changes
    break

  pass
