
import math,random

from visual import print_new_lines, pause, clear, outline,read_text, read, view_stats

from dungeon import generate_dungeon, print_dungeon,generate_events, remove_events



## GLOBAL VARIABLES ##
# TODO: Remove all global variables from functions


# Checks if a player is in a dungeon or has died
# Or equipped an item
# Set it to TRUE, TRUE, FALSE, FALSE
game_state = True
in_dungeon = True
player_died = False
player_equipped = False

# Checks if the player is in a battle with a monster or boss
# Or if it is in a inventory or shop
# Set it all to FALSE
in_monster_fight = False
in_inventory = False
in_shop = False

# Determines the next monster the player will encounter
# TODO: Create dictionary of dungeons
# EX: 1: [slime,skeleton]
#     2: [differentMonster1]
monster_index = 0
boss_index = 0
# Stores all the tuples for monster positions
monster_positions = []
treasure_positions = []
trap_positions = []
locked_positions = [(3,4)]
boss_position = (3,4)

# Stores all the monsters in the game

class Items:
  '''Represents Items'''
  def __init__(self,name,desc,dropChance,buff,buffName,value,consumable,equippable,quantity,shopQuantity,itemId):
    self.name = name
    self.description = desc
    self.dropChance = dropChance
    self.buff = buff
    self.buffName = buffName
    self.value = value
    self.consumable = consumable
    self.equippable = equippable
    self.quantity = quantity
    self.shopQuantity = shopQuantity
    self.itemId = itemId

woodenSword = Items(
  "WOODEN SWORD",
  "Nothing fancy but it gets the job done. If you are playing pretend that is.",
  .1,
  1, # +1 BASE ATTACK
  "ATTACK",
  50,
  False,
  True,
  0,
  2,
  0
)
healthPotion = Items(
  "HEALTH POTION",
  "Not FDA approved...", 
  .66, 
  4, # +4 HEALTH
  "HEALTH",
  20,
  True,
  False,
  0,
  3,
  1
)
key = Items(
  "KEY",
  "It can be used to unlock rooms and treasure chests.",
  .75,
  0,
  "OTHER",
  20,
  True,
  False,
  0,
  3,
  2
)

cheapSword = Items(
  "CHEAP SWORD",
  "Mass-produced by a heartless corporation. Support your local blacksmith instead.",
  0,
  3,
  "ATTACK",
  80,
  False,
  True,
  0,
  1,
  3
)

# Items that are exclusive to a specific type of monster
slimeSword = Items(
  "SLIME SWORD",
  "The metal of this sword has been stained green by the slime's insides. It also becomes luminesent.",
  .05,
  2, # +2 BASE ATTACK
  "ATTACK",
  50,
  False,
  True,
  0,
  0,
  4
)

drop_list = []
has_dropped_item = False
item_list = [woodenSword,healthPotion,key,slimeSword]
shop_items = [cheapSword,woodenSword,healthPotion,key]

# All the player info and stats

class Player:
  '''Represents Player'''

player = Player()
player.name = ""
player.hometown = ""
player.type = "HUMAN"

player.dungeonsCleared = 0
player.monstersKilled = 0
player.turnsTaken = 0

def nextLevel(level):
  exponent = 1.5
  baseXP = 2
  return math.floor(baseXP * (level * exponent))

player.level = 1
player.currentXP = 0
player.baseXP = nextLevel(player.level)
  
# Stats
player.maxHP = 15
player.currentHP = player.maxHP
player.baseAtk = 2
player.attack = [player.baseAtk-1,player.baseAtk,player.baseAtk+1]
player.critPercentage = 0.05

# Inventory
player.inventory = []
# Note: player.hand should only store one value at a time
player.hand = []
player.gold = 0

# Positioning and directions
# Set to (4,0)
player.position1 = 4 # Row
player.position2 = 0 # Col
player.posDirectionKeys = [] # Possible player input
player.posDirections = [] # Possible directions
player.directions = ["UP","DOWN","LEFT","RIGHT"]

# All actions that a player could make in-game
player.activeActions = ["ATTACK","USE ITEM"]
player.inactiveActions = ["MOVE","VIEW INVENTORY"]
player.inventoryActions = ["USE ITEM","VIEW ITEM","EQUIP ITEM","UNEQUIP ITEM","EXIT"]
player.choices = ["YES","NO"]
player.posItems = []
player.shopActions = ["BUY ITEM","VIEW ITEM","LEAVE SHOP"]

# Stores all the monsters and bosses in the game

class Monster:
  '''Represents Monster'''
  def __init__(self,name,monsterType,maxHP,baseAtk,value,critPercentage,XP):
    self.name = name
    self.monsterType = monsterType
    self.maxHP = maxHP
    self.currentHP = maxHP
    self.baseAtk = baseAtk
    self.attack = [baseAtk-1,baseAtk,baseAtk+1]
    self.value = value
    self.critPercentage = critPercentage
    self.XP = XP

slime = Monster("SLIME","SLIME",3,2,10,0.02,2)
skeleton = Monster("SKELETON","UNDEAD",4,3,20,0.04,3)
king_slime = Monster("KING SLIME","SLIME",14,2,40,0.06,5)

monster_list = [slime,skeleton]
boss_list = [king_slime]

# Stores all the narrator lines when they do not print out variables

class NarratorLines:
  '''represents Narrator's lines'''

narrator_lines = NarratorLines()

narrator_lines.prologue = [
  "Before we start, what is your name?", #0
  "Where do you live?", #1
  "DUNGEONS! Are you ready to embark on this adventure?", #2
  "Good. I welcome you to...", #3
  "THE CRAWLER OF THE DUNGEON!!" #4
]
narrator_lines.story = [
  "At the village, you were walking to your parent's house, doing some daily errands, when to your right you see a crowd of people surrounding the village square.", #0

  "You walk to the square to look at what was happening. You notice that the people were surronding the Knights of Arion, the city that governs your village and the villages around it.", #1

  "The knights announced that they have been fighting off monsters at the city, but do not know where they came from. They asked the people for any voluneers to visit a dungeon nearby, to look at what's going on. People looked at eachother and murmmured. No one was willing to go.", #2

  "One person from the crowd asked why they would they ask them for volunteers if the knights could go there themselves. They ignored his remark.", #3

  "Out of intuition, you forced your way to the front of the crowd and raised your hand. People stared at you as they continued to murmmur. You have no experience in fighting monsters, but you wanted an adventure. Anything that will let you out of this boring village. You also knew that no one in this village would have the guts to fight monsters.", #4

  "The knights looked down upon you from thier steeds and commanded you to come along.", #5

  "You arrived in front of the the dungeon, not so far away at the village. Your surroundings were full of trees and shrubs. The knights told you to go in there and see if there are any monsters in it.", #6

  "Without another word, they left you behind. You turn back to the large entrance of the dungeon, feeling the rush of cold air." #7
]
narrator_lines.general = [
  "What would you like to do? ", #0
  "Invalid action. Try again.", #1
  "Which way? ", #2
]
narrator_lines.trap = [
  "you stepped on a pressure plate that triggered an arrow to fly towards you!", #0
  "spikes came up from the ground in front of you!", #1
  "a giant axe came from the ceiling above you!", #2
  "you tripped and almost fell into a spike pit!", #3
]
narrator_lines.inactive = [
  "You walk into a dimly lit room made of ancient stone blocks." #0
]
narrator_lines.inventory = [
  "You have nothing in your inventory", #0
  "You have...", #1
  "But, you have nothing else in your inventory.", #2
  "You have nothing equipped in your hand.",
]
narrator_lines.dead = [
  "You have died. ", #0
  # If you cleared less than 20 dungeons
  "You did well for a beginner. ", #1
  "You were one of the high and mighty, only to die in a whimper. ", #2 # If you cleared more than 20 dungeons
  "What a shame. I was starting to like you. ", #3
  "If you want to continue your journey, you must start a new life to become... ", #4
  "THE CRAWLER OF THE DUNGEON. " #5
]
narrator_lines.shop = [
  "Later in the day, you visit a small old shop near the center of the village, as the shopkeeper welcomed you in.", #0
  "He offers you some items that will help you for your journey.", #1
  "You have no gold. You are broke." #2
]



## PROLOGUE FUNCTIONS ##



def get_player_info():
  # Asks for player name and hometown
  for i in range(0,2):
    read_text(narrator_lines.prologue[i])
    if i == 0:
      player.name = input(" ").upper()
    elif i == 1:
      player.hometown = input(" ").upper()
    clear()
    pause(1)
      
def play_prologue():
  global player_input
  # Reads player description (name, type, and hometown)
  read_text("Welcome, " + str(player.name) + " you are a " + str(player.type) + " that lives in a small village called " + str(player.hometown) + ". You are about to enter the world of monsters, dragons, and most importantly...")
  pause(1.5)
  print_new_lines(2)
  read_text(narrator_lines.prologue[2])
  player_input = input(" ")
  clear()
  pause(1)
  read(narrator_lines.prologue,3,4)
  pause(2)
  


## PLAYER INVENTORY SYSTEM ##



def view_inventory():
  global item_list
  global player_input
  # Prints out player inventory
  outline(50)
  # Checks if player has nothing
  if len(player.inventory) == 0 and player.gold == 0 and len(player.hand) == 0:
    read_text(narrator_lines.inventory[0]) # You have nothing.
  else:
    # Lists out all the items the player has
    read_text(narrator_lines.inventory[1]) # You have
    print_new_lines(1)
    read_text(str(player.gold) + " GOLD") 
    print_new_lines(1)
    if len(player.inventory) == 0:
      pause(1.5)
      print_new_lines(1)
      read_text(narrator_lines.inventory[2]) # But, you have nothing else in your inventory
    else:
      for item in player.inventory:
        print_new_lines(1)
        read_text("x"+str(item.quantity)+" "+str(item.name))
        print_new_lines(1)
    print_new_lines(1)
    if player_equipped == True:
      # Prints out what player has equipped in their hand
      read_text("You are equipped with a " + str(player.hand[0].name) + ".")
    else:
      read_text(narrator_lines.inventory[3]) # You have nothing equipped in your hand
  outline(50)
  print_new_lines(1)
  if len(player.inventory) == 0 and len(player.hand) == 0:
    # If there is nothing in their inventory, print other actions, else print out specific actions in the inventory
    choose_action()
  else:
    inventory_actions()

def inventory_actions():
  # Executes all the actions the player can make when they are in their inventoyr
  global in_inventory 
  global player_input
  global player_item
  in_inventory = True
  while in_inventory == True:
    # Goes back to other actions if the inventory is empty
    if len(player.inventory) == 0 and len(player.hand) == 0:
      in_inventory = False
      choose_action()
    else:
      read_text(narrator_lines.general[0]) # What to do?
      print_new_lines(2)
      print_actions(player.inventoryActions)
      check_invalid_input(player.inventoryActions)
      if player_input == 1: # USE ITEM 
        if check_player_inventory(True,False):
          print_items(True,False,False,player.inventory)
          use_item(player_item)
        else:
          read_text("You have no items that can be used.")
          print_new_lines(1)
      elif player_input == 2: # VIEW ITEM 
        print_items(False,False,True,player.inventory)
        view_item(player_item)
      elif player_input == 3: # EQUIP ITEM
        if check_player_inventory(False,True):
          print_items(False,True,False,player.inventory)
          equip_item(player_item)
        else:
          read_text("You have no items that can be equipped.")
          print_new_lines(1)
      elif player_input == 4: # UNEQUIP ITEM
        if len(player.hand) == 1:
          unequip_item(player_item)
        else:
          read_text("You have nothing in your hand.")
          print_new_lines(1)
      elif player_input == 5: # EXIT INVENTORY
        in_inventory = False
        choose_action()
      print_new_lines(1)

def check_player_inventory(condition1,condition2):
  # Filters specific items for the player to use
  # Prevents the user from equipping or using an item that should not be equiped or used
  for item in player.inventory:
    if item.consumable == condition1 and item.equippable == condition2:
      return True
  return False

def print_items(condition1,condition2,condition3,list1):
  # Prints the player's items and asks for which one to apply an action to (use, view, equip)
  global player_input
  global player_item
  if list1 == player.inventory and len(list1) == 0:
    read_text(narrator_lines.inventory[0])
  else:
    print_new_lines(1)
    read_text("Which item? ")
    i = 1
    for item in list1:
      if item.consumable == condition1 and item.equippable == condition2 or condition3:
        print("[" + str(i) + "] " + str(item.name),end=" ")
        i += 1
        player.posItems.append(item)
  print_new_lines(1)
  player_input = int(input(""))
  check_invalid_input(player.posItems)
  player_item = player.posItems[player_input-1]
  player.posItems = []

def use_item(player_item):
  global player_position_tuple
  global locked_positions
  # Uses given item and applies the buffs to the player
  # Currently the player can use items that will give them restored health
  if player_item.buffName == "HEALTH":
    player_item.quantity += -1
    if player_item.quantity == 0:
      player.inventory.remove(player_item)
    player.currentHP += player_item.buff
    print_new_lines(1)
    read_text("You feel better and restored " + str(player_item.buff) + " health!")
    print_new_lines(1)
    # Caps the player's health at max 
    if player.currentHP > player.maxHP:
      player.currentHP = player.maxHP 
  elif player_item.buffName == "OTHER": #KEY
    # Note: There is only one locked position in the game
    # This checks if player is on (3,3)
    # This function converts the tuple to (3,4)
    if (player.position1,player.position2+1) in locked_positions:
      remove_events(player.position1,player.position2,locked_positions)
      print_new_lines(1)
      read_text("You succussfully unlocked the gate!")
      player_item.quantity += -1
      if player_item.quantity == 0:
        player.inventory.remove(player_item)
      print_new_lines(1)
    elif (player.position1,player.position2) in treasure_positions:
      # Generates what's inside chest
      earnedGold = random.randint(20,80)
      treasure_positions.remove((player.position1,player.position2))
      print_new_lines(1)
      read_text("You succussfully unlocked the treasure chest! You found " + str(earnedGold) + " GOLD!")
      item_drop()
      if has_dropped_item == True and flg1 == True:
        print_dropped_items("CHEST")
        print_new_lines(1)
      player.gold += earnedGold
      player_item.quantity += -1
    else:
      read_text("You need to have something to unlock to use the key.")

def view_item(player_item):
  # Views any given item and tells the player what it does
  outline(50)
  print(str(player_item.name))
  print_new_lines(1)
  read_text(str(player_item.description))
  if player_item.buffName == "HEALTH":
    read_text(" Restores +" + str(player_item.buff) + " " + player_item.buffName+" when consumed.")
  elif player_item.buffName == "ATTACK":
    read_text(" Gives +" + str(player_item.buff) + " " + player_item.buffName+" when equipped.")
  outline(50)

def equip_item(player_item):
  # Equips a given item and applies it buff until player unquips it
  global player_equipped
  global player_input
  print_new_lines(1)
  # Checks if the player already has an item in their hand
  if player_equipped == True:
    read_text("This will unequip the " +str(player.hand[0].name)+ " you currently have on your hand.")
    print_new_lines(1)
    read_text("Are you sure you want to equip " + str(player_item.name)+"?")
    print_actions(player.choices)
    if player_input == 1: # Player equips player_item and removes thier hand
      # Removes the item and their buffs from player's hand
      player.baseAtk += -player.hand[0].buff
      player.inventory.append(player.hand[0])
      player.hand[0].quantity += 1
      # Removes item from inventory if they're not the same item
      if player_item.id != player.hand[0].id:
        player.inventory.remove(player_item)
      player_item.quantity += -1
      player.hand.remove(player.hand[0])
      # Equips player_item, applies its buff and removes it from inventory
      player.hand.append(player_item)
      player.baseAtk += player_item.buff
      player.attack = [player.baseAtk-1,player.baseAtk,player.baseAtk+1]
      player_equipped = True
    else:
      inventory_actions()
    # Equips the player_item if the player has nothing in their hand
  elif player_equipped == False: 
    # Equips player_item, applies its buff and removes it from inventory
    player_item.quantity += -1
    player.hand.append(player_item)
    player.inventory.remove(player_item)
    player.baseAtk += player_item.buff
    player.attack = [player.baseAtk-1,player.baseAtk,player.baseAtk+1]
    player_equipped = True
    read_text("You are now equipped with a " + str(player_item.name) + ". It granted you + " + str(player_item.buff) +" "+ str(player_item.buffName)+"!")
    print_new_lines(1)

def unequip_item(player_item):
  # Unequips item from player's hand and removes all its buffs
  global player_equipped
  global player_input
  # Checks if player_item is not in thier hand
  if player_item not in player.hand:
    read_text("This item is not in your hand.")
    print_new_lines(1)
  else:
    # Unequips player_item, removes its buffs, and places it back into the inventory
    player.hand[0].quantity += 1
    player.inventory.append(player.hand[0])
    player.baseAtk += -player.hand[0].buff
    player.attack = [player.baseAtk-1,player.baseAtk,player.baseAtk+1]
    player.hand.remove(player.hand[0])
    player_equipped = False
    read_text("You now unequipped the " + str(player_item.name) + ".")
    print_new_lines(1)



## PLAYER DIRECTION SYSTEM ##



def append_posDirections(direction1 = "None",direction2 = "None",direction3 = "None",direction4 = "None"):
  # Appends given directions into possible directions list
  # Used to append them on console
  possible_directions = [direction1,direction2,direction3,direction4]
  for direction in possible_directions:
    if direction == "None":
      continue
    else:
      player.posDirections.append(direction)

def get_directions(row,col):
  # Takes in player's positions and prints out possible directions
  # Checks where player can go and prevents them from going out of bounds
  UP = player.directions[0]
  DOWN = player.directions[1]
  LEFT = player.directions[2]
  RIGHT = player.directions[3]
  print_new_lines(1)
  player.posDirections = []
  player.posDirectionKeys = []
  if row == 4 and col == 0:
    #SPAWN POINT (UP)
    append_posDirections(UP)
  elif row == 3 and col == 3:
    #GATE TO BOSS ROOM (UP,LEFT,RIGHT)
    append_posDirections(UP,LEFT,RIGHT)
  elif row == 0 and col == 0:
    #TOP LEFT CORNER (DOWN, RIGHT)
    append_posDirections(DOWN,RIGHT) 
  elif row == 0 and col == 3:
    #TOP RIGHT CORNER (DOWN, LEFT)
    append_posDirections(DOWN,LEFT)
  elif row != 0 and row != 4 and col == 0:
    #LEFT SIDE (UP,DOWN,RIGHT)
    append_posDirections(UP,DOWN,RIGHT)
  elif row == 0 and col in [1,2]:
    #TOP SIDE (DOWN, LEFT, RIGHT)
    append_posDirections(DOWN,LEFT,RIGHT)
  elif row == 3 and col in [1,2,3]:
    #BOTTOM SIDE (UP,LEFT, RIGHT)
    append_posDirections(UP,LEFT,RIGHT)
  elif row != 0 and row != 3 and col in [3]:
    #RIGHT SIDE (UP, DOWN, LEFT)
    append_posDirections(UP,DOWN,LEFT)
  else:
    #IN THE MIDDLE
    append_posDirections(UP,DOWN,LEFT,RIGHT)
  for i in range(0,len(player.posDirections)-1):
      player.posDirectionKeys.append(i+1)
  ask_for_direction(row,col)

def ask_for_direction(row,col):
  global player_input
  read_text(narrator_lines.general[2]) # Which way?
  print_actions(player.posDirections)
  check_invalid_input(player.posDirections)
  chosen_direction = player.posDirections[player_input-1]
  print_new_lines(1)
  # Checks if player is at boss gate
  if row == 3 and col == 3 and chosen_direction == "RIGHT" and key not in player.inventory and boss_position in locked_positions:
    read_text("You will need a key to unlock the gate.")
  elif row == 3 and col == 3 and chosen_direction == "RIGHT" and boss_position in locked_positions:
    read_text("Use the key to unlock the gate.")
  elif row == 3 and col == 3 and chosen_direction == "RIGHT" and boss_position not in locked_positions:
    read_text("Get ready...")
    player_movement(chosen_direction)
  else:
    check_invalid_input(player.posDirections)
    player_movement(chosen_direction)
  pause(.8)

def player_movement(direction):
  if direction == "UP":
    player.position1 += -1
  elif direction == "DOWN":
    player.position1 += 1
  elif direction == "LEFT":
    player.position2 += -1
  elif direction == "RIGHT":
    player.position2 += 1  



# PLAYER AND STAT PROGRESSION



def player_progression(monsterXP):
  player.currentXP += monsterXP
  pause(1.5)
  if player.currentXP >= player.baseXP:
      player.level += 1
      print_new_lines(2)
      read_text("You leveled up! You are now a Lvl "+ str(player.level) +" "+ str(player.type) +"!")
      remainder = player.currentXP - player.baseXP
      player.currentXP = 0 + remainder
      player.baseXP = nextLevel(player.level)
      stat_progression()
  pause(1)

def stat_progression():
  player.maxHP += 1
  player.currentHP = player.maxHP
  print_new_lines(2)
  if player.level % 2 == 0 and player.level != 2:
    player.baseAtk += 1
    player.attack = [player.baseAtk-1,player.baseAtk,player.baseAtk+1]
    read_text("Your maxHP grew to "+ str(player.maxHP) +" and your baseAtk increased by one!")
  else:
    read_text("Your maxHP grew to "+ str(player.maxHP) +"!")
  pause(1)



## PLAYER ACTIONS (ACTIVE, INACTIVE) ##



def print_actions(player_action):
  global player_input
  # Prints all actions player can make
  i = 1
  for action in player_action:
    print("[" + str(i) + "] " + action, end = ' ')
    i += 1
  print_new_lines(1)
  player_input = int(input(""))

def active_actions():
  global monster_fight
  global player_input
  global monster_list
  global monster_index
  global boss_list
  global boss_index
  monster = monster_list[monster_index]
  boss = boss_list[boss_index]
  # Executes actions player can make during combat
  read_text(narrator_lines.general[0]) # What to do?
  print_actions(player.activeActions)
  check_invalid_input(player.inactiveActions)
  if player_input == 1: # ATTACK
    deal_attack("PLAYER",player.name,player.attack,player.baseAtk,player.critPercentage)
    if in_monster_fight == True and (player.position1,player.position2) in monster_positions:
      check_currentHP("MONSTER")
      if in_monster_fight == False: #IF MONSTER DIED
        print_victory_message(monster.name,earnedGold,monster.XP)
        # Prevents the player from encountering the same monster once defeated
        remove_events(player.position1,player.position2,monster_positions)
        player_progression(monster.XP)
    elif in_monster_fight == True and (player.position1,player.position2) == boss_position:
      check_currentHP("BOSS")
      if in_monster_fight == False: #IF BOSS DIED
        print_victory_message(boss.name,earnedGold,boss.XP)
        player_progression(boss.XP)
    print_new_lines(1)
  elif player_input == 2: # VIEW INVENTORY
    view_inventory()

def inactive_actions():
  global in_monster_fight
  global player_input
  global monster_positions
  global player_input
  # Executes actions player can make during exploring a dungeon
  read_text(narrator_lines.general[0]) # What to do?
  print_actions(player.inactiveActions)
  check_invalid_input(player.inactiveActions)
  if player_input == 1: #MOVE
    get_directions(player.position1,player.position2)  
      # Checks if player positions is equal to a monster position in a list, which will trigger 
    if (player.position1,player.position2) in monster_positions:
      in_monster_fight = True
    elif (player.position1,player.position2) == boss_position:
      in_monster_fight = True
  elif player_input == 2: #VIEW INVENTORY
    view_inventory()
    
def choose_action():
  global in_monster_fight
  if in_monster_fight == True: 
  # Prints actions while in battle
    active_actions()
  elif in_inventory == True:
  # Prints actions while in inventory
    inventory_actions()
  else:
  # Prints actions while not in battle
    inactive_actions()



## COMBAT SYSTEM ##



def enemy_encounter(nameStr,enemyName,enemyAttack,enemyCurrentHP,enemyMaxHP,enemyBaseAtk,enemyCritPercentage):
  if player.turnsTaken == 0: 
  # Notifies player that they encountered a monster
    read_text("As soon as you walked in, you encountered a " + enemyName + "!!!")
    player.turnsTaken += 1
  else: 
  # The monster attacks
    deal_attack(nameStr,enemyName,enemyAttack,enemyBaseAtk,enemyCritPercentage)
    check_currentHP("PLAYER")
  print_new_lines(1)
  view_stats(enemyName,enemyCurrentHP,enemyMaxHP,enemyBaseAtk,False)

def deal_attack(player1,player1name,player1attack,player1baseAtk,player1critPercentage):
  # Draws a random float between 0 and 1 to decide attack damage
  random_float = random.random()
  if random_float <= player1critPercentage:
    # Chance of critical hit, which doubles the amount of attack damage
    read_text("CRITICAL! ")
    player1_attack = player1baseAtk * 2
  else:
    player1_attack = random.randint(player1attack[0],player1attack[2])
  if player1 == "MONSTER" or player1 == "BOSS": 
    # Prints what the mosnter or boss dealt to the player
    player.currentHP = player.currentHP - player1_attack
    read_text("The " + player1name + " dealt " + str(player1_attack) + " damage to you!")
  elif player1 == "PLAYER": 
    # Prints what the player dealt to monster or boss
    if in_monster_fight == True and (player.position1,player.position2) in monster_positions: # DEALS ATTACK TO MONSTER
      monster.currentHP = monster.currentHP - player1_attack
    elif in_monster_fight == True and (player.position1,player.position2) == boss_position: # DEALS ATTACK TO BOSS
      boss.currentHP = boss.currentHP - player1_attack
    read_text("You dealt " + str(player1_attack) + " damage to it!")
    pause(2)

def check_currentHP(name):
  global game_state
  global in_dungeon
  global in_monster_fight
  global turns_taken
  global player_died
  global monster_list
  global monster_index
  global earnedGold
  # Checks if a player/monster/boss dies, then it will execute certain actions 
  if name == "PLAYER":
    if player.currentHP <= 0: #IF PLAYER DIES
    # Takes player out of game, executing death screen
      in_monster_fight = False
      game_state = False
      player_died = True
  elif name == "MONSTER":
    monster = monster_list[monster_index]
    if monster.currentHP <= 0: #IF MONSTER DIES
      # Takes player out of battle
      in_monster_fight = False
      # Adds 1 to monsters killed and player gains gold
      player.monstersKilled += 1
      earnedGold = random.randint(monster.value-5,monster.value+5)
      player.gold += earnedGold
      # Resets monster's HP
      monster.currentHP = monster.maxHP
      player.turnsTaken = 0
      # Changes what monster the player will encounter next
      monster_index = random.randint(0,len(monster_list)-1)
      item_drop()
  elif name == "BOSS": #IF BOSS DIES
    if boss.currentHP <= 0:
      # Takes player out of battle and of dungeon
      in_monster_fight = False
      in_dungeon = False
      # Adds 1 to monsters killed and player gains gold
      player.monstersKilled += 1 
      earnedGold = random.randint(boss.value-5,boss.value+5)
      player.gold += earnedGold
      # Resets monster's health
      boss.currentHP = boss.maxHP
      # Resets player's positions
      player.position1 = 4
      player.position2 = 0
      player.turnsTaken = 0
      # Adds 1 to dungeons cleared 
      player.dungeonsCleared += 1
      item_drop()    

def print_victory_message(name,value,XP):
  # Prints a victory message after player defeats a monster or boss
  print_new_lines(2)
  read_text("Great job! You defeated the " + str(name) + " and gained "+ str(XP) +" XP! You also gained " +  str(value) + " GOLD!!")



## ITEM DROP SYSTEM ##



def add_item(item):
  # Does not place duplicates of items
  if item not in player.inventory:
    player.inventory.append(item)

def item_drop():
  # TODO: Add exclusive item drops
  global has_dropped_item
  global item_list
  global drop_list
  global flg1
  # Executes function when player defeats a monster
  # This determines if the monster drops an item from the list of items
  drop_list = []
  item_index1 = 0
  item_index2 = 0
  while item_index1 == item_index2:
    item_index1 = random.randint(0,len(item_list)-1)
    item_index2 = random.randint(0,len(item_list)-1)
  # Draws two items that can be dropped
  for i in range(0,2):
    if i == 0:
      item = item_list[item_index1]
    elif i == 1:
      item = item_list[item_index2]
    # Draws a float between 0 and 1
    # Player recieves item if the float is less than the item's drop chance
    random_float = random.random()
    if random_float <= item.dropChance:
      has_dropped_item = True
      flg1 = True
      drop_list.append(item.name)
      add_item(item)
      item.quantity += 1

def print_dropped_items(name):
  global drop_list
  global has_dropped_item
  global flg1
  # Prints out the dropped items once
  if name == "CHEST":
    read_text(" You also found ")
  else:
    read_text("The " + str(name) + " dropped ")
  for i in range(0,len(drop_list)):
    if i == 0 and len(drop_list) == 1:
      read_text("a "+str(drop_list[i])+"!")
    elif i == 0:
      read_text("a "+str(drop_list[i]))
    elif i == len(drop_list)-1:
      read_text(" and a "+str(drop_list[i])+"!")
  # Empties drop_list and change booleans to FALSE to prevent message from repeating
  drop_list = []
  has_dropped_item = False
  flg1 = False



## SHOP SYSTEM ##



def open_shop():
  global in_shop
  # TODO: Simplify this function
  read_text("What can I get you?")
  while in_shop == True:
    print_new_lines(1)
    outline(40)
    print("THE SHOP")
    print_new_lines(1)
    for item in shop_items:
      if item.shopQuantity <= 0:
        print(str(item.name)+" [SOLD OUT]",end=" ")
      else:  
        print("x"+str(item.shopQuantity)+" "+str(item.name)+" ["+str(item.value)+" GOLD]",end=" ")
      print_new_lines(2)
    if player.gold == 0:
      read_text(narrator_lines.shop[2])
      in_shop = False
    else:
      read_text("You have " + str(player.gold) +" GOLD.")
      outline(40)
      shop_actions()
      pause(2)
      clear()
      pause(2)

def shop_actions():
  global in_shop
  print_new_lines(1)
  read_text(narrator_lines.general[0])
  print_new_lines(2)
  print_actions(player.shopActions)
  check_invalid_input(player.shopActions)
  if player_input == 1: #BUY ITEM
      print_items(False,False,True,shop_items)
      chosen_item = shop_items[player_input-1]
      if player.gold < chosen_item.value:
        read_text("You can't afford that item.")
      elif chosen_item.shopQuantity <= 0:
        read_text("There are no more of that item.")
      else:
        player.gold += -chosen_item.value
        player.inventory.append(chosen_item)
        chosen_item.quantity += 1
        chosen_item.shopQuantity += -1
        read_text("You bought a "+str(chosen_item.name)+"!")
  elif player_input == 2: # VIEW ITEMS
    print_items(False,False,True,shop_items)
    chosen_item = shop_items[player_input-1]
    view_item(chosen_item)
  elif player_input == 3:
    read_text("The shopkeeper thanked you for your business.")
    print_new_lines(1)
    in_shop = False



## MISC FUNCTIONS ##



def check_invalid_input(player_action = "None"):
  global player_input
  # Checks for invalid integer inputs
  while player_input > len(player_action) or player_input < 1:
    read_text(narrator_lines.general[1])
    player_input = int(input(" "))

def trigger_trap():
  i = random.randint(0,len(narrator_lines.trap)-1)
  damage = random.randint(1,4)
  read_text("As soon as you walked in, "+narrator_lines.trap[i]+" ")
  read_text("You got hurt and dealt "+ str(damage)+"!") 
  player.currentHP += -damage
  trap_positions.remove((player.position1,player.position2))
  check_currentHP("PLAYER")

def print_hand(player_hand):
  if len(player_hand) == 0:
    read_text("You enter the dark entrance of the dungeon with nothing in your hand.")
  else:
    read_text("You enter the dark entrance of the dungeon, wielding a " + str(player_hand[0].name) +" in your hand.")

def print_narrator_verdict():
  # Prints how well the player did after they died 
  if player.dungeonsCleared <= 20:
    #YOU DID WELL FOR A BEGINNER
    read_text(narrator_lines.dead[1])
  elif player.dungeonsCleared > 20: 
    #YOU DID WELL AS A PRO
    read(narrator_lines.dead,1,2)



## PROLOGUE ##



skip_story = True

if skip_story == False:
  get_player_info()
  play_prologue()
else: 
  # SETS NAME AND HOMETOWN TO "NONAME" AND "HOMETOWN"
  player.name = "NONAME"
  player.hometown = "HOMETOWN"



## MAIN LOOP ##



# Runs game until player has died
while game_state == True and player_died == False:
  dungeon = generate_dungeon()
  monster_positions = generate_events(5,monster_positions)
  treasure_positions = generate_events(2,treasure_positions)
  trap_positions = generate_events(2,trap_positions)
  if player.dungeonsCleared == 0 and skip_story == False:
    read(narrator_lines.story,0,7)
  print_hand(player.hand)
  flg1 = True
  print_new_lines(1)
  while in_dungeon == True and player_died == False:
    print_dungeon(dungeon,player.position1,player.position2,treasure_positions)
    if in_monster_fight == True and (player.position1,player.position2) in monster_positions:
      monster = monster_list[monster_index]
      enemy_encounter("MONSTER",monster.name,monster.attack,monster.currentHP,monster.maxHP,monster.baseAtk,monster.critPercentage)
      remove_events(trap_positions)
    elif in_monster_fight == True and (player.position1,player.position2) == boss_position:
      boss = boss_list[boss_index]
      enemy_encounter("BOSS",boss.name,boss.attack,boss.currentHP,boss.maxHP,boss.baseAtk,boss.critPercentage)
    elif player.position1 == 3 and player.position2 == 3:
      # Prints dropped items if monster happens to be at the boss gate
      if has_dropped_item == True and flg1 == True:
        print_dropped_items(monster.name)
        remove_events(player.position1,player.position2,treasure_positions)
        print_new_lines(2)
      # Prints gate to the boss
      read_text("You find yourself in a room with a locked gate in the east side. Something is locked in there, you thought. You hear a low, rumbling sound on the other side.")
    elif has_dropped_item == True and flg1 == True:
      print_dropped_items(monster.name)
      remove_events(player.position1,player.position2,treasure_positions)
    elif (player.position1,player.position2) in treasure_positions:
      read_text("You walk in to find a treasure chest right in the middle of the room. It appears to be locked.")
      # Prevents user from finding a treasure chest and then stumble across a trap
      remove_events(player.position1,player.position2,trap_positions)
    elif (player.position1,player.position2) in trap_positions:
      trigger_trap()
    else: 
      # You walk into empty room
      read_text(narrator_lines.inactive[0])
    print_new_lines(1)
    if player_died == False:
      # Prints player's stats and prints the possible actions
      view_stats(player.name,player.currentHP,player.maxHP,player.baseAtk,True,player.level,player.currentXP,player.baseXP)
      print_new_lines(1)
      choose_action()
    clear()
    pause(0.2)
  
  # After you clear a dungeon

  if in_dungeon == False and player_died == False:
    # Little congratulary message
    boss = boss_list[boss_index]
    read_text("You cleared the dungeon and killed the "+str(boss.name) +"! Well done!")
    pause(1)
    clear()
    if player.dungeonsCleared == 1:
      # Some story elements
      read_text("As you head back to the cottages of your village, "+ str(player.hometown)+" , your father congratulated you for coming back in one piece.")
      pause(1)
      clear()
    # You visit a shop
    read(narrator_lines.shop,0,1)
    in_shop = True
    open_shop()
    # Loops back to the beginning
  in_dungeon = True

# After player has died

if player_died == True:
  # You have died
  pause(1)
  read_text(narrator_lines.dead[0])
  print_narrator_verdict()
  # Prints final stats
  read_text("You cleared " + str(player.dungeonsCleared) + " dungeons and killed " + str(player.monstersKilled) + " monsters. You were a Lvl "+ str(player.level) +" " + str(player.type) + " that had a maxHP of " + str(player.maxHP) + " and a baseAtk of " + str(player.attack[1]) + ".")
  print_new_lines(1)
  # If your want to contuinue your journey
  # You must start a new game
  read(narrator_lines.dead,4,5)
  clear()
  pause(10)
  


