# Changelog
This file will keep track of notable changes.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

## Known Bugs
- The program will crash if the player inputs a letter, a space, or any kind of special character (kept for debgugging)
- When at the entrance of the boss room (3,3), you can go out of bounds


## [0.1] - 2020-6-12
### Added
- Version control!
- This new, more organized changelog file! (now in markdown)
- Concpets file to plan out different features
- A code directory in the readme file
- A 'print_dropped_items' check if the player defeats a monster at the gate of the boss room and drops an item
### Changed
- Placed 'dungeon = generate_dungeon()' line in game loop so that all discovered tiles from last dungeon reverts back to an undiscovered tile, which is blank
- Tweaked the stat_progression function where the player is restored to full HP once they level up
- The shop will now refresh once the player executes an action and cleans up the console
- Boss_position is now just a tuple value, not a tuple within a list (see below)
### Fixed
- Where player could enter the boss room without unlocking the gate becuase 'boss_position not in locked_positions' returned True when it should return False 

## [NOTE] All changes before 2020-6-12 can not be reversed 
### All changes descibed below can be more vague than current versions

## - 2020-6-9
### Added
- Player and stat progression!
### Changes  
- Outline function takes in a parameter to change line length (cosmetic)
### Fixed
- Item choices disapear when the user backspaces

## - 2020-6-7
### Added
- Indicators of treasure chests (cosmetic)
- More helper functions
### Removed
- Dungeon hallways to prevent misalignment of rooms (cosmetic)
### Fixed
- Fixed shop
- Game loop

## - 2020-6-5
### Added
- Treasure chest and trap events!
- A 'read' function to handle story elements of game (cosmetic)
- Moved statements to 'narrator_lines' class
### Changed
- Key chance drop increased from 66% to 75%

## - 2020-6-3
### Removed
- 'print_corridors' function (cosmetic function that told players of possible directions)

## - 2020-6-2
### Changed
- Change functions

## - 2020-6-1
### Added
- Fog of war!
- Story lines (it is skipped if skip_story == True in line 1074)
### Changed
- Shop system tweaks and bug fixes

## - 2020-5-31
### Added
- Shop system!

## - 2020-30-5
### Added
- Boss fights are back!
- The ability to unlock rooms
- Player can not equip items that aren't equippable
- Player can not consume items that aren't consumable
### Changed
- Increased key dropChance from 0.125 to 0.66
- Tweaked monster stats
- Equip and unquip item functions are now separate
### Fixed
- Player cant unequip item when their inventory is empty
- 'Which item?' message duplicates as player gets more items
- Player cant equip the SLIME SWORD
- After inputting an invalid input, once a player types a valid input it refreshes itself instead of executing actions

## - 2020-5-28
### Added
- Inventory actions! (USE, VIEW, EQUIP)

## - 2020-5-27
### Added
- A working item drop system! 
- A monster can drop up to 2 items
- 'print_new_lines' function now takes in a parameter to determine how many lines to skip (cosmetic)
### Fixed
- Inventory system

## - 2020-5-26
### Added
- Items() object
- Skeletons! (different monster types) Made with using __init__
### Changed
- 'get_direction' function to be more efficient
- Tweaked 'create_monsters' function to print positions at 
  (0,0),(1,1),(2,2),and (3,3)
### Removed
- Boss fights and inventory to work on item drops (temporary)

## - 2020-5-26 
### Added
- New changelog! (look at old/CHANGELOG.txt)

## - 2020-5-24
### Changed
- Cleaned up code with small tweaks

## - 2020-5-23
### Added 
- Created inventory system
- Potions!
- 'enemy_encounter' function, used for both in monster and boss fights
- Boss fight system!
### Changed
- Tweaks and bug fixes
### Fixed
- When in the boss room, it shows "=[ X ]=" instead of intended marker with boss "=[ X  ☠ ]" (cosmetic)
- Uneven spacing in the game (cosmetic)

## - 2020-5-22
### Added
- Outline for boss fight
- Attack system!
- Death screen!
- Added class 'narrator_lines' to store all game lines
### Changed
- Cleaned up and consolidated code
- 'deal_monster_attack' function turned into 'deal_attack' function for both player and monster attack
### Fixed
- 'check_invalid_inputs' will always print out 'Invalid Action' line the first time even though player picked a valid option

## - 2020-21-5
### Added
- Player positioning system! (used index)
- Player movement system!
- Safeguard to prevent players from going out of bounds
- Outline for monster detection/combat
### Changed
- Renamed functions

## - 2020-5-20
### Added
- Dungeon layout! (lists within more lists)
- 'spawn_monster' function to generate monster positions 
- Made helper functions to construct game loop
  - print_dungeon
  - view_stats
  - getDirections
  - Picking actions

## - 2020-5-19
### Added
- Made a completely optional intro scene to get player name and hometown
- Player/monster/boss classes
- Text files to plan out responses for the AP CSP exam 

## - 2020-5-18
### Added
- This repl!
- The Crawler of the Dungeon was born! (originally named ScuffedCreateTask)



  