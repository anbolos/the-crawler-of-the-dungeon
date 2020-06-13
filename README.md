# The Crawler of the Dungeon

A text-based dungeon crawler made by @Anquilis and @ketomlinson using python

This file is best viewed on GitHub:
https://github.com/Anquilis/the-crawler-of-the-dungeon

## FEATURES:

  #### DUNGEON
  
  - The player is placed in a generated 4x4 dungeon (not including the spawn and the boss room)
  
  - The player can encounter two kind of monsters: The SLIME and the SKELETON

  - The player can also stumble across tresure chests and traps
  
  - The player can fight the SLIME KING once a monster drops a key that unlocks the boss room 

  - The player can move in up to four directions or view their inventory while not it combat
  
  - Players can use, view, equip or unequip items 
    
  - The player can level up and gain stat buffs

  #### COMBAT

  - Player can either attack or use item (in the inventory)
  There is a small chance of a critical hit, which doubles the player's base attack

  #### OTHER

  - Items that can be dropped/found in monsters or treasure chests: GOLD, HEALTH POTION, KEY, WOODEN SWORD, SLIME SWORD

  - There is a shop at the end of the dungeon, where the can buy items using the gold they earned
  
  - The player is able to replay the game with the same monsters

## FEATURES TO THINK ABOUT ADDING:

  #### DUNGEON

  - More randomized dungeon layouts with floors

  - More kinds of monsters/bosses and stat types 

  #### COMBAT

  - The ability to defend against a monster and nulify their attack

  - The ability to run from a monster, with a chance of succession

  #### OTHER

  - A storyline

  - A blacksmith to improve player's skils or to craft their own items
  (look at CONCEPTS.md)

  - Quest system

  - More items with different buffs

## TECHNICAL STUFF

- This game uses the sy, os, time, math, and random modules built-in into python

- I'm planning to split up the main.py file into smaller chunks (for each class) as suggested

- This game uses four classes to hold 
  - Player data 
  - Monster data
  - Item data
  - Narrator line data
(Found on lines 42-271)

- They currently do not hold any functions that contribute to the game logic

- I'm considering using json to serialize all the data and load it back into the class for effeciency

- Game uses global variables to dictate the game logic, but I'm planning to remove it to save memory and put it all in some kind of class 

### DIRECTORY

- As for now, I will keep this directory to hopefully guide contributers and code reviews in the main.py file

- Anything in **bold** are functions for the player exclusively 

(Lines 4-28) imported modules and global variables

(126-129) all created items

(200-205) all created monsters and bosses

(279-307) visual functions
and
(421-425) 'read' function
and
(427-436) 'view stats' function

(309-323) getting player info and introduction functions

(337-345) Function to convert player's positions into a tuple (used to trigger events)

(347-419) dungeon creation/priting and event generator (which generates list of tuples)

**(438-478) player inventory system**

**(480-566) player movement system (includes safeguard to prevent player from going out of bounds)**

(568-573) check invalid inputs function (only checks for invalid number inputs)

**(575-597) player progression and stat progression system** 

**(599-649) actions player could make in or out of combat (functions to execute those actions are NOT included)**

**(655-842) actions player could make while in their inventory (functions to execute those actions are included)**

(861-944) combat system

(946-995) item drop system

(1002-1051) shop system

(1075-1083) introduction (get player info and "title screen")

- skip story variable disables all the story elements, including the introduction

**(1089-1162) Main loop, uses all functions above**

**(1166-1178) Player death screen **

