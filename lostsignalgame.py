import time
import random
import sys
import select

# ============================================================
#                   UTILITY FUNCTIONS
# ============================================================

def slow_print(text, delay=0.02):
    """Prints dialog with a typewriter effect."""
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()

def input_with_timeout(prompt, timeout=8):
    slow_print(prompt)
    sys.stdout.flush()
    ready, _, _ = select.select([sys.stdin], [], [], timeout)

    if ready:
        return sys.stdin.readline().strip().lower()
    else:
        return None  # timed out
# ============================================================
#                   GLOBAL GAME STATE
# ============================================================

inventory = {}   # {item_name: {"desc": "...", "type": "weapon/lore/buff", "uses": int}}
badge_buff = False
basement_unlocked = False
clone_defeated = False



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
        "Bartender: \"First time in the Drift? (yes/no)\"",
        "Bartender: \"You get your bearings yet? Know your way around? (yes/no)\"",
        "Bartender: \"You lookin’ for something? Or someone? (yes/no)\""

    ]

    for q in questions:
        ans = input(q).strip().lower()
        while ans not in ["yes", "no"]:
            ans = input("Answer yes or no: ").strip().lower()
        player_answers.append(ans)

    if player_answers == correct_sequence:

        slow_print("\nThe bartender studies you for a moment, his expression softening.\n")
        slow_print("Bartender: \"Yeah... figures. Folks who wander in lookin’ like you—")
        slow_print("—new place, no bearings, chasin’ something they can’t quite name.\"")

        slow_print("\nHe reaches under the counter, rummaging through an old crate.")
        slow_print("Bartender: \"See all kinds come through the Drift. ")
        slow_print("People runnin’, people searchin’, people forgettin’.\"")

        slow_print("\nHe pulls out nothing, but his hand pauses like he remembers something.")
        slow_print("Bartender: \"Got somethin' downstairs you might wanna check out.\"")
        slow_print("Bartender: \"Some traveler left it behind awhile back. Said it belonged to")
        slow_print("someone who might come lookin’. Never knew what they meant.\"")

        slow_print("\nHe jerks his chin toward the hallway.")
        slow_print("Bartender: \"Basement door’s unlocked. Shelf on the right. ")
        slow_print("Take a look. Might help you find whatever it is you’re after.\"")

        basement_unlocked = True

        choice = input("\nGo to the basement now? (yes/no): ").strip().lower()
        if choice == "yes":
            basement_scene()
    else:
        slow_print("\nThe bartender shrugs, losing interest.")
        slow_print("Bartender: 'Alright then. Forget I asked.'")
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

        defend = False

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

            if defend:
                reduced = max(1, dmg // 2)
                slow_print(f"\nClone attacks, but you brace! Damage reduced from {dmg} to {reduced}.")
                player_hp -= reduced
            else:
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
    
        slow_print("\nHis voice distorts mid-sentence. A glitch runs down his neck.")
        slow_print("You watch in horror as his skin flickers like a damaged hologram.\n")

        slow_print("The human mask tears away — revealing metal beneath.")
        slow_print("Synthetic tendons. Wires. A steel jaw shaped exactly like yours.")
        slow_print("The clone wasn't human. It was wearing you.\n")

        slow_print("Panels split open across his chest, exposing a glowing pulse core.")
        slow_print("It sputters… flickers… then fires off a sharp electronic burst.\n")

        slow_print("ALERT PING: **TERMINATION SIGNAL SENT**")
        slow_print("Someone — somewhere — now knows this clone has been destroyed.\n")

        slow_print("You stumble back, trying to steady your breathing.")
        slow_print("Who built these things? And why do they look like you?\n")

        global clone_defeated
        clone_defeated = True

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
#                   RAID EVENT
# ============================================================

def raid_event():
    slow_print("\nYou climb out of the basement, breathing hard, metal dust still clinging to your hands.")
    slow_print("The tavern feels strangely normal. Music hums. Glasses clink. Conversations resume.")
    slow_print("For a moment, it almost feels like nothing happened.\n")

    slow_print("A group of off-duty corporate soldiers sit at a corner table, helmets off, half-drunk.")
    slow_print("One of them laughs at a joke you’ll never hear.\n")

    slow_print("Then—\n")

    slow_print("**BZZT. BZZT.**")

    slow_print("Their comm units crackle to life, all at once.")
    slow_print("The soldiers freeze mid-sip.\n")

    slow_print("\"—ALERT: TERMINATION SIGNAL RECEIVED.\"")
    slow_print("\"—SOURCE IDENTIFIED WITHIN TAVERN PERIMETER.\"")
    slow_print("\"—PROBABLE CARRIER PRESENT. SECURE IMMEDIATELY.\"\n")

    slow_print("The soldiers exchange wide-eyed glances.")
    slow_print("One of them whispers, \"No way… Here?\"")
    slow_print("Another: \"If a construct was destroyed that close… the carrier must be nearby.\"\n")

    slow_print("Their eyes begin to sweep the tavern… and slowly narrow toward you.")

    slow_print("\nChaos erupts instantly.")
    slow_print("The soldiers leap to their feet, drawing weapons. Patrons scream and overturn tables.")
    slow_print("The alarms are blaring from the soldiers gear.\n")

    slow_print("You don’t know what ‘carrier’ means. You don’t know why they’re here.")
    slow_print("But you DO know one thing:\n")

    slow_print("**They’re coming for you.**\n")

    # --- First timed choice ---
    choice1 = input_with_timeout(
        "CHOICE (8s): Hide, Run, or Blend In? (hide/run/blend)\n"
    )

    if choice1 is None:
        return got_caught("You freeze as a soldier points directly at you.")

    if choice1 == "hide":
        return raid_hide_route()
    elif choice1 == "run":
        return raid_run_route()
    elif choice1 == "blend":
        return raid_blend_route()
    else:
        return got_caught("You hesitate, and a soldier locks onto your position.")


# ---------------------- ROUTE: HIDE ---------------------------

def raid_hide_route():
    slow_print("\nYou dive behind the bar counter as bullets crack overhead.")
    slow_print("The bartender is already curled up under the shelf, trembling.\n")

    slow_print("Soldier: \"Scan for heat signatures! The carrier is WOUNDED!\"\n")

    choice = input_with_timeout(
        "CHOICE (8s): Stay hidden or crawl to the storage room? (stay/crawl)\n"
    )

    if choice is None:
        return got_caught("A thermal scanner sweeps the bar. You're found immediately.")

    if choice == "stay":
        return got_caught("A soldier vaults over the bar and spots you instantly.")
    elif choice == "crawl":
        slow_print("\nYou crawl through shattered bottles and spilled liquor.")
        slow_print("A laser sweeps inches above your back as you slip into the storage room.\n")
        return escape_vent()
    else:
        return got_caught("You hesitate and expose yourself to a patrol.")


# ---------------------- ROUTE: RUN ---------------------------

def raid_run_route():
    slow_print("\nYou bolt across the tavern floor—")
    slow_print("A spotlight immediately snaps to your position.\n")

    slow_print("Soldier: \"TARGET IDENTIFIED! DO NOT LET THEM ESCAPE!\"\n")

    choice = input_with_timeout(
        "CHOICE (8s): Dive behind tables or sprint to the back exit? (dive/sprint)\n"
    )

    if choice is None:
        return got_caught("You trip as gunfire erupts behind you.")

    if choice == "dive":
        slow_print("\nYou slide behind a row of overturned tables.")
        slow_print("Gunfire rips into the wooden frames but misses you narrowly.\n")
        return escape_kitchen()
    elif choice == "sprint":
        return got_caught("A stun round slams into your ribs mid-sprint.")
    else:
        return got_caught("You hesitate for half a second—too long.")


# ---------------------- ROUTE: BLEND ---------------------------

def raid_blend_route():
    slow_print("\nYou shove yourself into a crowd of fleeing mercenaries.")
    slow_print("Smoke fills the room as the sprinkler system activates.\n")

    slow_print("Soldier: \"Filter the crowd! The anomaly's signal is degrading!\"\n")

    choice = input_with_timeout(
        "CHOICE (8s): Move with the crowd or break off toward the vents? (crowd/vents)\n"
    )

    if choice is None:
        return got_caught("A soldier grabs your shoulder out of suspicion.")

    if choice == "crowd":
        return got_caught("A scanner picks up your heartbeat pattern. You're pulled from the crowd.")
    elif choice == "vents":
        slow_print("\nYou slip away as soldiers focus on the larger group.")
        slow_print("A maintenance vent hangs open, steam billowing out.\n")
        return escape_vent()
    else:
        return got_caught("Your hesitation draws attention.")


# ---------------------- ESCAPE: VENTS ---------------------------

def escape_vent():
    slow_print("\nYou climb into the vent, pulling the grate shut behind you.")
    slow_print("The metal tunnels vibrate as soldiers pound through the tavern.\n")

    slow_print("A distorted voice echoes faintly through the ducts:")
    slow_print("\"The carrier is close. Their signal is unstable. Move units downstairs.\"\n")

    slow_print("You crawl toward a faint blue glow ahead...")
    demo_end()


# ---------------------- ESCAPE: KITCHEN ---------------------------

def escape_kitchen():
    slow_print("\nYou dart through the swinging kitchen doors.")
    slow_print("Steam, broken dishes, and shouting cooks blur around you.\n")

    slow_print("A back service hatch stands slightly ajar.\n")

    choice = input_with_timeout(
        "CHOICE (8s): Open the hatch quietly or kick it open? (quiet/kick)\n"
    )

    if choice is None:
        return got_caught("A patrol enters the kitchen as you freeze in place.")

    if choice == "quiet":
        slow_print("\nYou slip through the hatch silently, disappearing into the alley beyond.\n")
        demo_end()
    elif choice == "kick":
        return got_caught("The loud crash alerts the soldiers immediately.")
    else:
        return got_caught("That moment of uncertainty seals your fate.")


# ---------------------- FAILURE STATE ---------------------------

def got_caught(reason):
    slow_print(f"\n{reason}")
    slow_print("A stun baton cracks against your skull as everything goes dark...")
    slow_print("\n*** DEMO OVER: YOU WERE CAPTURED ***\n")
    main_menu()

# ---------------------- DEMO END ---------------------------
def demo_end():
    slow_print("\nYou stumble into the cold neon-lit alley behind the tavern.")
    slow_print("Sirens echo in the distance as corporate drones swarm overhead.\n")

    slow_print("You clutch your chest, catching your breath.")
    slow_print("Whatever that clone was… whatever the capsule is…")
    slow_print("One thing is certain now:\n")

    slow_print("**Someone built those constructs. And they’re still looking for you.**\n")

    slow_print("*** DEMO COMPLETE — THANK YOU FOR PLAYING ***\n")
    main_menu()

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
    global clone_defeated

    if clone_defeated:
        raid_event()
        clone_defeated = False
        return

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
