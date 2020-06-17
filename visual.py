
import time,os,sys

def print_new_lines(num):
  for i in range(0,num):
      print("\n", end='')

def pause(x):
  time.sleep(x)

def clear():
  os.system('clear')

def outline(x):
  temp_row = ""
  for x in range(0,x):
    temp_row += "="
  print_new_lines(1)
  print(temp_row,end='')
  print_new_lines(1)

# Created by Jan Vorcak from Stack Overflow
def read_text(str):
  # Creates a "typewriter" effect while printing out a str
  # Note: Player can type anything while this function is still executing
  for letter in str:
    if letter in [",", ".", "!"]:
      pause(0.3)
    else:
      pause(0.04)
    sys.stdout.write(letter)
    sys.stdout.flush()
  
def read(lines,start,end):
  for i in range(start,end+1):
    read_text(lines[i])
    pause(1)
    clear()    

def view_stats(name,currentHP,maxHP,baseAtk,isPlayer,level ="none",currentXP="none",baseXP="none"):
  # Views stats for player, monster, and boss
  if isPlayer == True:
    outline(55)
    print(name,"   LVL",level,"   XP",currentXP,"/",baseXP,"    HP",currentHP,"/",maxHP,"    ATK",baseAtk,end = '')
    outline(55)
  else:
    outline(55)
    print(name,"    HP",currentHP,"/",maxHP,"    ATK",baseAtk,end = '')
    outline(55)