
import random

from visual import print_new_lines, outline

def generate_dungeon():
  # TODO: Add parameters to customize dungeon size and randomize the position of the boss room
  dungeon = []
  temp_row = []
  for row in range(0,4):
    for col in range(0,4):
      i = 0
      temp_row.append(i)
      # Generates an extra tile for boss room
      if row == 3 and col == 3:
        temp_row.append(0)
    dungeon.append(temp_row)
    temp_row = []
  temp_row.append(0)
  dungeon.append(temp_row)
  temp_row = []
  return dungeon

def print_dungeon(dungeon,player_pos1,player_pos2,treasure_pos):
  # Takes in the lists and prints out dungeon
  outline(30)
  print("THE DUNGEON")
  print_new_lines(1)
  temp_row = ""
  for row in range(0,len(dungeon)):
    for col in range(0,len(dungeon[row])):
      if row == player_pos1 and col == player_pos2:
        dungeon[row][col] = 1
         # Uses player_pos and treasure_pos to mark them on the dungeon
        if row == 3 and col == 3:
          temp_row += "[ X ]️🗝️"
        elif row == 3 and col == 4:
          temp_row += " [ X  ☠ ]"
        else:
          temp_row += "[ X ]"
      else:
        if dungeon[row][col] == 0:
          temp_row += "     "
        elif (row,col) in treasure_pos:
          temp_row += "[ 🗝️ ]"
        elif row == 3 and col == 3:
          temp_row += "[ - ]🗝️"
        else:
          temp_row += "[ - ]"
    print(temp_row)
    temp_row = ""
  outline(30)
  print_new_lines(1)

def generate_events(num_of_loops,pos_list):
  # Creates spawn positions for monsters, traps, and treasure and puts it in a list
  # Reccomended number of loops are 8
  # X number_of_loops == X monsters/treasure/trap
  pos_list = []
  x = 0
  while x < num_of_loops:
    temp_position = 0 
    pos1 = random.randint(0,3)
    pos2 = random.randint(0,3)
    # TODO: Make sure events don't overlap
    while (pos1,pos2) in pos_list:
      pos1 = random.randint(0,3)
      pos2 = random.randint(0,3)
    temp_position = (pos1,pos2)
    pos_list.append(temp_position)
    x += 1
  return pos_list

def remove_events(player_pos1,player_pos2,event):
  # Prevents overlaps in events
  if (player_pos1,player_pos2) in event:
    event.remove((player_pos1,player_pos2))