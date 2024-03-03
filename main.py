import random
import pygame
import sys
from pygame import mixer

pygame.init()

mixer.music.load('Revelations.mp3')


class Item:
    def __init__(self, name, description, price, item_type):
        self.name = name
        self.description = description
        self.price = price
        self.item_type = item_type

    def apply_effect(self, player, enemy=None):
        if self.item_type == "Green Persimmon":
            percentage_to_heal = 0.5
            player.heal(percentage_to_heal)
            print(f"{player.name} used a Green Persimmon and healed {percentage_to_heal * 100}% of max HP.")

            player.inventory.remove(self)
        elif self.item_type == "Strength Potion":
            player.boost_attack(10)
            print(f"{player.name} used a Strength Potion and increased their attack by 10.")
            player.inventory.remove(self)
        elif self.item_type == "Speed Potion":
            player.attack_enemy(enemy)
            player.attack_enemy(enemy)
            print(f"{player.name} used a Speed Potion and attacked twice.")
            player.inventory.remove(self)
class Entity:
    def __init__(self, name, level=1, currentEXP=0, maxEXP=0, currentHP=100, maxHP=100, mana=50, speed=10, armor=20,
                 magic_resist=15, attack_damage=15, magic_damage=30):
        self.name = name
        self.level = level
        self.currentEXP = currentEXP
        self.maxEXP = maxEXP
        self.currentHP = currentHP
        self.maxHP = maxHP
        self.mana = mana
        self.speed = speed
        self.armor = armor
        self.magic_resist = magic_resist
        self.attack_damage = attack_damage
        self.magic_damage = magic_damage
        self.equipments = {'head': None, 'chest': None, 'leg': None, 'foot': None}
        self.weapons = {'hand_weapon': None, 'book_spell': None}

    def gain_exp(self, exp):
        self.currentEXP += exp
        print(f"{self.name} a gagné {exp} points d'expérience!")

        while self.currentEXP >= self.maxEXP:
            self.level_up()
            self.currentEXP -= self.maxEXP

    def level_up(self):
        print(f"{self.name} est monté de niveau!")
        self.level += 1
        self.maxEXP = self.level * 250
        self.maxEXP *= 1.2  
        self.maxHP += 10
        self.currentHP = self.maxHP
        self.mana += 10
        self.max_mana = self.mana
        self.speed += 5
        self.armor += 5
        self.magic_resist += 5
        self.attack_damage += 5
        self.magic_damage += 5
        self.display_status()
    
    def display_status(self):
        print(f"{self.name} (Niveau {self.level}):")
        print(f"EXP: {self.currentEXP}/{self.maxEXP}")
        print(f"HP: {self.currentHP}/{self.maxHP}, Mana: {self.mana}")
        print(f"Armor: {self.armor}, Magic Resist: {self.magic_resist}")
        print(f"Attaque: {self.attack_damage}, Magie: {self.magic_damage}")

    def display_status(self):
        print(f"{self.name} (Niveau {self.level}):")
        print(f"EXP: {self.currentEXP}/{self.maxEXP}")
        print(f"HP: {self.currentHP}/{self.maxHP}, Mana: {self.mana}")
        print(f"Armor: {self.armor}, Magic Resist: {self.magic_resist}")
        print(f"Attaque: {self.attack_damage}, Magie: {self.magic_damage}")

    def attack_enemy(self, enemy):
        damage = random.randint(1, self.attack_damage)
        enemy.take_damage(damage)
        return damage

    def use_skill(self, skill, target):
        if skill.name == "Heal":
            self.heal(skill.magic_damage)
            print(f"{self.name} utilise {skill.name} et récupère {skill.magic_damage} points de vie.")
        else:
            if self.mana >= skill.mana_cost:
                self.mana -= skill.mana_cost
                damage = random.randint(1, skill.magic_damage)
                target.take_damage(damage)
                print(f"{self.name} utilise {skill.name} et inflige {damage} points de dégâts à {target.name}.")
            else:
                print("Mana insuffisant. Tour perdu, veuillez recharger votre mana.")
                
    def boost_attack(self, amount):
        self.attack_damage += amount

    def boost_defense(self, amount):
        self.armor += amount

    def boost_max_hp(self, amount):
        self.maxHP += amount
        self.heal(amount)

    def boost_speed(self, amount):
        self.speed += amount

    def take_damage(self, damage):
        self.currentHP -= damage
        if self.currentHP < 0:
            self.currentHP = 0

    def fireball(self, enemy):
        if self.mana >= 20:
            self.mana -= 20
            damage = int(0.1 * enemy.maxHP) 
            enemy.take_damage(damage)
            print(f"{self.name} used Fireball and dealt {damage} damage to {enemy.name}.")
        else:
            print("Not enough mana to use Fireball. Turn skipped.")

    def victory(self):
        print(f"Vous avez vaincu l'ennemi !")
        self.coins += random.randint(0, 15)
        print(f"Vous avez gagné {self.coins} pièces !")

    def display_status(self):
        print(
            f"{self.name} (HP: {self.currentHP}/{self.maxHP}, Mana: {self.mana}, Speed: {self.speed}, Armor: {self.armor}, Magic Resist: {self.magic_resist}, Attack Damage: {self.attack_damage}, Magic Damage: {self.magic_damage})")


class Player(Entity):
    def __init__(self, name, currentHP, maxHP, mana, speed, armor, magic_resist, attack_damage, magic_damage):
        super().__init__(name, 1, 0, 250, currentHP, maxHP, mana, speed, armor, magic_resist, attack_damage, magic_damage)
        self.max_mana = mana
        self.mana = mana
        self.coins = 0
        self.inventory = []
        self.exp = 0
    def heal(self, percentage):
        mana_cost = 15

        if self.mana >= mana_cost:
            self.mana -= mana_cost
            amount_to_heal = int(percentage * self.maxHP)
            self.currentHP = min(self.currentHP + amount_to_heal, self.maxHP)
            print(f"{self.name} used Heal and recovered {amount_to_heal} HP.")
        else:
            print("Not enough mana to use Heal. Turn skipped.")


    def use_item(self, item, enemy=None):
        item.apply_effect(self, enemy)

    def show_inventory(self):
        print(f"\nInventory of {self.name}:")
        for i, item in enumerate(self.inventory, start=1):
            print(f"{i}. {item.name} - {item.description}")
        print(f"{len(self.inventory) + 1}. Return")

    def choose_inventory_item(self):
        while True:
            self.show_inventory()
            choice = input("Choose the number corresponding to your choice : ")
            if choice.isdigit() and 1 <= int(choice) <= len(self.inventory) + 1:
                return int(choice)
            else:
                print("Invalid choice. Please choose again.")

    def add_item(self, item):
        self.inventory.append(item)

class PNJ(Entity):
    def __init__(self, name, currentHP, maxHP, mana, speed, armor, magic_resist, attack_damage, magic_damage):
        super().__init__(name, currentHP, maxHP, mana, speed, armor, magic_resist, attack_damage, magic_damage)


class Enemy(Entity):
    def __init__(self, name, currentHP, maxHP, mana, speed, armor, magic_resist, attack_damage, magic_damage,
                 monster_type):
        super().__init__(name, 1, 0, 0, currentHP, maxHP, mana, speed, armor, magic_resist

, attack_damage, magic_damage)
        self.monster_type = monster_type

    def attack_enemy(self, player):
        damage = random.randint(1, self.attack_damage)
        player.take_damage(damage)
        return damage
    def display_ascii(self):
        if self.monster_type == "slime":
            slime_ascii = """
                             ██████████                
                             ██████████                
                             ██████████                
            """
            print(slime_ascii)
        elif self.monster_type == "ghoul":
            ghoul_ascii = """
                        ___
                      .';:;'.
                    ' `
            """
            print(ghoul_ascii)
        elif self.monster_type == "phantom":
            phantom_ascii = """
           ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀            ⢀⣀⣀⣀⣀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣴⣾⣿⣿⣿⣿⣿⣶⣄⠀⠀⠀
            """
            print(phantom_ascii)
        elif self.monster_type == "killing hand":
            killing_hand_ascii = """
                                @**++%%@           
                             #**#+#*++#@@         
                             %@@@*@@@%*@@@        
                             #%@#*#@@*#@@@        
                             #****++*#%@@         
                             %**#**+*@@@          
            """
            print(killing_hand_ascii)
        elif self.monster_type == "weak devil":
            weak_devil_ascii = """
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡠⠤⣤⣤⣀⡀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢧⢸⣄⠉⠁⠉⢉⡲⢤
⠀⠀⠀⢀⡠⠴⠊⣭⠃⠀⣀⣀⡤⠴⢶⠤⠤⢤⣀⠀⢸⠸⠈⠣⡀⢠⠃⠀⠀
              """
            print(weak_devil_ascii)
        elif self.monster_type == "swarmooh":
            swarmooh_ascii = """
        ⠀⠀⠀⠀⠀⣠⡄⡀⠀⠀⠀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠹⣿⣇⠀⠀⢻⡿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            """
            print(swarmooh_ascii)


def generate_random_enemy(player_level):
    monster_types = ["slime", "ghoul", "phantom", "weak devil", "swarmooh"]
    special_monster_chance = random.random()

    if special_monster_chance < 0.2:
        return Enemy("killing Hand", player_level * 100, player_level * 100, player_level * 10, player_level * 8,
                     player_level * 25, player_level * 20, player_level * 30, player_level * 15, "killing hand")
    else:
        monster_type = random.choice(monster_types)
        max_hp = player_level * 50
        return Enemy(monster_type.capitalize(), max_hp, max_hp, player_level * 2, player_level,
                     player_level * 2, player_level, player_level * 5, player_level * 2, monster_type)


def combat(player, enemy):
    print(f"{enemy.monster_type} apparaît !")
    enemy.display_ascii()
    print(f"{player.name} (Niveau {player.level}) vs {enemy.name} (Niveau {enemy.level}")

    mixer.music.play(-1)

    while player.currentHP > 0 and enemy.currentHP > 0:
        print("\n--------------------")
        player.display_status()
        print(
            f"{enemy.name} (HP: {enemy.currentHP}/{enemy.maxHP}, Armor: {enemy.armor}, Magic Resist: {enemy.magic_resist}, Attack Damage: {enemy.attack_damage}, Magic Damage: {enemy.magic_damage})")

        print("\n1. Attaquer")
        print("2. Utiliser une compétence")
        print("3. Inventaire")
        print("4. Fuir")

        choice = input("Choisissez votre action (1-4): ")

        if choice == "1":
            damage_dealt = player.attack_enemy(enemy)
            print(f"{player.name} inflige {damage_dealt} points de dégâts à {enemy.name}.")

            if enemy.currentHP > 0:
                damage_taken = enemy.attack_enemy(player)
                print(f"{enemy.name} inflige {damage_taken} points de dégâts à {player.name}.")
                    

        elif choice == "2":
            print("Compétences:")
            print("1. Focus")
            print("2. Fireball")
            print("3. Swift")
            print("4. Heal")
            skill_choice = input("Choose a skill (1-4), 5 pour revenir en arrière: ")

            if skill_choice.isdigit():
                skill_choice = int(skill_choice)
                if 1 <= skill_choice <= 4:
                    if skill_choice == 1:
                        player.boost_attack(5)
                        print(f"{player.name} used Focus and increased their attack by 5.")
                    elif skill_choice == 2:
                        player.fireball(enemy)
                        print(f"{player.name} used Fireball.")
                    elif skill_choice == 3:
                        player.boost_speed(2)
                        print(f"{player.name} used swift and increased their speed by 2.")
                    elif skill_choice == 4:
                        player.heal()
                elif skill_choice == 5:
                    continue
                else:
                    print("Invalid choice.")
                    
            if enemy.currentHP > 0:
                damage_taken = enemy.attack_enemy(player)
                print(f"{enemy.name} inflige {damage_taken} points de dégâts à {player.name}.")

        elif choice == "3":
            print("b pour revenir en arrière")
            inventory_choice = player.choose_inventory_item()
            
            if inventory_choice != len(player.inventory) + 1:
                item = player.inventory[inventory_choice - 1]
                player.use_item(item, enemy)
                
                if enemy.currentHP > 0:
                    damage_taken = enemy.attack_enemy(player)
                    print(f"{enemy.name} inflige {damage_taken} points de dégâts à {player.name}.")
                    
            elif inventory_choice == "b":
                continue

        elif choice == "4":
            print("Vous avez fui le combat.")
            mixer.music.stop()
            return False

        else:
            print("Choix invalide. Essayez à nouveau.")
            continue

        if player.currentHP <= 0:
            print("Vous avez été vaincu !")
            mixer.music.stop()

            while True:
                choice = input("Voulez-vous recommencer? (oui/non): ").lower()
                if choice == "oui":
                    player = Player("Player", 100, 100, 50, 10, 20, 15, 15, 30)
                    enemy = generate_random_enemy(player.level)
                    combat(player, enemy)
                    break
                elif choice == "non":
                    print("Merci d'avoir joué. À bientôt !")
                    sys.exit()
                else:
                    print("Choix invalide. Veuillez saisir 'oui' ou 'non'.")

        if enemy.currentHP <= 0:
            exp_gained = enemy.level * 250
            player.gain_exp(exp_gained)
            enemy.level_up()
            print(f"{player.name} a vaincu {enemy.name}!")
            print(f"EXP gagné: {exp_gained}")

            if player.currentEXP >= player.maxEXP:
                print(f"{player.name} est monté de niveau!")
                player.level_up()

            player.coins += random.randint(0, 15)
            print(f"Vous avez gagné {player.coins} pièces !")

            mixer.music.stop()
            return True

def merchant_room(player):
    print("You encountered a merchant room!")
    print("Merchant: Welcome, adventurer! Take a look at my wares.")

    items_for_sale = [Item("Green Persimmon", "A healing item that restores 50% of your max health", 10, "Green Persimmon"),
                  Item("Strength Potion", "Adds 10 damage to your attack for 3 turns", 10, "Strength Potion"),
                  Item("Speed Potion", "Allows the player to attack twice", 15, "Speed Potion")]


    random_items = random.sample(items_for_sale, k=min(4, len(items_for_sale)))

    while True:
        print("Available items for purchase:")
        for i, item in enumerate(random_items, start=1):
            print(f"{i}. {item.name} - {item.description} (Price: {item.price} coins)")

        choice = input("Choose an item to buy (1-4), or choose '5' to exit the merchant room: ")

        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= 4:
                selected_item = random_items[choice - 1]
                if player.coins >= selected_item.price:
                    player.coins -= selected_item.price
                    player.add_item(selected_item)
                    print(f"You bought a {selected_item.name} for {selected_item.price} coins.")
                else:
                    print("You don't have enough coins to buy that item.")
            elif choice == 5:
                print("You chose to exit the merchant room.")
                break
            else:
                print("Invalid choice.")
        else:
            print("Invalid choice.")

def choose_room(player):
    while True:
        print("1. Room 1")
        print("2. Room 2")
        print("3. Room 3")
        print("4. Exit the Dungeon")
        print(f"Coins: {player.coins}")

        second_choice = input("Choose a room (1-3), or choose '4' to exit the dungeon: ")

        if second_choice == "1":
            print("You entered Room 1.")
            encounter_chance = random.random()
            if encounter_chance < 0.5:
                enemy = generate_random_enemy(player.level)
                if not combat(player, enemy):
                    continue  
            elif 0.5 <= encounter_chance < 0.7:
                merchant_room(player)
        elif second_choice == "2":
            print("You entered Room 2.")
            encounter_chance = random.random()
            if encounter_chance < 0.5:
                enemy = generate_random_enemy(player.level)
                if not combat(player, enemy):
                    continue  
            elif 0.5 <= encounter_chance < 0.7:
                merchant_room(player)
        elif second_choice == "3":
            print("You entered Room 3.")
            encounter_chance = random.random()
            if encounter_chance < 0.5:
                enemy = generate_random_enemy(player.level)
                if not combat(player, enemy):
                    continue  
            elif 0.5 <= encounter_chance < 0.7:
                merchant_room(player)
        elif second_choice == "4":
            print("You chose to exit the dungeon.")
            break  
        else:
            print("Invalid choice.")


player = Player("Player", 100, 100, 50, 10, 20, 15, 15, 30)
enemy = generate_random_enemy(player.level)
combat(player, enemy)

if player.currentHP > 0:
    choose_room(player)