# import classes
from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random


# create black magic
fire = Spell('Fire', 25, 600, 'black')
thunder = Spell('Thunder', 25, 600, 'black')
blizzard = Spell('Blizzard', 25, 600, 'black')
meteor = Spell('Meteor', 40, 1200, 'black')
quake = Spell('Quake', 14, 140, 'black')

# create white magic
cure = Spell('Cure', 25, 620, 'white')
cura = Spell('Cura', 32, 1500, 'white')
curaga = Spell('Curaga', 50, 6000, 'white')

# create some item
potion = Item('Potion', 'potion', 'Heals 50 HP', 50)
hipotion = Item('Hi-Potion','potion', 'Heals 100 HP', 100)
superpotion = Item('Super Potion','potion','Heals 500 HP', 1000)
elixer = Item('Elixer','elixer','Fully restores HP/MP of one party member', 9999)
hielixer = Item('MegaElixer','elixer','Fully restores HP/MP', 9999)

grenade = Item('Grenade','attack','Deals 500 damage',500)

enemy_spells = [fire,meteor,curaga]

player_spells = [fire, blizzard, thunder, meteor, quake, cure, cura]
player_items = [{"item": potion, "quantity": 15},{"item":  hipotion, "quantity": 5},
                {"item":  superpotion, "quantity": 5},
                {"item":  elixer, "quantity": 5},
                {"item": hielixer, "quantity": 2},{ "item": grenade, "quantity": 5}]


"""magic = [{"name": "Fire","cost": 10,"dmg": 100},
        {"name": "Thunder","cost": 10,"dmg": 124},
        {"name": "Blizzard","cost": 10,"dmg": 100}
         ]"""

# instantiate person player
player1 = Person('Valos', 3260, 132, 300, 34,player_spells, player_items)
player2 = Person('Nick ', 4160, 188, 311, 34,player_spells, player_items)
player3 = Person('James', 3089, 174, 288, 34,player_spells, player_items)

# enemy
enemy1 = Person('Imp  ', 1250, 130, 560, 325, enemy_spells, [])
enemy2 = Person('Magus',11200, 701, 525, 25, enemy_spells, [])
enemy3 = Person('Imp  ', 1250, 130, 560, 325, enemy_spells, [])


players = [player1,player2,player3]
enemies = [enemy1, enemy2, enemy3]
running = True
i = 0

print(bcolors.FAIL + bcolors.BOLD + "Enemy attack !!!" + bcolors.ENDC)

while running:
    print("==================================")

    print('\n\n')
    print(bcolors.FAIL+bcolors.BOLD+'Name                HP                               MP'+bcolors.ENDC)
    for player in players:
        player.get_stat()

    print('\n')
    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:
        player.choose_action()
        choice = input(bcolors.FAIL+"Choose action :"+bcolors.ENDC)
        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)

            enemies[enemy].take_damage(dmg)
            print("You attack ", enemies[enemy].name.replace(' ', ''), "for ", dmg, "points of damage.")
            if enemies[enemy].get_hp() == 0:
                print(bcolors.OKGREEN, enemies[enemy].name.replace(' ', ''), 'has died',bcolors.ENDC)
                del enemies[enemy]

        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("Choose Magic:")) - 1

        # return
            if magic_choice == -1:
                continue
            ''' magic_dmg = player.generate_spell_damage(magic_choice)
            spell = player.get_spell_name(magic_choice)
            cost = player.get_spell_mp_cost(magic_choice)'''

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL, "\n Not enough mp !!! \n", bcolors.ENDC)
                continue
            player.reduce_mp(spell.cost)

            if spell.type == 'white':
                player.heal(magic_dmg)
                print(bcolors.OKBLUE, '\n', spell.name, 'heals for ',magic_dmg, 'HP', bcolors.ENDC)
            elif spell.type == 'black':
                enemy = player.choose_target(enemies)
                dmg = player.generate_damage()
                enemies[enemy].take_damage(dmg)

                #enemy.take_damage(magic_dmg)
                print(bcolors.OKBLUE, '\n', spell.name, 'deals', magic_dmg, 'points of damage to ',enemies[enemy].name.replace(' ', ''), bcolors.ENDC)
        elif index == 2:
            player.choose_items()
            item_choice = int(input('Choose item: ')) - 1

        # return
            if item_choice == -1:
                continue

            if player.items[item_choice]['quantity'] == 0:
                print(bcolors.FAIL, "\n None left....", bcolors.ENDC)
                continue

            item = player.items[item_choice]['item']
            player.items[item_choice]['quantity'] -= 1

            if item.type == 'potion':
                player.heal(item.prop)
                print(bcolors.OKGREEN, '\n', item.name,' heals for', item.prop, 'HP', bcolors.ENDC)
            elif item.type == 'elixer':
                if item.name == 'MegaElixer':
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp

                player.hp = player.maxhp
                player.mp = player.maxmp
                print(bcolors.OKGREEN, item.name, 'Fully restores HP/MP',bcolors.ENDC)
            elif item.type == 'attack':
                enemy = player.choose_target(enemies)

                enemies[enemy].take_damage(item.prop)

                print(bcolors.OKGREEN, item.name, 'deals',item.prop, 'points of damage to', enemies[enemy].name, bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(bcolors.OKGREEN, enemies[enemy].name.replace(' ',''),'has died',bcolors.ENDC)
                    del enemies[enemy]
                # enemy.take_damage(item.prop)
# check if battle is over
    defeated_enemies = 0
    defeated_players = 0

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1
# check if player won
    if defeated_enemies >= 2:
        print(bcolors.OKGREEN, 'You win', bcolors.ENDC)
        running = False

# check if enemies won
    elif defeated_players >= 2:
        print(bcolors.FAIL, 'You have lost', bcolors.ENDC)
        running = False

# enemies attack phase
    for enemy in enemies:
        enemy_choice = random.randrange(0,3)
        if enemy_choice ==0:
            target = random.randrange(0,3)
            enemy_dmg = enemy.generate_damage()

            players[target].take_damage(enemy_dmg)
            print(bcolors.FAIL, enemy.name," attacks for ",players[target].name.replace(' ',''), enemy_dmg, "",bcolors.ENDC)
        if enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()
            # did enemy have mp ???
            enemy.reduce_mp(spell.cost)
            if spell.type == 'white':
                enemy.heal(magic_dmg)
                print(bcolors.OKBLUE, '\n', spell.name, 'heals',enemy.name,' for ', magic_dmg, 'HP', bcolors.ENDC)
            elif spell.type == 'black':
                target = random.randrange(0, 3)
                players[target].take_damage(magic_dmg)
                print(bcolors.OKBLUE, '\n', spell.name, 'deals', magic_dmg, 'points of damage to ',
                      players[target].name.replace(' ', ''), bcolors.ENDC)
                if players[target].get_hp() == 0:
                    print(bcolors.FAIL, players[target].name.replace(' ', ''), 'has died',bcolors.ENDC)
                    del players[target]#del players[player]


 #print('Enemy chose',spell,' damage is',magic_dmg)




