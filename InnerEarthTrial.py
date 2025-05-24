import random
import time

'''
Inner Earth Trial is a text-based RPG where you create a character, choosing from classes like Warrior, Witch, or Doctor, each with unique stats and skills. 
Battle progressively tougher monsters, such as Giant Rats and Dragons, using attacks, skills, and potions, while managing stamina. 
Defeat enemies to earn gold, level up, and boost your stats. Visit the shop to buy potions, attack boosts, or temporary skill enhancements. 
With critical hits, monster regeneration, and strategic choices like resting or running, your goal is to defeat all monsters and claim victory in this challenging adventure!
'''

# Player data dictionary to store character attributes
PLAYER = {
    "name": "",              # Player's chosen name
    "class": "",             # Selected character class (warrior, witch, doctor)
    "level": 1,              # Current player level
    "hp": 0,                 # Current health points
    "max_hp": 0,             # Maximum health points
    "attack": 0,             # Base attack damage
    "gold": 20,              # Currency for buying items
    "potions": 2,            # Number of healing potions
    "skill_name": "",        # Name of the class-specific skill
    "skill_damage": 0,       # Damage dealt by the skill
    "current_monster_index": 0,  # Tracks progress through monster list
    "stamina": 10,           # Stamina for performing actions in combat
    "skill_boost": 0         # Temporary skill damage boost from shop
}

# List of character classes with their stats and abilities
CLASSES = [
    {"name": "warrior", "hp": 100, "attack": 12, "skill_name": "Power Strike", "skill_damage": 20, "skill_desc": "Deals 20 extra damage."},
    {"name": "witch", "hp": 80, "attack": 14, "skill_name": "Fireball", "skill_damage": 20, "skill_desc": "Deals 20 extra damage."},
    {"name": "doctor", "hp": 90, "attack": 8, "skill_name": "Healing Touch", "skill_damage": 20, "skill_desc": "Heals 20 HP and deals 20 damage."}
]

# List of monsters with their stats and rewards
MONSTERS = [
    {"name": "Giant Rat", "hp": 20, "attack": 7, "gold": 30},
    {"name": "Goblin", "hp": 40, "attack": 10, "gold": 50},
    {"name": "Dragon", "hp": 100, "attack": 15, "gold": 100, "regen": 10}  # Dragon has HP regeneration
]

# Shop items available for purchase
SHOP_ITEMS = [
    {"name": "Health Potion", "cost": 15, "effect": "potion", "desc": "Heals 50 HP."},
    {"name": "Attack Boost", "cost": 20, "effect": "attack", "value": 3, "desc": "Adds 3 to Attack."},
    {"name": "HP Boost", "cost": 30, "effect": "hp", "value": 15, "desc": "Adds 15 to Max HP and heals 15 HP."},
    {"name": "Skill Boost", "cost": 25, "effect": "skill_boost", "value": 10, "desc": "Next skill deals +10 damage (one fight)."}
]

# Game constants
POTION_HEAL_AMOUNT = 50     # Amount of HP restored by a potion
MAX_SKILL_USES = 3          # Maximum uses of a skill per fight
MAX_STAMINA = 10            # Maximum stamina for combat actions
STAMINA_REGEN_ON_REST = 2   # Stamina regained when resting
CRIT_CHANCE = 0.2           # Probability of landing a critical hit
CRIT_MULTIPLIER = 1.5       # Damage multiplier for critical hits

# Create player character by choosing a name and class
def create_character():
    print("Welcome to Inner Earth Trial!")
    print('Are you ready for the trial, little challenger?')
    PLAYER["name"] = input("What's your name? ")  # Get player's name
    print(f"Hi, {PLAYER['name']}! Choose your class:")

    # Display available classes with their stats
    for i in range(len(CLASSES)):
        cls = CLASSES[i]
        print(f"{i + 1}. {cls['name'].capitalize()}")  # Show 1-based index for user
        print(f"   HP: {cls['hp']}, Attack: {cls['attack']}")
        print(f"   Skill: {cls['skill_name']} - {cls['skill_desc']}")

    # Handle class selection
    while True:
        choice = input("Pick a class number: ")
        if choice.isdigit():
            choice_index = int(choice) - 1  # Convert to 0-based index
            if 0 <= choice_index < len(CLASSES):
                cls = CLASSES[choice_index]
                PLAYER["class"] = cls["name"]
                PLAYER["hp"] = cls["hp"]
                PLAYER["max_hp"] = cls["hp"]
                PLAYER["attack"] = cls["attack"]
                PLAYER["skill_name"] = cls["skill_name"]
                PLAYER["skill_damage"] = cls["skill_damage"]
                print(f"You picked {cls['name'].capitalize()}!")
                time.sleep(0.5)
                break
        print("Invalid choice.")

# Display player's current stats
def show_stats():
    print("\n--- Your Stats ---")
    print(f"Name: {PLAYER['name']}")
    print(f"Class: {PLAYER['class'].capitalize()}")
    print(f"Level: {PLAYER['level']}")
    print(f"HP: {PLAYER['hp']}/{PLAYER['max_hp']}")
    print(f"Attack: {PLAYER['attack']}")
    print(f"Gold: {PLAYER['gold']}")
    print(f"Potions: {PLAYER['potions']}")
    print(f"Skill: {PLAYER['skill_name']} (+{PLAYER['skill_damage']} damage, {MAX_SKILL_USES} uses per fight)")
    if PLAYER["skill_boost"] > 0:
        print(f"Skill Boost Active: +{PLAYER['skill_boost']} to next skill")
    input("Press Enter...")

# Level up player after defeating a monster
def level_up():
    PLAYER["level"] += 1  # Increment level
    PLAYER["max_hp"] += 10  # Increase max HP
    PLAYER["attack"] += 2   # Increase attack
    PLAYER["hp"] = PLAYER["max_hp"]  # Fully heal player
    print(f"\n*** Level {PLAYER['level']} Reached! ***")
    print(f"Max HP: {PLAYER['max_hp']} (+10)")
    print(f"Attack: {PLAYER['attack']} (+2)")
    print("HP restored!")
    time.sleep(1)

# Shop menu for purchasing items
def visit_shop():
    print("\n--- Shop ---")
    while True:
        print(f"Gold: {PLAYER['gold']}")
        for i in range(len(SHOP_ITEMS)):
            item = SHOP_ITEMS[i]
            print(f"{i + 1}. {item['name']} ({item['cost']}G) - {item['desc']}")  # Show shop items
        print("0. Leave")

        choice = input("Buy what? ")
        if choice == "0":
            print("Goodbye!")
            time.sleep(0.5)
            break
        if choice.isdigit():
            choice_index = int(choice) - 1  # Convert to 0-based index
            if 0 <= choice_index < len(SHOP_ITEMS):
                item = SHOP_ITEMS[choice_index]
                if PLAYER["gold"] >= item["cost"]:
                    PLAYER["gold"] -= item["cost"]  # Deduct gold
                    if item["effect"] == "potion":
                        PLAYER["potions"] += 1
                        print(f"Bought {item['name']}!")
                    elif item["effect"] == "attack":
                        PLAYER["attack"] += item["value"]
                        print(f"Bought {item['name']}! Attack +{item['value']}.")
                    elif item["effect"] == "hp":
                        PLAYER["max_hp"] += item["value"]
                        PLAYER["hp"] += item["value"]
                        if PLAYER["hp"] > PLAYER["max_hp"]:
                            PLAYER["hp"] = PLAYER["max_hp"]
                        print(f"Bought {item['name']}! Max HP +{item['value']}.")
                        print(f"HP: {PLAYER['hp']}/{PLAYER['max_hp']}.")
                    elif item["effect"] == "skill_boost":
                        PLAYER["skill_boost"] = item["value"]  # Set one-time skill boost
                        print(f"Bought {item['name']}! Next skill +{item['value']} damage.")
                    time.sleep(0.5)
                else:
                    print("Not enough gold!")
                    time.sleep(0.5)
            else:
                print("Invalid choice.")  # Handles out-of-range numbers
                time.sleep(0.5)
        else:
            print("Invalid choice.")  # Handles non-digits
            time.sleep(0.5)

# Combat logic against a monster
def fight_monster():
    print("\n=== FIGHT! ===")
    if PLAYER["current_monster_index"] >= len(MONSTERS):
        print("No more monsters!")
        return True  # Game should end (all monsters defeated)

    monster = MONSTERS[PLAYER["current_monster_index"]].copy()  # Copy monster data for this fight
    print(f"{monster['name']} appears!")
    time.sleep(0.5)

    skill_uses = MAX_SKILL_USES  # Reset skill uses for this fight
    PLAYER["stamina"] = MAX_STAMINA  # Reset stamina for combat

    while PLAYER["hp"] > 0 and monster["hp"] > 0:
        # Display combat status
        print(f"\n{PLAYER['name']}: {PLAYER['hp']}/{PLAYER['max_hp']} HP, {PLAYER['potions']} Potions, {PLAYER['stamina']}/{MAX_STAMINA} Stamina")
        if PLAYER["skill_boost"] > 0:
            print(f"(Skill Boost Active: +{PLAYER['skill_boost']} to next skill)")
        print(f"{monster['name']}: {monster['hp']} HP")
        print("--- Actions ---")
        print(f"1. Attack (Cost: 2 Stamina)")
        print(f"2. Use {PLAYER['skill_name']} ({skill_uses} left, Cost: 4 Stamina)")
        print(f"3. Use Potion (Cost: 2 Stamina)")
        if PLAYER["current_monster_index"] < len(MONSTERS) - 1:  # Can't run from final boss
            print("4. Run (Cost: 2 Stamina)")
        print(f"5. Rest (Cost: 0 Stamina, Gain {STAMINA_REGEN_ON_REST} Stamina)")

        action = input("Choose action: ")
        action_taken = False  # Track if a valid action was performed

        if action == "1":  # Normal attack
            if PLAYER["stamina"] >= 2:
                PLAYER["stamina"] -= 2
                damage = PLAYER["attack"]
                if random.random() < CRIT_CHANCE:  # Check for critical hit
                    damage = int(damage * CRIT_MULTIPLIER)
                    print("Critical Hit!")
                monster["hp"] -= damage
                print(f"You deal {damage} damage!")
                action_taken = True
            else:
                print("Not enough stamina for Attack!")

        elif action == "2":  # Use class skill
            if skill_uses <= 0:
                print("No skill uses left for this fight!")
            elif PLAYER["stamina"] >= 4:
                PLAYER["stamina"] -= 4
                damage = PLAYER["attack"] + PLAYER["skill_damage"] + PLAYER["skill_boost"]
                if PLAYER["class"] == "doctor":  # Doctor's skill heals
                    PLAYER["hp"] = min(PLAYER["max_hp"], PLAYER["hp"] + 20)
                    print(f"You heal 20 HP! Now at {PLAYER['hp']}.")
                if random.random() < CRIT_CHANCE:  # Critical hit for skill
                    damage = int(damage * CRIT_MULTIPLIER)
                    print("Critical Skill Hit!")
                monster["hp"] -= damage
                print(f"{PLAYER['skill_name']} deals {damage} damage!")
                skill_uses -= 1
                PLAYER["skill_boost"] = 0  # Reset skill boost after use
                action_taken = True
            else:
                print("Not enough stamina for Skill!")

        elif action == "3":  # Use potion
            if PLAYER["potions"] > 0:
                if PLAYER["stamina"] >= 2:
                    PLAYER["stamina"] -= 2
                    PLAYER["hp"] = min(PLAYER["max_hp"], PLAYER["hp"] + POTION_HEAL_AMOUNT)
                    PLAYER["potions"] -= 1
                    print(f"Potion heals {POTION_HEAL_AMOUNT} HP! Now at {PLAYER['hp']}.")
                    action_taken = True
                else:
                    print("Not enough stamina to use a Potion!")
            else:
                print("No potions left!")

        elif action == "4" and PLAYER["current_monster_index"] < len(MONSTERS) - 1:  # Run from fight
            if PLAYER["stamina"] >= 2:
                PLAYER["stamina"] -= 2
                print("You manage to escape!")
                time.sleep(0.5)
                return False  # Escaped, fight not won
            else:
                print("Not enough stamina to Run!")

        elif action == "5":  # Rest to regain stamina
            stamina_before_rest = PLAYER["stamina"]
            PLAYER["stamina"] = min(MAX_STAMINA, PLAYER["stamina"] + STAMINA_REGEN_ON_REST)
            gained_stamina = PLAYER["stamina"] - stamina_before_rest
            if gained_stamina > 0:
                print(f"You rest and regain {gained_stamina} stamina. Stamina: {PLAYER['stamina']}/{MAX_STAMINA}")
            else:
                print(f"You try to rest, but your stamina is already full. Stamina: {PLAYER['stamina']}/{MAX_STAMINA}")
            action_taken = True

        else:
            print("Invalid choice or action unavailable.")
            time.sleep(0.5)
            continue  # Skip monster turn on invalid input

        time.sleep(0.5)

        if not action_taken and PLAYER["hp"] > 0 and monster["hp"] > 0:  # Failed action due to stamina
            print("Monster waits as you ponder...")
            time.sleep(0.5)
            continue

        if monster["hp"] <= 0:  # Monster defeated
            print(f"\n{monster['name']} defeated!")
            PLAYER["gold"] += monster["gold"]
            print(f"Gained {monster['gold']} Gold!")
            PLAYER["current_monster_index"] += 1
            level_up()
            return True

        if action_taken:  # Monster attacks after valid player action
            monster_damage = monster["attack"]
            if random.random() < CRIT_CHANCE:  # Monster critical hit
                monster_damage = int(monster_damage * CRIT_MULTIPLIER)
                print(f"\n{monster['name']} lands a CRITICAL HIT!")
            PLAYER["hp"] -= monster_damage
            print(f"{monster['name']} attacks and deals {monster_damage} damage to you!")

            if "regen" in monster and monster["hp"] > 0:  # Monster regeneration
                original_monster_max_hp = MONSTERS[PLAYER["current_monster_index"]]["hp"]
                monster["hp"] = min(monster["hp"] + monster["regen"], original_monster_max_hp)
                print(f"{monster['name']} regenerates {monster['regen']} HP! Now at {monster['hp']}.")

        time.sleep(0.5)

        if PLAYER["hp"] <= 0:  # Player defeated
            print("\nYou have been defeated...")
            print("GAME OVER")
            time.sleep(1)
            return False

    return False  # Fallback, should be caught by HP checks

# Main game loop to handle menu and game progression
def main():
    create_character()  # Initialize player character
    while True:
        if PLAYER["hp"] <= 0:  # Check for game over
            break
        if PLAYER["current_monster_index"] >= len(MONSTERS):  # Victory condition
            print("\n*********************")
            print("*** YOU WIN!    ***")
            print("*********************")
            print("All monsters have been defeated!")
            print(f"Final Gold: {PLAYER['gold']}, Potions: {PLAYER['potions']}")
            show_stats()
            break

        # Display town menu
        next_monster_name = MONSTERS[PLAYER["current_monster_index"]]["name"]
        print(f"\n=== Town Menu (Level {PLAYER['level']}) ===")
        print(f"HP: {PLAYER['hp']}/{PLAYER['max_hp']} | Gold: {PLAYER['gold']} | Stamina: {PLAYER['stamina']}/{MAX_STAMINA}")
        print(f"Next Monster: {next_monster_name}")
        if PLAYER["skill_boost"] > 0:
            print(f"(Shop Skill Boost Active: +{PLAYER['skill_boost']} to next skill)")
        print("-------------------------")
        print("1. Fight Next Monster")
        print("2. Visit Shop")
        print("3. View Your Stats")
        print("4. Quit Game")

        choice = input("Choose an action: ")

        if choice == "1":
            fight_monster()  # Start combat
        elif choice == "2":
            visit_shop()  # Enter shop
        elif choice == "3":
            show_stats()  # Show player stats
        elif choice == "4":
            print("Thanks for playing Hell Trial!")
            break
        else:
            print("Invalid choice. Try again.")
            time.sleep(0.5)

if __name__ == "__main__":
    main()  # Start the game
