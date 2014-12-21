import random

player_health = 100
mob_health = 0


def set_mob_health(mob):
    global mob_health
    if mob_health <= 0:
        if mob == 'spider':
            mob_health = 10
        elif mob == 'rat':
            mob_health = 25
        elif mob == 'zombie':
            mob_health = 50
        elif mob == 'skeleton':
            mob_health = 75

def fight(mob):
    global player_health
    global mob_health
    set_mob_health(mob)
    if mob == 'spider':
        print('You attack the spider!\n')
        mob_dmg = random.randint(0, 3)
        if mob_dmg == 0:
            print('The spider tried attacking you but missed!')
        else:
            print('The spider does %s damage!' % mob_dmg)
            player_health -= mob_dmg
            print('You have', player_health, 'health left!\n')
            if player_health <= 0:
                print('You\'re dead! Game over!')
                exit()

        #  The player attacks the mob
        player_dmg = random.randint(0, 20)
        if player_dmg == 0:
            print('You missed!')
            return False
        else:
            print('You hit the spider and deal %s damage!' % player_dmg)
            mob_health -= player_dmg
            if mob_health <= 0:
                print('You kill the spider!')
                return True
            if mob_health > 0:
                print('The spider has', mob_health, 'health left!')
                return False

    if mob == 'rat':
        print('You attack the rat!\n')
        mob_dmg = random.randint(0,7)
        if mob_dmg == 0:
            print('The rat tried attacking you but missed!')
        else:
            print('The rat does %s damage!' % mob_dmg)
            player_health -= mob_dmg
            print('You have', player_health, 'health left!\n')
            if player_health <= 0:
                print('You\'re dead! Game over!')
                exit()

        #  The player attacks the mob
        player_dmg = random.randint(0, 20)
        if player_dmg == 0:
            print('You missed!')
            return False
        else:
            print('You hit the rat and deal %s damage!' % player_dmg)
            mob_health -= player_dmg
            if mob_health <= 0:
                print('You kill the rat!')
                return True
            if mob_health > 0:
                print('The rat has', mob_health, 'health left!')
                return False

    if mob == 'zombie':
        print('You attack the zombie!\n')
        mob_dmg = random.randint(0, 15)
        if mob_dmg == 0:
            print('The zombie tried attacking you but missed!')
        else:
            print('The zombie does %s damage!' % mob_dmg)
            player_health -= mob_dmg
            print('You have', player_health, 'health left!\n')
            if player_health <= 0:
                print('You\'re dead! Game over!')
                exit()

        #  The player attacks the mob
        player_dmg = random.randint(0, 20)
        if player_dmg == 0:
            print('You missed!')
            return False
        else:
            print('You hit the zombie and deal %s damage!' % player_dmg)
            mob_health -= player_dmg
            if mob_health <= 0:
                print('You kill the zombie!')
                return True
            if mob_health > 0:
                print('The zombie has', mob_health, 'health left!')
                return False

    if mob == 'skeleton':
        print('You attack the skeleton!\n')
        mob_dmg = random.randint(0, 20)
        if mob_dmg == 0:
            print('The skeleton tried attacking you but missed!')
        else:
            print('The skeleton does %s damage!' % mob_dmg)
            player_health -= mob_dmg
            print('You have', player_health, 'health left!\n')
            if player_health <= 0:
                print('You\'re dead! Game over!')
                exit()

        #  The player attacks the mob
        player_dmg = random.randint(0, 20)
        if player_dmg == 0:
            print('You missed!')
            return False
        else:
            print('You hit the skeleton and deal %s damage!' % player_dmg)
            mob_health -= player_dmg
            if mob_health <= 0:
                print('You kill the skeleton!')
                return True
            if mob_health > 0:
                print('The skeleton has', mob_health, 'health left!')
                return False