import random
import textwrap
import cmd
import time
import combat

SCREEN_WIDTH = 80

NORTH = 'north'
SOUTH = 'south'
WEST = 'west'
EAST = 'east'
DESC = 'desc'
CHESTS = 'chests'
MOBS = 'mobs'

show_full_exits = True
chest_opened = False
mob_dead = False
gold_pouch = 0


def chest_gen():
    return random.randint(0, 4) == 1


def spawn_mob():
    spawn = (random.randint(0, 1) == 1)
    _mobs = ['spider', 'rat', 'zombie', 'skeleton']
    if spawn:
        return _mobs[random.randint(0, 3)]


def gold_get():
    global gold_pouch
    print('You open the chest...')
    time.sleep(1)
    added_gold = random.randint(10, 100)
    print('You find ', added_gold, 'in the chest! Wow!')
    gold_pouch += added_gold
    print('You have ', gold_pouch, ' gold in your pouch!')
    return


def room_gen():
    return random.randint(1, 11)

location = room_gen()


cave_rooms = {
    1: {
        DESC: 'There\'s a door in every direction!',
        NORTH: room_gen(),
        EAST: room_gen(),
        SOUTH: room_gen(),
        WEST: room_gen(),
        CHESTS: chest_gen(),
        MOBS: spawn_mob()},
    2: {
        DESC: 'There\'s a door to the north, east, and south of you!',
        NORTH: room_gen(),
        EAST: room_gen(),
        SOUTH: room_gen(),
        CHESTS: chest_gen(),
        MOBS: spawn_mob()},
    3: {
        DESC: 'There\'s a door to the north and east of you!',
        NORTH: room_gen(),
        EAST: room_gen(),
        CHESTS: chest_gen(),
        MOBS: spawn_mob()},
    4: {
        DESC: 'There\'s a door to the north!',
        NORTH: room_gen(),
        CHESTS: chest_gen(),
        MOBS: spawn_mob()},
    5: {
        DESC: 'There\'s a door to the north and west of you!',
        NORTH: room_gen(),
        WEST: room_gen(),
        CHESTS: chest_gen(),
        MOBS: spawn_mob()},
    6: {
        DESC: 'There\'s a door to the north and south of you!',
        NORTH: room_gen(),
        SOUTH: room_gen(),
        CHESTS: chest_gen(),
        MOBS: spawn_mob()},
    7: {
        DESC: 'There\'s a door to your east and west of you!',
        EAST: room_gen(),
        WEST: room_gen(),
        CHESTS: chest_gen(),
        MOBS: spawn_mob()},
    8: {
        DESC: 'There\'s a door to the south and west of you!',
        SOUTH: room_gen(),
        WEST: room_gen(),
        CHESTS: chest_gen(),
        MOBS: spawn_mob()},
    9: {
        DESC: 'There\'s a door to your east!',
        EAST: room_gen(),
        CHESTS: chest_gen(),
        MOBS: spawn_mob()},
    10: {
        DESC: 'There\'s a door to the south!',
        SOUTH: room_gen(),
        CHESTS: chest_gen(),
        MOBS: spawn_mob()},
    11: {
        DESC: 'There\'s a door to the west!',
        WEST: room_gen(),
        CHESTS: chest_gen(),
        MOBS: spawn_mob()},
    }


def display_location(loc):
    """A helper function for displaying an area's description and exits."""
    global mob_dead
    # Print the room's description (using textwrap.wrap())
    print('\n'.join(textwrap.wrap(cave_rooms[loc][DESC], SCREEN_WIDTH)))

    # Print all chests in the area
    if cave_rooms[loc][CHESTS]:
        print('There\'s a chest!')

    # Print mob in area
    if cave_rooms[loc][MOBS] is None:
        print('You got lucky! No monsters in here!')
    else:
        print('There\'s a %s in the room!' % (cave_rooms[loc][MOBS]))


def move_direction(direction):
    """A helper function that changes the location of the player."""
    global location
    global mob_dead
    if mob_dead:
        if direction in cave_rooms[location]:
            mob_dead = False
            print('You move to the %s.' % direction)
            location = cave_rooms[location][direction]
            display_location(location)
        else:
            print('You cannot move in that direction')
    else:
        print('There\'s a %s in the way!' % cave_rooms[location][MOBS])


class CaveCommands(cmd.Cmd):
    prompt = '\n> '

    #  The default() method is called when none of the other do_*() command methods match.
    def default(self, arg):
        print('I do not understand that command. Type "help" for a list of commands.')

    # A very simple "quit" command to terminate the program:
    def do_quit(self, arg):
        """Quit th game"""
        return True  # This exits the cmd application loop in TextAdventureCmd.cmdloop()

    def do_look(self, arg):
        """Print surrounding area"""
        display_location(location)

    def do_north(self, arg):
        """Move north"""
        global chest_opened
        chest_opened = False
        move_direction('north')

    def do_south(self, arg):
        """Move south"""
        global chest_opened
        chest_opened = False
        move_direction('south')

    def do_east(self, arg):
        """Move south"""
        global chest_opened
        chest_opened = False
        move_direction('east')

    def do_west(self, arg):
        """move west"""
        global chest_opened
        chest_opened = False
        move_direction('west')

    do_n = do_north
    do_s = do_south
    do_e = do_east
    do_w = do_west

    def do_open(self, args):
        """open <chest> - opens a chest."""
        global chest_opened
        what_to_open = args.lower()

        if what_to_open == 'chest':
            if cave_rooms[location][CHESTS]:
                if not chest_opened:
                    gold_get()
                    chest_opened = True
                else:
                    print('You\'ve already opened this chest!')
        else:
            print('Open what?')

    def do_fight(self, args):
        """fight <mob> - fights a mob"""
        global mob_dead
        what_to_fight = args.lower()
        mob = cave_rooms[location][MOBS]
        if mob_dead:
            print('The', mob, 'is already dead!')
        elif what_to_fight == mob:
            mob_dead = combat.fight(mob)
        elif mob is None:
            print('There\'s nothing to fight!')
        else:
            print('Fight what?')




def enter_cave():
    print('You enter the cave...')
    time.sleep(1)
    display_location(location)
    CaveCommands().cmdloop()