import cmd
import textwrap
import cave

# miniQuest Text - Written by Cody Cooper with the help of Al Sweigart (http://inventwithpython.com)

DESC = 'desc'
NORTH = 'north'
SOUTH = 'south'
EAST = 'east'
WEST = 'west'
CHESTS = 'chests'
CHESTDESC = 'chestdesc'
SHORTDESC = 'shortdesc'
LONGDESC = 'longdesc'
TAKEABLE = 'takeable'
EDIBLE = 'edible'
DESC_WORDS = 'desc_words'
SHOP = 'shop'
BUYPRICE = 'buyprice'
SELLPRICE = 'sellprice'

SCREEN_WIDTH = 80

world_rooms = {
    'Your House': {
        DESC: 'You live here! A small, cozy house. Your front door takes you right in to the market!',
        NORTH: 'Market',
        CHESTS: ['Health Potion']},
    'Market': {
        DESC: 'The market is bustling!',
        NORTH: 'Cave Entrance',
        EAST: 'Blacksmith',
        SOUTH: 'Your House',
        WEST: 'Apothecary',
        CHESTS: []},
    'Cave Entrance': {
        DESC: 'The entrance to the cave!',
        SOUTH: 'Market',
        CHESTS: []},
    'Blacksmith': {
        DESC: 'The blacksmith! Buy weapons and armor here.',
        WEST: 'Market',
        SHOP: ['Health Potion'],
        CHESTS: []},
    'Apothecary': {
        DESC: 'The apothecary! Buy potions here.',
        EAST: 'Market',
        SHOP: ['Health Potion'],
        CHESTS: []},
    }

world_items = {
    'Health Potion': {
        CHESTDESC: 'A health potion! Drink to restore your health!',
        SHORTDESC: 'a health potion',
        LONGDESC: 'A health potion! Type drink health to use!',
        EDIBLE: True,
        DESC_WORDS: ['health', 'potion', 'health potion'],
        BUYPRICE: 25,
        SELLPRICE: 5},
    }

location = 'Your House'  # Start in your house
inventory = []  # Start with nothing in inventory
show_full_exits = True


def display_location(loc):
    """A helper function for displaying an area's description and exits."""
    # Print location
    print(loc)
    print('~' * len(loc))

    # Print the location's description using textwrap
    print('\n'.join(textwrap.wrap(world_rooms[loc][DESC], SCREEN_WIDTH)))

    # Print all chests and list what items are inside of them
    if len(world_rooms[loc][CHESTS]) > 0:
        print()
        for item in world_rooms[loc][CHESTS]:
            print('There\'s a chest with', world_items[item][SHORTDESC], 'inside of it!')

    # Print all the exits
    exits = []
    for direction in (NORTH, SOUTH, EAST, WEST):
        if direction in world_rooms[loc].keys():
            exits.append(direction.title())
    print()
    if show_full_exits:
        for direction in (NORTH, SOUTH, EAST, WEST):
            if direction in world_rooms[location]:
                print('%s: %s' % (direction.title(), world_rooms[location][direction]))
    else:
        print('Exits: %s' % ' '.join(exits))


def move_direction(direction):
    """A helper function that changes the location of the player."""
    global location

    if direction in world_rooms[location]:
        print('You move to the %s.' % direction)
        location = world_rooms[location][direction]
        display_location(location)
    else:
        print('You cannot move in that direction')


def get_all_desc_words(item_list):
    """Returns a list of 'description words' for each item named in item_list."""
    item_list = list(set(item_list))  # Make item_list unique
    desc_words = []
    for item in item_list:
        desc_words.extend(world_items[item][DESC_WORDS])
    return list(set(desc_words))


def get_all_first_desc_words(item_list):
    """Returns a list of the first 'description word' in the list of
        description words for each item named in item_list"""
    item_list = list(set(item_list))  # Make item_list unique
    desc_words = []
    for item in item_list:
        desc_words.append(world_items[item][DESC_WORDS][0])
    return list(set(desc_words))


def get_first_item_matching_desc(desc, item_list):
    item_list = list(set(item_list))  # Make item_list unique
    for item in item_list:
        if desc in world_items[item][DESC_WORDS]:
            return item
    return None


def get_all_items_matching_desc(desc, item_list):
    item_list = list(set(item_list))  # Make item_list unique
    matching_items = []
    for item in item_list:
        if desc in world_items[item][DESC_WORDS]:
            matching_items.append(item)
    return matching_items


class TextAdventureCmd(cmd.Cmd):
    prompt = '\n> '

    # The default() method is called when none of the other do_*() command methods match.
    def default(self, arg):
        print('I do not understand that command. Type "help" for a list of commands.')

    # A very simple "quit" command to terminate the program:
    def do_quit(self, arg):
        """Quit th game"""
        return True  # This exits the cmd application loop in TextAdventureCmd.cmdloop()

    def help_combat(self):
        print('Not yet implemented')

    def do_north(self, arg):
        """Move north"""
        move_direction('north')

    def do_south(self, arg):
        """Move south"""
        move_direction('south')

    def do_east(self, arg):
        """Move south"""
        move_direction('east')

    def do_west(self, arg):
        """move west"""
        move_direction('west')

    do_n = do_north
    do_s = do_south
    do_e = do_east
    do_w = do_west

    def do_exits(self, arg):
        """Toggle showing full exit descriptions or brief exit descriptions."""
        global show_full_exits
        show_full_exits = not show_full_exits
        if show_full_exits:
            print('Showing full exit descriptions.')
        else:
            print('Showing brief exit descriptions')

    def do_inventory(self, arg):
        """Display a list of the items in your possession"""

        if len(inventory) == 0:
            print('Inventory:\n  (nothing)')
            return

        # first get a count of each distinct item in the inventory
        item_count = {}
        for item in inventory:
            if item in item_count.keys():
                item_count[item] += 1
            else:
                item_count[item] = 1

        # get a list of inventory items with duplicates removed:
        print('Inventory:')
        for item in set(inventory):
            if item_count[item] > 1:
                print('  %s (%s)' % (item, item_count[item]))
            else:
                print('  ' + item)

    do_inv = do_inventory

    def do_take(self, arg):
        """Take <item> - take an item from a chest."""

        # Put this value in a more suitably named variable
        item_to_take = arg.lower()

        if item_to_take == '':
            print ('Take what?')
            return

        cant_take = False

        # Get the item name that the player's command describes
        for item in get_all_items_matching_desc(item_to_take, world_rooms[location][CHESTS]):
            if not world_items[item].get(TAKEABLE, True):
                cant_take = True
                continue  # There may be other items named this that you can take, so continue checking.
            print('You take %s.' % (world_items[item][SHORTDESC]))
            world_rooms[location][CHESTS].remove(item)  # Remove from the ground
            inventory.append(item)  # add to inventory
            return

        if cant_take:
            print('You can\'t take "%s".' % item_to_take)
        else:
            print('That is not in the chest.')

    def do_drop(self, arg):
        """drop <item> - drop an item from your inventory on to the ground."""

        # put this value in a more suitably named variable
        item_to_drop = arg.lower()

        # get a list of all "Description words" for each item in the inventory
        inv_desc_words = get_all_desc_words(inventory)

        # find out if the player doesn't have that item
        if item_to_drop not in inv_desc_words:
            print('You do not have "%s" in your inventory.' % item_to_drop)
            return

        # get the item name that the player's command describes
        item = get_first_item_matching_desc(item_to_drop, inventory)
        if item is not None:
            print('You drop %s.' % (world_items[item][SHORTDESC]))
            inventory.remove(item)  # remove from inventory
            world_rooms[location][CHESTS].append(item)  # add to the ground

    def complete_take(self, text, line, begidx, endidx):
        possible_items = []
        text = text.lower()

        # if the user has only typed 'take' but no item name:
        if not text:
            return get_all_first_desc_words(world_rooms[location][CHESTS])

        # otherwise, get a list of description words for ground items matching the command text so far.
        for item in list(set(world_rooms[location][CHESTS])):
            for desc_word in world_items[item][DESC_WORDS]:
                if desc_word.startswith(text) and world_items[item].get(TAKEABLE, True):
                    possible_items.append(desc_word)
        return list(set(possible_items))  # make list unique

    def complete_drop(self, text, line, begidx, endidx):
        possible_items = []
        item_to_drop = text.lower()

        # get a list of all description words for each item in the inventory
        inv_desc_words = get_all_desc_words(inventory)

        for desc_word in inv_desc_words:
            if line.startswith('drop %s' % desc_word):
                return []  # command is complete.

        # if the use has only typed drop but no item name:
        if item_to_drop == '':
            return get_all_first_desc_words(inventory)

        # otherwise, get a list of all 'description words' for inventory items matcing the command text so far.
        for desc_word in inv_desc_words:
            if desc_word.startswith(text):
                possible_items.append(desc_word)

        return list(set(possible_items))  # make list unique.

    def do_look(self, arg):
        """Look at an item, description, or the area:
            'look' - display the current area's description
            'look <direction>' - display the description of the area in that directio
            'look exits' - display the description of all adjacent areas
            'look <item> - display the description of an item in a chest or in your inventory"""

        looking_at = arg.lower()
        if looking_at == '':
            # look will re print the area description
            display_location(location)
            return

        if looking_at == 'exits':
            for direction in (NORTH, SOUTH, EAST, WEST):
                if direction in world_rooms[location]:
                    print('%s: %s' % (direction.title(), world_rooms[location][direction]))
            return

        if looking_at in ('north', 'west', 'east', 'south', 'n', 'e', 's', 'w'):
            if looking_at.startswith('n') and NORTH in world_rooms[location]:
                print(world_rooms[location][NORTH])
            elif looking_at.startswith('w') and WEST in world_rooms[location]:
                print(world_rooms[location][WEST])
            elif looking_at.startswith('e') and EAST in world_rooms[location]:
                print(world_rooms[location][EAST])
            elif looking_at.startswith('s') and SOUTH in world_rooms[location]:
                print(world_rooms[location][SOUTH])
            else:
                print('There is nothing in that direction.')
            return

        # see if the item being looked at is on the ground at this location
        item = get_first_item_matching_desc(looking_at, world_rooms[location][CHESTS])
        if item is not None:
            print('\n'.join(textwrap.wrap(world_items[item][LONGDESC], SCREEN_WIDTH)))
            return

        # see if the item being looked at is in the inventory
        item = get_first_item_matching_desc(looking_at, inventory)
        if item is not None:
            print('\n'.join(textwrap.wrap(world_items[item][LONGDESC], SCREEN_WIDTH)))
            return

        print('You do not see that nearby.')

    def complete_look(self, text, line, begidx, endidx):
        possible_items = []
        looking_at = text.lower()

        # get a list of all description words for each item in the inventory.
        inv_desc_words = get_all_desc_words(inventory)
        ground_desc_words = get_all_desc_words(world_rooms[location][CHESTS])
        shop_desc_words = get_all_desc_words(world_rooms[location].get(SHOP, []))

        for desc_word in inv_desc_words + ground_desc_words + shop_desc_words + [NORTH, SOUTH, EAST, WEST]:
            if line.startswith('look %s' % desc_word):
                return []  # command is complete

        # if the user has only typed "look" but no item name, show all items in chest, shop, and directions
        if looking_at == '':
            possible_items.extend(get_all_first_desc_words(world_rooms[location][CHESTS]))
            possible_items.extend(get_all_first_desc_words(world_rooms[location].get(SHOP, [])))
            for direction in (NORTH, SOUTH, EAST, WEST):
                if direction in world_rooms[location]:
                    possible_items.append(direction)
            return list(set(possible_items))  # make list unique

        # otherwise, get a list of all description words for ground items matching the command text so far.
        for desc_word in ground_desc_words:
            if desc_word.startswith(looking_at):
                possible_items.append(desc_word)

        # otherwise, get a list of all description words for items for sale at the shop ( if this is one )
        for desc_word in shop_desc_words:
            if desc_word.startswith(looking_at):
                possible_items.append(desc_word)

        # check for matching directions
        for direction in (NORTH, SOUTH, EAST, WEST):
            if direction.startswith(looking_at):
                possible_items.append(direction)

        # get a list of all description words for inventory items matching the command text so far
        for desc_word in inv_desc_words:
            if desc_word.startswith(looking_at):
                possible_items.append(desc_word)

        return list(set(possible_items)) # make list unique

    def do_list(self, arg):
        """List the items for sale at the current location's shop. "list full" will show details of the items."""
        if SHOP not in world_rooms[location]:
            print('This is not a shop.')
            return

        arg = arg.lower()

        print('For sale:')
        for item in world_rooms[location][SHOP]:
            print(' - %s' % item)
            if arg == 'full':
                print('\n'.join(textwrap.wrap(world_items[item][LONGDESC], SCREEN_WIDTH)))

    def do_buy(self, arg):
        """buy <item> - buy an item at the current location's shop."""
        if SHOP not in world_rooms[location]:
            print('This is not a shop.')
            return

        item_to_buy = arg.lower()

        if item_to_buy == '':
            print('Buy what? Type "list" or "list full" to see a list of items for sale.')
            return

        item = get_first_item_matching_desc(item_to_buy, world_rooms[location][SHOP])
        if item != None:
            # Check gold/remove gold here.
            print('You have purchased %s' % (world_items[item][SHORTDESC]))
            inventory.append(item)
            return

        print('"%s" is not sold here. Type "list" or "list full" to see a list of items for sale.' % item_to_buy)


    def complete_buy(self, text, line, begidx, endidx):
        if SHOP not in world_rooms[location]:
            return []

        item_to_buy = text.lower()
        possible_items = []

        # if the user has only typed "buy" but no item name:
        if not item_to_buy:
            return get_all_first_desc_words(world_rooms[location][SHOP])

        # otherwise, get a list of all "description words" for shop items matching the command text so far:
        for item in list(set(world_rooms[location][SHOP])):
            for desc_word in world_items[item][DESC_WORDS]:
                if desc_word.startswith(text):
                    possible_items.append(desc_word)

        return list(set(possible_items))  # make list unique


    def do_sell(self, arg):
        """"sell <item>" - sell an item at the current location's shop."""
        if SHOP not in world_rooms[location]:
            print('This is not a shop.')
            return

        item_to_sell = arg.lower()

        if item_to_sell == '':
            print('Sell what? Type "inventory" or "inv" to see your inventory.')
            return

        for item in inventory:
            if item_to_sell in world_items[item][DESC_WORDS]:
                # implement check price/add gold here
                print('You have sold %s' % (world_items[item][SHORTDESC]))
                inventory.remove(item)
                return

        print('You do not have "%s". Type "inventory" or "inv" to see your inventory.' % item_to_sell)


    def complete_sell(self, text, line, begidx, endidx):
        if SHOP not in world_rooms[location]:
            return []

        item_to_sell = text.lower()
        possible_items = []

        # if the user has only typed "sell" but no item name:
        if not item_to_sell:
            return get_all_first_desc_words(inventory)

        # otherwise, get a list of all "description words" for inventory items matching the command text so far:
        for item in list(set(inventory)):
            for desc_word in world_items[item][DESC_WORDS]:
                if desc_word.startswith(text):
                    possible_items.append(desc_word)

        return list(set(possible_items))  # make list unique


    def do_drink(self, arg):
        """"drink <item>" - drink an item in your inventory."""
        item_to_drink = arg.lower()

        if item_to_drink == '':
            print('drink what? Type "inventory" or "inv" to see your inventory.')
            return

        cant_drink = False

        for item in get_all_items_matching_desc(item_to_drink, inventory):
            if not world_items[item].get(EDIBLE, False):
                cant_drink = True
                continue
            # check food/add health here
            print('You drink %s' % (world_items[item][SHORTDESC]))
            inventory.remove(item)
            return

        if cant_drink:
            print('You cannot drink that.')
        else:
            print('You do not have "%s". Type "inventory" or "inv" to see your inventory.' % item_to_drink)

    def complete_drink(self, text, line, begidx, endidx):
        item_to_drink = text.lower()
        possible_items = []

        # if the user has only typed "drink" but no item name:
        if item_to_drink == '':
            return get_all_first_desc_words(inventory)

        # otherwise, get a list of all "description words" for edible inventory items matching the command text so far:
        for item in list(set(inventory)):
            for desc_word in world_items[item][DESC_WORDS]:
                if desc_word.startswith(text) and world_items[item].get(EDIBLE, False):
                    possible_items.append(desc_word)

        return list(set(possible_items))  # make list unique


    def do_enter(self, args):
        if location == 'Cave Entrance':
            cave.enter_cave()
        else:
            return

if __name__ == '__main__':
    print('Mini Quest Demo!')
    print('================')
    print()
    print('(Type "help" for commands.)')
    print()
    display_location(location)
    TextAdventureCmd().cmdloop()
    print('Thanks for playing!')
