import random
import pygame
from pygame import mixer
from main import contentPath
from main import player

pygame.init()

mixer.music.load(contentPath+'Revelations.mp3')

class Equipment:
    def __init__(self, name, armor_increase, magic_resist_increase, special_effect):
        self.name = name
        self.armor_increase = armor_increase
        self.magic_resist_increase = magic_resist_increase
        self.special_effect = special_effect

class HeadEquipment(Equipment):
    def __init__(self, name, armor_increase, magic_resist_increase, special_effect):
        super().__init__(name, armor_increase, magic_resist_increase, special_effect)

class ChestEquipment(Equipment):
    def __init__(self, name, armor_increase, magic_resist_increase, special_effect):
        super().__init__(name, armor_increase, magic_resist_increase, special_effect)

class LegEquipment(Equipment):
    def __init__(self, name, armor_increase, magic_resist_increase, special_effect):
        super().__init__(name, armor_increase, magic_resist_increase, special_effect)

class FootEquipment(Equipment):
    def __init__(self, name, armor_increase, magic_resist_increase, special_effect):
        super().__init__(name, armor_increase, magic_resist_increase, special_effect)

class Weapon:
    def __init__(self, name, attack_damage, magic_damage, special_effects):
        self.name = name
        self.attack_damage = attack_damage
        self.magic_damage = magic_damage
        self.special_effects = special_effects

class HandWeapon(Weapon):
    def __init__(self, name, attack_damage, magic_damage, special_effects):
        super().__init__(name, attack_damage, magic_damage, special_effects)

class Spell(Weapon):
    def __init__(self, name, attack_damage, magic_damage, special_effects, mana_cost):
        super().__init__(name, attack_damage, magic_damage, special_effects)
        self.mana_cost = mana_cost

class Potion:
    def __init__(self, name, effect_type, healing_amount):
        self.name = name
        self.effect_type = effect_type
        self.healing_amount = healing_amount

class Entity:
    def __init__(self, name, level, currentEXP, maxEXP, currentHP, maxHP, mana, speed, armor, magic_resist, attack_damage, magic_damage):
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
        self.consumables = {'potion': None}
        self.skills = {'fireball': Spell("Fireball", 20, 10, "Burn", 10),
                       'heal': Spell("Heal", 0, 30, "Heal", 15),
                       'ice_shard': Spell("Ice Shard", 15, 15, "Freeze", 12),
                       'thunder_strike': Spell("Thunder Strike", 25, 5, "Paralyze", 20)}
        
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
        self.maxHP += 10
        self.mana += 10
        self.speed += 5
        self.armor += 5
        self.magic_resist += 5
        self.attack_damage += 5
        self.magic_damage += 5

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
                print("Mana insuffisant. Tour perdu , veuillez recharger votre mana.")

    def heal(self, amount):
        self.currentHP = min(self.maxHP, self.currentHP + amount)

    def take_damage(self, damage):
        self.currentHP -= damage
        if self.currentHP < 0:
            self.currentHP = 0

    def use_potion(self, potion):
        if potion.effect_type == "heal":
            self.currentHP = min(self.maxHP, self.currentHP + potion.healing_amount)
            print(f"{self.name} utilise {potion.name} et récupère {potion.healing_amount} points de vie.")

    def display_status(self):
        print(f"{self.name} (HP: {self.currentHP}/{self.maxHP}, Mana: {self.mana}, Speed: {self.speed}, Armor: {self.armor}, Magic Resist: {self.magic_resist}, Attack Damage: {self.attack_damage}, Magic Damage: {self.magic_damage})")

class Player(Entity):
    def __init__(self, name, currentHP, maxHP, mana, speed, armor, magic_resist, attack_damage, magic_damage):
        super().__init__(name, currentHP, maxHP, mana, speed, armor, magic_resist, attack_damage, magic_damage)

class PNJ(Entity):
    def __init__(self, name, currentHP, maxHP, mana, speed, armor, magic_resist, attack_damage, magic_damage):
        super().__init__(name, currentHP, maxHP, mana, speed, armor, magic_resist, attack_damage, magic_damage)

class Enemy(Entity):
    def __init__(self, name, currentHP, maxHP, mana, speed, armor, magic_resist, attack_damage, magic_damage, monster_type):
        super().__init__(name, 1, 0, 0, currentHP, maxHP, mana, speed, armor, magic_resist, attack_damage, magic_damage)
        self.monster_type = monster_type


    def display_ascii(self):
        if self.monster_type == "slime":
            slime_ascii = """
                             ██████████                
                     ████████░░░░░░░░░░████████        
                   ██░░░░░░░░░░░░░░░░░░░░░░░░░░██      
                 ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██    
               ██░░░░░░░░░░░░░░░░░░            ░░██    
               ██░░░░░░░░░░░░░░                  ░░██  
             ██░░░░░░░░░░                        ░░░░██
             ██░░░░░░░░░░                        ░░░░██
             ██░░░░░░░░░░        ██        ██      ░░██
             ██░░░░░░░░          ██        ██      ░░██
             ██░░░░░░░░          ██        ██      ░░██
             ██░░░░░░░░                            ░░██
             ██░░░░░░░░░░                          ░░██
             ██░░░░░░░░░░░░                        ░░██
             ██░░░░░░░░░░░░░░                      ░░██
             ██░░░░░░░░░░░░░░░░░░                ░░░░██
             ████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░████
                 ██████████████████████████████████ 
            """
            print(slime_ascii)
        elif self.monster_type == "ghoul":
            ghoul_ascii = """
                        ___
                      .';:;'.
                     /_' _' /\   __
                     ;a/ e= J/-'"  '.
                     \ ~_   (  -'  ( ;_ ,.
                      L~"'_.    -.  \ ./  )
                      ,'-' '-._  _;  )'   (
                    .' .'   _.'")  \  \(  |
                   /  (  .-'   __\{`', \  |
                  / .'  /  _.-'   "  ; /  |
                 / /    '-._'-,     / / \ (
              __/ (_    ,;' .-'    / /  /_'-._
             `"-'` ~`  ccc.'   __.','     \j\L\
                              .='/|\7      
                    ' `
            """
            print(ghoul_ascii)
        elif self.monster_type == "orc":
            orc_ascii = """
           ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀            ⢀⣀⣀⣀⣀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣴⣾⣿⣿⣿⣿⣿⣿⣶⣄⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⠿⢿⣿⣿⣿⣿⣆⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⠁⠀⠿⢿⣿⡿⣿⣿⡆⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣦⣤⣴⣿⠃⠀⠿⣿⡇⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⡿⠋⠁⣿⠟⣿⣿⢿⣧⣤⣴⣿⡇⠀
            ⠀⠀⠀⠀⢀⣠⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀⠘⠁⢸⠟⢻⣿⡿⠀⠀
            ⠀⠀⠙⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣴⣇⢀⣤⠀⠀⠀⠀⠘⣿⠃⠀⠀
            ⠀⠀⠀⠀⠀⢈⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣴⣿⢀⣴⣾⠇⠀⠀⠀
            ⠀⠀⣀⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀
            ⠀⠀⠉⠉⠉⠉⣡⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠃⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⡿⠟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀
            ⠀⠀⣴⡾⠿⠿⠿⠛⠋⠉⠀⢸⣿⣿⣿⣿⠿⠋⢸⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⡿⠟⠋⠁⠀⠀⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀  
            """
            print(orc_ascii)
        elif self.monster_type == "killing hand":
            killing_hand_ascii = """
                                @**++%%@           
                             #**#+#*++#@@         
                             %@@@*@@@%*@@@        
                             #%@#*#@@*#@@@        
                             #****++*#%@@         
                             %**#**+*@@@          
                             @######@@@           
                              @@@@@@@@            
                              *%%@@@@@            
                             %#%%@@@%+#           
                           @@@+*=:::**%@@         
                         %@@@@=*#@@%**%@@@@       
                         @@@@@-*##%##*%@@@@@      
                        @@@@@@*##%###*@@@@@@@     
                       @@@@@@%*#%%%##*%@@@@@@@    
                       @@@@@@==+#==#**%@@@@@@@    
                      @@#%@@@%=:::::-=@@@@@@@@    
                      @#=%@@#%@@%=+@@%%@@@@@@@@   
                     @@@@@@@%@@@#*@@@#*@@@@@@@@@  
                     @@@@@@@@@@@@@@@@#+@@  @@@@@  
                    @@%@@@@@@@@@@@@@@@@@@   @@@@  
                   @%#@@ @@@%@@@@@@@@@@@    @@@@@ 
                  @#*@@   @@#@@@@@@@@@@@     @@@@ 
                  @#%@    @%#@@@@@@@@@@@       @@ 
                         @@#*@@@@@@@#@@           
                         @@**@@%#@@%*@@           
                         @@%%@@#+@@*#@            
                          @@@@@**@%+%@            
                                 @@@@             

            """
            print(killing_hand_ascii)
        elif self.monster_type == "weak devil":
            weak_devil_ascii = """
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡠⠤⣤⣤⣀⡀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢧⢸⣄⠉⠁⠉⢉⡲⢤
⠀⠀⠀⢀⡠⠴⠊⣭⠃⠀⣀⣀⡤⠴⢶⠤⠤⢤⣀⠀⢸⠸⠈⠣⡀⢠⠃⠀⠀
⠀⢀⢔⡉⢀⣀⠐⠐⢧⣾⣴⣿⡿⠀⠀⡏⡄⠀⠀⢱⡧⢀⡠⠤⠬⣎⣧⠀⠀
⠐⠋⠁⠀⠀⢸⠔⢢⣿⣿⣿⡿⠃⠀⢠⠃⠀⠠⢚⣉⣠⢯⠀⠀⠀⠈⠛⠀⠀
⠀⠀⠀⠀⠀⠈⠀⣼⠙⠛⠉⠀⢀⣠⢊⠆⠀⠀⠈⣴⠃⣼⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⡌⢦⣀⣀⠬⡺⠕⠁⠀⠀⠀⢀⠟⠸⡟⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⡇⣀⠀⡦⢄⣠⣾⣿⣾⣦⠀⢀⠼⢱⠁⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠳⡏⠉⠁⣀⠈⠻⣿⣿⠉⠀⠈⢠⠇⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⡏⠁⠈⠙⣿⢟⡀⢀⠄⢹⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣀⡤⠀⡤⠃⠫⡉⠙⠃⠁⠀⠈⠠⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠰⠐⡀⠀⠀⠀⠀⣨⠆⠀⣀⠤⠒⠀⠙⠣⠤⠐⠒⠒⠄⡀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢀⡤⠒⠊⡉⠀⠀⡜⠄⠀⠘⣏⡄⠀⣀⡠⠤⠠⢄⠘⡄⠀
⠀⠀⠀⠀⠀⠀⠀⢸⠀⡔⣳⠒⠒⠚⣿⠀⠰⢎⠀⠈⠁⠀⠀⠀⠀⢠⠇⡼⠀
⠀⠀⠀⠀⠀⠀⠀⠈⠳⢌⡘⢄⡀⠀⠘⠦⣀⣉⣉⣁⠒⣄⠀⠀⠀⣸⢼⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣈⡧⣸⠀⠀⠀⠀⢠⠔⠋⢀⡼⠀⠀⠀⠉⠉⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠓⠊⠁⠀⠀⠀⠀⠈⠙⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠠⠤⠠⠤⠴⠠⠠⠠⠤⠤⠀⠠⠲⠀⠆⠤⠦⠴⠰⠀⠀⠀⠀
              """
            print(weak_devil_ascii)
        elif self.monster_type == "swarmooh":
            swarmooh_ascii = """
        ⠀⠀⠀⠀⠀⣠⡄⡀⠀⠀⠀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠹⣿⣇⠀⠀⢻⡿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⣠⣾⠿⣿⣶⣴⣶⣶⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⣰⠏⠈⠀⣿⢫⣩⣤⣙⡧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⢸⡟⠀⢀⣀⣿⣭⣿⡳⡟⠁⠀⠀⠀⢀⣤⣴⡷⣆⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⢠⡏⠀⠀⠈⠁⣠⡿⠶⠿⠃⠀⠀⣠⠞⠋⠀⠀⠀⠉⠀⠉⠉⠳⢦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⢸⠁⠀⠀⠀⢰⡏⠀⠀⠀⠀⢀⡾⡁⠀⠀⠀⠰⠶⢦⣀⠀⠀⠀⠀⠙⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⢸⠀⠀⠀⠀⠸⣇⠀⠀⠀⣠⠏⠀⠀⣄⡀⡼⠛⠓⢦⡈⠓⠀⠀⠀⠀⠘⢦⣀⡀⠀⠀⢀⣀⣀⣀⠀⠀⠀
        ⠀⢸⠀⠀⠀⠀⠀⠉⠳⣄⣠⠏⠀⠀⠀⠛⢻⡇⠀⠀⠀⠳⣄⣤⣀⡀⠀⣀⣠⣬⡟⣠⡶⠛⠉⠉⠙⢷⡄⠀
        ⠀⠸⣇⠀⠀⠀⠀⠀⠀⠈⠉⠀⠀⠒⠦⠀⠀⠻⣄⡀⢀⣰⠋⠁⠘⣷⠋⠉⠀⣾⣷⠏⠀⠀⠀⣀⠀⠀⢷⠀
        ⠀⠈⠷⡿⡄⠀⠈⠁⠀⠀⠀⠀⠀⠀⠀⡿⢤⠞⢳⡉⠉⠀⠀⠀⠀⠸⠦⠤⠾⣽⠁⡄⠀⡶⣶⡿⢀⡀⣿⡀
        ⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠻⣄⣀⡴⢶⡀⢀⣀⣄⡀⣼⠀⠁⠈⡷⣿⣵⡄⠙⢹⠁
        ⠀⠀⠀⠀⢹⣄⣤⡀⠀⣤⢠⣄⢀⠀⢀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠛⠛⣱⣟⢽⣋⣀⣤⣄⣳⡿⣿⣰⣶⡟⠀
        ⠀⠀⠀⠀⠀⠉⠘⡇⠀⠉⠀⠻⠞⠀⠈⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣃⣼⣴⠟⠉⠁⠈⠉⠀⢷⣿⠉⠁⠀
        ⠀⠀⠀⠀⠀⠀⠀⣷⠀⠀⠀⠀⠀⠀⠀⠳⣄⠀⣠⠖⢢⣤⡾⢳⡄⣼⡿⢷⡮⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠁⠀⠀⠀⠀⠀⠙⠋⠠⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⣹⠂⠀⠀⠀⢶⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⣴⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣦⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⢿⡄⠀⠀⠀⠀⠀⣄⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠀⠀⢹⡂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠈⢻⠂⠀⠀⠀⠀⣿⣧⡄⣰⡀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⡄⠀⠀⢡⣧⣾⠟⠀⠀⠀⠀⠀⣴⡦⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⣠⡟⠀⣤⣼⠁⠀⠀⠀⠉⠁⠀⠀⠀⠀⠀⠀⠈⠀⠀⣼⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⣠⠤⠤⠖⠋⠀⠀⠈⠁⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⡆⠀⠀⠀⢠⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⣸⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠁⠀⠀⢠⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⢠⠏⠀⠀⠀⠀⠀⠀⣀⣀⠀⠀⠀⠀⣀⡿⠲⢦⡀⠀⠀⠀⠀⠀⠈⢸⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⣼⠀⠀⠀⠀⠀⠀⠀⢻⠋⠀⠀⠀⣠⡾⠁⠀⠀⢻⠀⠀⠀⠀⠀⠀⢀⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⢧⡀⠀⠀⠀⡤⢤⣀⣀⣀⣀⣠⡾⠋⠀⠀⠀⠀⢸⡄⠀⠀⠀⢀⠀⢘⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠈⠛⠒⠛⠾⠃⠀⠀⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⣸⠀⠀⠀⠸⠾⠁⠈⠉⢳⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⢢⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⠶⠶⣾⣄⠀⠀⠀⠀⠀⢰⣷⡾⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⠛⠛⠛⠛⠛⠛⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            """
            print(swarmooh_ascii)

def generate_random_enemy(player_level):
    monster_types = ["slime", "ghoul", "orc", "weak devil", "swarmooh"]
    special_monster_chance = random.random()
    
    if special_monster_chance < 0.2: 
        return Enemy("killing Hand", player_level * 100, player_level * 100, player_level * 10, player_level * 8,player_level * 25, player_level * 20, player_level * 30, player_level * 15, "killing hand")
    else:
        monster_type = random.choice(monster_types)
        return Enemy(monster_type.capitalize(), player_level * 50, player_level * 10, player_level * 2, player_level,player_level * 2, player_level, player_level * 5, player_level * 2, monster_type)

def combat(player, enemy):
    print(f"{enemy.monster_type} apparaît !")
    enemy.display_ascii()
    print(f"{player.name} (Niveau {player.level}) vs {enemy.name} (Niveau {enemy.level})")

    mixer.music.play(-1)  

    while player.currentHP > 0 and enemy.currentHP > 0:
        print("\n--------------------")
        player.display_status()
        print(f"{enemy.name} (HP: {enemy.currentHP}/{enemy.maxHP}, Armor: {enemy.armor}, Magic Resist: {enemy.magic_resist}, Attack Damage: {enemy.attack_damage}, Magic Damage: {enemy.magic_damage})")

        print("\n1. Attaquer")
        print("2. Utiliser une compétence")
        print("3. Utiliser une potion")
        print("4. Fuir")

        choice = input("Choisissez votre action (1-4): ")

        if choice == "1":
            damage_dealt = player.attack_enemy(enemy)
            print(f"{player.name} inflige {damage_dealt} points de dégâts à {enemy.name}.")
        elif choice == "2":
            print("Compétences disponibles:")
            for i, skill_name in enumerate(player.skills.keys(), start=1):
                print(f"{i}. {skill_name} (Coût en mana: {player.skills[skill_name].mana_cost})")

            skill_choice = input("Choisissez une compétence (1-4): ")
            if skill_choice.isdigit() and 1 <= int(skill_choice) <= 4:
                selected_skill = list(player.skills.values())[int(skill_choice) - 1]
                player.use_skill(selected_skill, enemy)
            else:
                print("ERREUR, commande pas prise en compte")
        elif choice == "3":
            print("Potions disponibles:")
            for i, potion_name in enumerate(player.consumables.keys(), start=1):
                print(f"{i}. {potion_name}")

            potion_choice = input("Choisissez une potion (1-3): ")
            if potion_choice.isdigit() and 1 <= int(potion_choice) <= 3:
                selected_potion = list(player.consumables.values())[int(potion_choice) - 1]
                player.use_potion(selected_potion)
            else:
                print("ERREUR, commande pas prise en compte ")
        elif choice == "4":
            print("Vous avez fui le combat.")
            return False
        else:
            print("ERREUR, commande pas prise en compte")

        if enemy.currentHP > 0:
            enemy_damage = random.randint(1, enemy.attack_damage)
            player.take_damage(enemy_damage)
            print(f"{enemy.name} inflige {enemy_damage} points de dégâts à {player.name}.")
            print(f"{player.name} a perdu {enemy_damage} points de vie.")

    if player.currentHP > 0:
        exp_gained = enemy.level * 250 
        player.gain_exp(exp_gained)
        print(f"{player.name} a vaincu {enemy.name}!")
        print(f"EXP gagné: {exp_gained}")

        if player.currentEXP >= player.maxEXP:
            print(f"{player.name} est monté de niveau!")
            player.level_up()
    else:
        print(f"{enemy.name} a vaincu {player.name} .")
    
mixer.music.stop()