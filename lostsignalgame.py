import time

def slow_print(text, delay=0.02):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()  # new line after printing


# ------- INTRO SCENE ------- #
def intro():
    slow_print("Lost Signal - Demo Version\n")
    slow_print("...Memory rebooting...\n")
    slow_print(
        "You remember flashes of metal scraping, alarms droning in static,\n"
        "and silhouettes dragging something from your hands... a black capsule.\n"
        "It's heavy.. important... and dangerous.\n"
    )

    slow_print(
        "When you woke, the world was already gone.\n"
        "Unbeknownst to you, your copies have already scattered across this wasteland.\n"
        "Some run, some fight... most warn you to stay away.\n"
    )

    slow_print(
        "You've been wandering aimlessly ever since. No map. No signal.\n"
        "Only the feeling that something... or someone is after you.\n"
    )

    slow_print(
        "Your steps eventually lead you to the Central Drift;\n"
        "a floating tavern wedged between corporate sectors and lawless space.\n"
        "A place where mercs, rebels, and rogues drink under the same neon haze.\n"
    )

    input("Press Enter to enter the tavern...")

    # ----- Bartender Interaction Scene ----- #
    def talk_to_bartender():
        slow_print("\nYou step up to the bar. The bartender cleans a glass without looking up.\n")
        slow_print("Bartender: \"Yeah? You need somethin'?\"")

        # correct sequence is yes no yes 
        correct_sequence = ["yes", "no", "yes"]
        player_responses = []

        questions = [
            "Bartender: \"You new 'round here? (yes/no)\" ",
            "Bartender: \"You runnin' from someone? (yes/no)\" ",
            "Bartender: \"Would you like to hear about the daily special? (yes/no)\" "
        ]

        for q in questions:
            answer = input(q).strip().lower()
            while answer not in ["yes", "no"]:
                answer = input("Please answer 'yes' or 'no': ").strip().lower()
            player_responses.append(answer)

        if player_responses == correct_sequence:
            slow_print("\nBartender: \"Thought so. People like you don't just wander in.\"\n")
            slow_print("Listen real close—whatever you're doing here, make sure you don't get caught.\n")
            slow_print("To be continued...\n")
        else:
            slow_print("\nThe bartender squints at you, unimpressed.")
            slow_print("Get lost. Maybe next time you'll be more convincing.\n")
            slow_print("Game Over.\n")

        input("Press Enter to return to the tavern...")

    #----- Merc Interaction Scene ----- #
    def talk_to_merc():
        slow_print("\nYou approach the merc leaning against the rusted pillar, his figure illuminated by the flickering neon lights.")
        slow_print("His armor is mismatched corporate gear, rebel straps, and scavenged parts, all held together with duct tape and determination.")
        slow_print("Merc: \"You lookin' for trouble, or just lost?\"")

        slow_print("Player: \"Just passing through. Heard this place is safe enough.\"")
        slow_print("Merc: \"A word of advice, stranger. Keep 'yer head low for yer own good.\"")

        slow_print("\nHe gives you a nod. Not friendly. Not hostile. Just... warning you.")
        input("Press Enter to return to the tavern...")

    # ---- Explore Tavern Scene ---- #
    
    def explore_tavern():
        slow_print("\nYou step away from the noise of the bar and wander deeper into the tavern...")

        inventory = []

        discoveries = [
            ("a cracked holo-chip", 
             "Its screen flickers with corrupted coordinates. Someone tried to wipe it, but not well enough."),
            ("an old starfighter badge", 
             "The emblem is from a squadron that was supposedly wiped out decades ago."),
            ("a data key wrapped in cloth", 
             "It’s warm to the touch—almost like it’s been used recently."),
            ("a torn page from a manifest log", 
             "The names are smudged, except one: yours.")
        ]

        for item, description in discoveries:
            slow_print(f"\nYou find {item}.")
            slow_print(description)

            choice = input(f"Do you take the {item}? (yes/no): ").strip().lower()
            while choice not in ["yes", "no"]:
                choice = input("Please answer 'yes' or 'no': ").strip().lower()

            if choice == "yes":
                inventory.append(item)
                slow_print(f"You place {item} into your pocket.")
            else:
                slow_print(f"You leave {item} where you found it.")

        slow_print("\nYou've explored everything you can for now.")
        
        if inventory:
            slow_print("Items collected:")
            for item in inventory:
                slow_print(f" - {item}")
        else:
            slow_print("You leave the tavern floor empty-handed.")

        input("\nPress Enter to return to the tavern...")


    # ----- Tavern Main Loop ----- #
    def tavern_loop():
        while True:
            slow_print("\nYou are in the Central Drift Tavern. What would you like to do?")
            slow_print("1. Talk to the Bartender")
            slow_print("2. Talk to the Merc")
            slow_print("3. Explore the Tavern")
            slow_print("4. Exit Tavern")

            choice = input("Enter the number of your choice: ").strip()

            if choice == "1":
                talk_to_bartender()
            elif choice == "2":
                talk_to_merc()
            elif choice == "3":
                explore_tavern()
            elif choice == "4":
                slow_print("\nYou exit the tavern, stepping back into the desolate world outside.\n")
                break
            else:
                slow_print("Invalid choice. Please try again.")

    # run tavern loop after intro dialogue
    tavern_loop()


# Run game
intro()
