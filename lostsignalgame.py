import time
import random

# ============================================================
#                   UTILITY FUNCTIONS
# ============================================================

def slow_print(text, delay=0.02):
    """Prints dialog with a typewriter effect."""
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()


# ============================================================
#                   GLOBAL GAME STATE
# ============================================================

inventory = {}   # {item_name: {"desc": "...", "type": "weapon/lore/buff", "uses": int}}
badge_buff = False
basement_unlocked = False


# ============================================================
#                   MAIN MENU
# ============================================================

def main_menu():
    while True:
        slow_print("\n" + "="*55)
        slow_print("       LOST SIGNAL — MAIN MENU")
        slow_print("="*55)
        print("1. Start Game")
        print("2. View Inventory")
        print("3. Quit")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            intro()
        elif choice == "2":
            open_inventory()
        elif choice == "3":
            slow_print("\nExiting game... Signal terminated.")
            exit()
        else:
            slow_print("Invalid choice. Try again.")


# ============================================================
#                   INTRO SCENE
# ============================================================

def intro():
    slow_print("\nLost Signal - Demo Version\n")
    slow_print("...Memory rebooting...\n")

    slow_print(
        "You remember flashes of metal scraping, alarms drowning in static,\n"
        "and silhouettes dragging something from your hands — a black capsule.\n"
        "It's heavy... important... and dangerous.\n"
    )

    slow_print(
        "When you woke, the world was already gone.\n"
        "Unbeknownst to you, your copies scattered across this wasteland.\n"
        "Some run. Some fight. Most warn you to stay away.\n"
    )

    slow_print(
        "You've been wandering ever since. No map. No signal.\n"
        "Only a feeling that something — or someone — is closing in.\n"
    )

    slow_print(
        "Your steps lead you to the Central Drift;\n"
        "a floating tavern wedged between corporate sectors and lawless space.\n"
    )

    input("Press Enter to enter the tavern...")
    tavern_loop()



# ============================================================
#                   INVENTORY SYSTEM
# ============================================================

def add_to_inventory(name, desc, item_type, uses=1):
    inventory[name] = {"desc": desc, "type": item_type, "uses": uses}
    slow_print(f"You pick up **{name}**.")


def open_inventory():
    slow_print("\n===== INVENTORY =====")

    if not inventory:
        slow_print("You have no items.")
        return

    for item in inventory:
        print(f"- {item} ({inventory[item]['type']})")

    while True:
        choice = input("\nType an item name to inspect or 'exit': ").strip().lower()

        if choice == "exit":
            return

        if choice in inventory:
            show_item_details(choice)
        else:
            slow_print("Item not found.")


def show_item_details(item):
    info = inventory[item]
    slow_print(f"\n--- {item.upper()} ---")
    slow_print(info["desc"])

    if info["type"] in ["weapon", "buff"]:
        slow_print(f"Uses left: {info['uses']}")

    choice = input("\nDiscard this item? (yes/no): ").strip().lower()
    if choice == "yes":
        del inventory[item]
        slow_print(f"{item} discarded.")


# ============================================================
#                   EXPLORE TAVERN
# ============================================================

def explore_tavern():
    slow_print("\nYou wander deeper into the tavern...")

    discoveries = [
        ("discarded knife", 
         "A small blade. Rusted, but sharp. Could cause bleeding.",
         "weapon", 
         999),  # reusable

        ("broken bottle", 
         "Shattered at the end. Fragile, but could stun in a fight.",
         "weapon", 
         1),    # one-time use

        ("starfighter badge",
         "A polished emblem from a long-lost squadron. Wearing it makes you feel steadier.",
         "buff",
         999),  # permanent buff

        ("cracked holo-chip",
         "Displays corrupted coordinates and static faces you don't recognize.",
         "lore",
         0),

         ("medkit",
          "A compact emergency medkit filled with synthfoam patches. Restores health in combat.",
          "heal",
         1),

        ("torn manifest page",
         "A manifest log with smeared names. One name isn't smeared: yours.",
         "lore",
         0),
    ]

    for name, desc, item_type, uses in discoveries:
        slow_print(f"\nYou find {name}.")
        slow_print(desc)
        take = input("Take it? (yes/no): ").strip().lower()

        if take == "yes":
            add_to_inventory(name, desc, item_type, uses)

    input("\nPress Enter to return to the tavern...")


# ============================================================
#                   BARTENDER PUZZLE
# ============================================================

def talk_to_bartender():
    global basement_unlocked
    slow_print("\nYou approach the bartender. He doesn't look up from his glass.\n")
    slow_print("Bartender: \"Yeah? You need somethin'?\"")

    correct_sequence = ["yes", "no", "yes"]
    player_answers = []

    questions = [
        "Bartender: \"You new 'round here? (yes/no)\" ",
        "Bartender: \"You runnin' from someone? (yes/no)\" ",
        "Bartender: \"Wanna hear today's special? (yes/no)\" "
    ]

    for q in questions:
        ans = input(q).strip().lower()
        while ans not in ["yes", "no"]:
            ans = input("Answer yes or no: ").strip().lower()
        player_answers.append(ans)

    if player_answers == correct_sequence:
        slow_print("\nBartender freezes mid-polish.\n")
        slow_print("Bartender: \"...Thought so. People like you don't wander without purpose.\"")
        slow_print("Bartender: \"If you're lookin' for answers... there's a door downstairs.\"")
        slow_print("Bartender: \"Wasn't me who told you. Understand?\"")

        basement_unlocked = True

        choice = input("\nEnter the basement now? (yes/no): ").strip().lower()
        if choice == "yes":
            basement_scene()

    else:
        slow_print("\nBartender squints at you.")
        slow_print("Bartender: \"Mm. Try again when you ain't actin' suspicious.\"")
        slow_print("He turns away.")
        return


# ============================================================
#                   BASEMENT + CLONE ENCOUNTER
# ============================================================

def basement_scene():
    slow_print("\nYou descend the metal stairs into a dim, humming basement...")
    slow_print("Pipes drip. Something moves in the darkness.\n")

    slow_print("A figure steps forward — your face, your posture... but not your eyes.")
    slow_print("Clone: \"...You're awake. That complicates everything.\"")

    slow_print("\nHis tone is cold, analytical — yet something cracks beneath it.")
    slow_print("Clone: \"I was told the original wouldn't survive the breach.\"")
    slow_print("Clone: \"But here you are. Alive. And that means I have to finish this.\"")

    input("\nPress Enter as the clone steps closer...")

    combat_system()


# ============================================================
#                   COMBAT SYSTEM
# ============================================================

def combat_system():
    global badge_buff

    player_hp = 25
    clone_hp = 22
    bleed_turns = 0
    stun_next_turn = False

    # Badge passive buff?
    if "starfighter badge" in inventory:
        badge_buff = True

    slow_print("\n===== COMBAT START =====\n")

    while player_hp > 0 and clone_hp > 0:

        # --- Show HP ---
        slow_print(f"Your HP: {player_hp}   |   Clone HP: {clone_hp}")

        # --- Player's Turn ---
        print("\nYour options:")
        print("1. Attack")
        print("2. Use Item")
        print("3. Defend")

        choice = input("Choose: ").strip()

        # ------------------ ATTACK ------------------
        if choice == "1":
            base = 4
            if badge_buff:
                base += 2

            slow_print(f"You strike the clone! ({base} dmg)")
            clone_hp -= base

        # ------------------ USE ITEM ------------------
        elif choice == "2":
            used = use_item_combat()

            if used == "knife":
                slow_print("The blade cuts deep — the clone begins bleeding!")
                bleed_turns = 2

            elif used == "bottle":
                slow_print("The bottle shatters! The clone is stunned!")
                stun_next_turn = True

            elif used == "heal":
                player_hp += 8
                if player_hp > 25:
                    player_hp = 25
                slow_print("You feel your strength returning!")


        # ------------------ DEFEND ------------------
        elif choice == "3":
            slow_print("You brace yourself. Incoming damage reduced.")
            defend = True
        else:
            slow_print("Invalid input. You lose your turn.")
            defend = False

        # ------------------ BLEED DAMAGE ------------------
        if bleed_turns > 0:
            slow_print("Clone bleeds... (-2 HP)")
            clone_hp -= 2
            bleed_turns -= 1

        if clone_hp <= 0:
            break

        # ------------------ CLONE TURN ------------------
        if stun_next_turn:
            slow_print("\nClone is stunned and cannot act!")
            stun_next_turn = False
        else:
            dmg = random.randint(3, 5)
            slow_print(f"\nClone attacks! ({dmg} dmg)")
            player_hp -= dmg

    # ============================================================
    #                   COMBAT RESULT
    # ============================================================

    if player_hp <= 0:
        slow_print("\nYou collapse... vision fading.")
        slow_print("Clone: \"Another failure...\"")
        slow_print("\nYou awaken back in the tavern.\n")
        return_tavern()
        return

    if clone_hp <= 0:
        slow_print("\nClone staggers, dropping to one knee.")
        slow_print("Clone: \"If you're alive... the others will come for you.\"")
        slow_print("Clone: \"Don't trust the capsule... it's not what you think.\"")
        slow_print("The clone collapses.\n")

    # --- Post-Fight Reflection ---
        slow_print("You stand over him, chest heaving. He looks so much like you that "
                   "your stomach twists.\n")
        slow_print("For a moment, you're not sure which one of you was meant to survive.")
        slow_print("Your hands tremble—not from fear, but from recognition.\n")

        slow_print("If he was created to replace you... then what does that make you?")
        slow_print("A prototype? A mistake? The real one?")
        slow_print("None of it fits together.\n")

        slow_print("His final words echo in your skull:")
        slow_print("\"The others will come.\"")
        slow_print("\"Don't trust the capsule.\"")

        slow_print("\nYou wipe the blood from your face, steadying your breath.")
        slow_print("Whoever sent them… they're still out there.")
        slow_print("And they’re the ones who know who... or what you really are.\n")


        return_tavern()



# ============================================================
#                   COMBAT ITEM HANDLER
# ============================================================

def use_item_combat():
    if not inventory:
        slow_print("You have no usable combat items.")
        return None

    slow_print("\nItems available:")
    for item in inventory:
        if inventory[item]["type"] in ["weapon", "buff", "heal"]:
            print(f"- {item}")

    choice = input("Use which item? ").strip().lower()

    if choice not in inventory:
        slow_print("Invalid choice.")
        return None

    item = inventory[choice]

    if item["type"] == "weapon":

        if choice == "discarded knife":
            return "knife"

        if choice == "broken bottle":
            if item["uses"] > 0:
                item["uses"] -= 1
                if item["uses"] == 0:
                    del inventory[choice]
                return "bottle"

    if item["type"] == "buff":
        slow_print("You grip the badge. Confidence rises.")
        return None
    
    if item["type"] == "heal":
        slow_print("You quickly apply the medkit! (+8 HP)")
        item["uses"] -= 1
        if item["uses"] == 0:
            del inventory[choice]
        return "heal"


    slow_print("Item cannot be used in combat.")
    return None


# ============================================================
#                   RETURN TO TAVERN
# ============================================================

def return_tavern():
    input("Press Enter to return to the tavern...")
    tavern_loop()


# ============================================================
#                   MERC DIALOGUE
# ============================================================

def talk_to_merc():
    slow_print("\nA merc leans against a rusted pillar, armor scraped and mismatched.")
    slow_print("Merc: \"You lookin' for trouble, or just lost?\"")
    slow_print("Merc: \"Word of advice: keep 'yer head low.\"")
    input("Press Enter to return to the tavern...")


# ============================================================
#                   TAVERN MAIN LOOP
# ============================================================

def tavern_loop():
    global basement_unlocked

    while True:
        slow_print("\n===== CENTRAL DRIFT TAVERN =====")
        print("1. Talk to Bartender")
        print("2. Talk to Merc")
        print("3. Explore Tavern")
        print("4. Check Inventory")
        print("5. Exit Tavern")

        choice = input("\nChoose: ").strip()

        if choice == "1":
            talk_to_bartender()
        elif choice == "2":
            talk_to_merc()
        elif choice == "3":
            explore_tavern()
        elif choice == "4":
            open_inventory()
        elif choice == "5":
            slow_print("You leave the tavern and step into the desolate wasteland...")
            main_menu()
            return
        else:
            slow_print("Invalid choice.")


# ============================================================
#                   RUN GAME
# ============================================================

main_menu()
