#!/usr/bin/env python3

import os
import sys
import time
import random
from typing import Dict, List, Tuple, Optional

class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'

class GameState:
    def __init__(self):
        self.player_name = ""
        self.health = 100
        self.magic = 50
        self.inventory = []
        self.visited_locations = set()
        self.story_flags = {}
        self.ending_path = []

class AdventureGame:
    def __init__(self):
        self.state = GameState()
        self.terminal_width = self.get_terminal_width()
        self.terminal_height = self.get_terminal_height()
        
    def get_terminal_width(self) -> int:
        try:
            return os.get_terminal_size().columns
        except:
            return 80
    
    def get_terminal_height(self) -> int:
        try:
            return os.get_terminal_size().lines
        except:
            return 24

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_centered(self, text: str, color: str = Colors.WHITE):
        lines = text.split('\n')
        for line in lines:
            padding = (self.terminal_width - len(line)) // 2
            print(f"{color}{' ' * padding}{line}{Colors.RESET}")

    def print_boxed(self, text: str, color: str = Colors.WHITE, bg_color: str = ""):
        lines = text.split('\n')
        max_length = max(len(line) for line in lines)
        box_width = min(max_length + 4, self.terminal_width - 4)
        
        border = "╔" + "═" * (box_width - 2) + "╗"
        self.print_centered(f"{color}{bg_color}{border}{Colors.RESET}")
        
        for line in lines:
            content = line.ljust(box_width - 4)
            boxed_line = f"║ {content} ║"
            self.print_centered(f"{color}{bg_color}{boxed_line}{Colors.RESET}")
        
        border = "╚" + "═" * (box_width - 2) + "╝"
        self.print_centered(f"{color}{bg_color}{border}{Colors.RESET}")

    def animated_print(self, text: str, delay: float = 0.03, color: str = Colors.WHITE):
        for char in text:
            print(f"{color}{char}{Colors.RESET}", end='', flush=True)
            time.sleep(delay)
        print()

    def print_status_bar(self):
        health_bar = "█" * (self.state.health // 5) + "░" * (20 - self.state.health // 5)
        magic_bar = "█" * (self.state.magic // 5) + "░" * (10 - self.state.magic // 5)
        
        status = f"❤️  {Colors.RED}{health_bar}{Colors.RESET} {self.state.health}/100  " \
                f"✨ {Colors.BLUE}{magic_bar}{Colors.RESET} {self.state.magic}/50"
        
        if self.state.inventory:
            items = ", ".join(self.state.inventory)
            status += f"  🎒 {Colors.YELLOW}{items}{Colors.RESET}"
        
        self.print_centered("═" * min(80, self.terminal_width))
        self.print_centered(status)
        self.print_centered("═" * min(80, self.terminal_width))

    def wait_for_input(self, prompt: str = "Press Enter to continue..."):
        self.print_centered(f"{Colors.DIM}{prompt}{Colors.RESET}")
        input()

    def get_choice(self, choices: List[str]) -> int:
        while True:
            print()
            for i, choice in enumerate(choices, 1):
                choice_text = f"{Colors.CYAN}[{i}]{Colors.RESET} {choice}"
                self.print_centered(choice_text)
            
            print()
            try:
                choice_input = input(f"{Colors.YELLOW}Enter your choice (1-{len(choices)}): {Colors.RESET}")
                choice_num = int(choice_input)
                if 1 <= choice_num <= len(choices):
                    return choice_num - 1
                else:
                    self.print_centered(f"{Colors.RED}Invalid choice. Please enter a number between 1 and {len(choices)}.{Colors.RESET}")
            except ValueError:
                self.print_centered(f"{Colors.RED}Please enter a valid number.{Colors.RESET}")

    def show_title_screen(self):
        self.clear_screen()
        
        title_art = """
    ╔══════════════════════════════════════════╗
    ║        🌲 MYSTICAL FOREST QUEST 🌲        ║
    ║                                          ║
    ║      An Interactive Adventure Game       ║
    ╚══════════════════════════════════════════╝
        """
        
        self.print_centered(title_art, Colors.GREEN + Colors.BOLD)
        print()
        
        intro_text = """Welcome, brave adventurer, to the Mystical Forest!
Your choices will determine your fate in this enchanted realm.
Will you become a legendary hero, or fall to the darkness within?

The forest awaits your decision..."""
        
        self.animated_print(intro_text, 0.05, Colors.CYAN)
        print()
        self.wait_for_input()

    def get_player_name(self):
        self.clear_screen()
        self.print_boxed("CHARACTER CREATION", Colors.MAGENTA + Colors.BOLD)
        print()
        
        while True:
            name = input(f"{Colors.YELLOW}Enter your character's name: {Colors.RESET}").strip()
            if name:
                self.state.player_name = name
                break
            self.print_centered(f"{Colors.RED}Please enter a valid name.{Colors.RESET}")
        
        welcome_text = f"Welcome, {Colors.BOLD + Colors.GREEN}{self.state.player_name}{Colors.RESET}!"
        self.print_centered(welcome_text)
        self.wait_for_input()

    def forest_entrance(self):
        self.clear_screen()
        self.print_status_bar()
        
        if "forest_entrance" not in self.state.visited_locations:
            self.state.visited_locations.add("forest_entrance")
            
            story_text = f"""🌲 THE FOREST ENTRANCE 🌲

{self.state.player_name}, you stand before the ancient Mystical Forest.
Towering trees stretch endlessly upward, their canopy blocking most sunlight.
Strange whispers echo from within, and magical sparkles dance in the air.

Two paths diverge before you:
- A well-worn trail leading deeper into the forest
- A narrow, overgrown path that seems rarely traveled"""
            
            self.animated_print(story_text, 0.04, Colors.GREEN)
        else:
            self.animated_print("You return to the forest entrance, contemplating your next move.", 0.04, Colors.GREEN)
        
        print()
        choices = [
            "Take the well-worn trail (Safe but predictable)",
            "Follow the overgrown path (Dangerous but mysterious)",
            "Search the area for useful items",
            "Rest and recover health"
        ]
        
        choice = self.get_choice(choices)
        
        if choice == 0:
            self.state.ending_path.append("safe_path")
            return self.safe_trail()
        elif choice == 1:
            self.state.ending_path.append("dangerous_path")
            return self.dangerous_path()
        elif choice == 2:
            return self.search_entrance()
        else:
            return self.rest_at_entrance()

    def search_entrance(self):
        self.clear_screen()
        self.print_status_bar()
        
        if "searched_entrance" not in self.state.story_flags:
            self.state.story_flags["searched_entrance"] = True
            
            search_text = """🔍 SEARCHING THE ENTRANCE 🔍

You carefully examine the forest entrance...
Behind a moss-covered rock, you discover an old leather pouch!"""
            
            self.animated_print(search_text, 0.04, Colors.YELLOW)
            
            found_item = random.choice(["Healing Potion", "Magic Crystal", "Ancient Coin"])
            self.state.inventory.append(found_item)
            
            if found_item == "Healing Potion":
                self.state.health = min(100, self.state.health + 20)
            elif found_item == "Magic Crystal":
                self.state.magic = min(50, self.state.magic + 15)
            
            self.animated_print(f"You found: {Colors.BOLD + Colors.CYAN}{found_item}{Colors.RESET}!", 0.04, Colors.GREEN)
        else:
            self.animated_print("You've already searched this area thoroughly.", 0.04, Colors.DIM)
        
        self.wait_for_input()
        return self.forest_entrance()

    def rest_at_entrance(self):
        self.clear_screen()
        self.print_status_bar()
        
        rest_text = """💤 RESTING 💤

You sit down on a comfortable log and take a moment to rest.
The peaceful sounds of the forest help you recover your strength."""
        
        self.animated_print(rest_text, 0.04, Colors.BLUE)
        
        health_gain = random.randint(10, 25)
        magic_gain = random.randint(5, 15)
        
        self.state.health = min(100, self.state.health + health_gain)
        self.state.magic = min(50, self.state.magic + magic_gain)
        
        self.animated_print(f"Health restored: +{health_gain} | Magic restored: +{magic_gain}", 0.04, Colors.GREEN)
        
        self.wait_for_input()
        return self.forest_entrance()

    def safe_trail(self):
        self.clear_screen()
        self.print_status_bar()
        
        story_text = f"""🛤️  THE SAFE TRAIL 🛤️

{self.state.player_name}, you walk along the well-maintained path.
Sunlight filters through the canopy, creating beautiful patterns on the ground.
You hear the gentle sound of a stream nearby.

Ahead, you notice a small wooden bridge crossing the stream.
On the other side, you can see what appears to be an old cottage."""
        
        self.animated_print(story_text, 0.04, Colors.GREEN)
        
        print()
        choices = [
            "Cross the bridge to the cottage",
            "Follow the stream instead of crossing",
            "Turn back to the forest entrance"
        ]
        
        choice = self.get_choice(choices)
        
        if choice == 0:
            return self.old_cottage()
        elif choice == 1:
            return self.follow_stream()
        else:
            return self.forest_entrance()

    def dangerous_path(self):
        self.clear_screen()
        self.print_status_bar()
        
        story_text = f"""⚠️  THE DANGEROUS PATH ⚠️

{self.state.player_name}, you push through the thick undergrowth.
Thorns catch at your clothes, and strange shadows move between the trees.
The air grows colder, and you sense you're being watched.

Suddenly, you hear a low growling sound ahead!"""
        
        self.animated_print(story_text, 0.04, Colors.RED)
        
        print()
        choices = [
            "Investigate the source of the growling",
            "Try to sneak around quietly",
            "Use magic to create light",
            "Retreat immediately"
        ]
        
        choice = self.get_choice(choices)
        
        if choice == 0:
            return self.encounter_wolf()
        elif choice == 1:
            return self.sneak_around()
        elif choice == 2:
            return self.use_magic_light()
        else:
            return self.forest_entrance()

    def old_cottage(self):
        self.clear_screen()
        self.print_status_bar()
        
        story_text = f"""🏠 THE OLD COTTAGE 🏠

You approach the quaint cottage. Smoke rises from its chimney,
and warm light glows from the windows. The door is painted bright red,
and colorful flowers bloom in window boxes.

An elderly woman emerges, wearing a pointed hat and carrying a wooden staff."""
        
        self.animated_print(story_text, 0.04, Colors.MAGENTA)
        
        witch_dialogue = f'''"Welcome, {self.state.player_name}!" she says with a knowing smile.
"I am Sage Willow, keeper of forest wisdom. I sense great potential in you.
Would you like me to enhance your abilities, or do you prefer to continue
your journey with your current strength?"'''
        
        self.animated_print(witch_dialogue, 0.04, Colors.CYAN)
        
        print()
        choices = [
            "Ask for magical enhancement (+20 Magic, -10 Health)",
            "Request physical training (+20 Health, -10 Magic)",
            "Ask for wisdom about the forest",
            "Politely decline and continue"
        ]
        
        choice = self.get_choice(choices)
        
        if choice == 0:
            self.state.magic = min(50, self.state.magic + 20)
            self.state.health = max(10, self.state.health - 10)
            self.state.story_flags["magical_enhancement"] = True
            self.animated_print("Sage Willow enchants you with powerful magic!", 0.04, Colors.BLUE)
        elif choice == 1:
            self.state.health = min(100, self.state.health + 20)
            self.state.magic = max(5, self.state.magic - 10)
            self.state.story_flags["physical_training"] = True
            self.animated_print("Sage Willow teaches you forest survival techniques!", 0.04, Colors.RED)
        elif choice == 2:
            wisdom = "The forest holds three great treasures: the Crystal of Light in the Deep Cave, the Sword of Courage near the Ancient Oak, and the Crown of Wisdom in the Misty Peaks."
            self.animated_print(f"Sage Willow shares: '{wisdom}'", 0.04, Colors.YELLOW)
            self.state.story_flags["received_wisdom"] = True
        
        self.wait_for_input()
        return self.forest_crossroads()

    def follow_stream(self):
        self.clear_screen()
        self.print_status_bar()
        
        story_text = """🏞️  FOLLOWING THE STREAM 🏞️

You decide to follow the babbling stream deeper into the forest.
The water is crystal clear, and you can see colorful fish swimming below.
The path becomes more challenging as you navigate over rocks and fallen logs.

After walking for some time, you discover a beautiful waterfall
cascading into a pristine pool surrounded by glowing mushrooms."""
        
        self.animated_print(story_text, 0.04, Colors.CYAN)
        
        if "Healing Potion" not in self.state.inventory:
            self.animated_print("The magical pool seems to have healing properties!", 0.04, Colors.BLUE)
            self.state.health = min(100, self.state.health + 30)
            self.animated_print("Your health is fully restored by the magical waters!", 0.04, Colors.GREEN)
        
        print()
        choices = [
            "Dive into the pool to search for treasures",
            "Climb up beside the waterfall",
            "Rest by the peaceful pool",
            "Return to the safe trail"
        ]
        
        choice = self.get_choice(choices)
        
        if choice == 0:
            return self.dive_for_treasure()
        elif choice == 1:
            return self.climb_waterfall()
        elif choice == 2:
            return self.rest_by_pool()
        else:
            return self.safe_trail()

    def encounter_wolf(self):
        self.clear_screen()
        self.print_status_bar()
        
        story_text = """🐺 WOLF ENCOUNTER 🐺

You cautiously approach the source of the growling.
A massive silver wolf emerges from behind a tree, its eyes glowing amber.
But as you look closer, you notice it seems injured and afraid rather than aggressive.
There's an arrow stuck in its hind leg."""
        
        self.animated_print(story_text, 0.04, Colors.RED)
        
        print()
        choices = [
            "Try to help the injured wolf",
            "Slowly back away",
            "Use magic to calm the wolf",
            "Make loud noises to scare it away"
        ]
        
        choice = self.get_choice(choices)
        
        if choice == 0:
            return self.help_wolf()
        elif choice == 1:
            self.animated_print("You carefully back away. The wolf watches but doesn't follow.", 0.04, Colors.YELLOW)
            self.wait_for_input()
            return self.dangerous_path()
        elif choice == 2:
            if self.state.magic >= 10:
                return self.magic_calm_wolf()
            else:
                self.animated_print("You don't have enough magic energy!", 0.04, Colors.RED)
                self.wait_for_input()
                return self.encounter_wolf()
        else:
            self.animated_print("The wolf flees in terror, but you feel guilty about frightening an injured creature.", 0.04, Colors.DIM)
            self.state.story_flags["scared_wolf"] = True
            self.wait_for_input()
            return self.deep_forest()

    def help_wolf(self):
        self.clear_screen()
        self.print_status_bar()
        
        story_text = """❤️  HELPING THE WOLF ❤️

You speak in soothing tones and slowly approach the injured wolf.
It growls softly but doesn't attack. With gentle hands, you carefully
remove the arrow and tend to its wound using herbs you find nearby.

The wolf looks at you with grateful eyes and lets out a soft whine.
Suddenly, it transforms before your eyes into a tall, ethereal figure!"""
        
        self.animated_print(story_text, 0.04, Colors.GREEN)
        
        transformation_text = '''"I am the Forest Guardian," the figure speaks in a melodious voice.
"You have shown kindness to a creature in need. For this, I grant you
the ability to communicate with all forest animals."'''
        
        self.animated_print(transformation_text, 0.04, Colors.MAGENTA)
        
        self.state.story_flags["forest_guardian_friend"] = True
        self.state.inventory.append("Animal Communication")
        self.state.magic = min(50, self.state.magic + 25)
        
        self.wait_for_input()
        return self.guardian_guidance()

    def magic_calm_wolf(self):
        self.clear_screen()
        self.print_status_bar()
        
        self.state.magic -= 10
        
        story_text = """✨ MAGICAL CALMING ✨

You extend your hands and channel your magical energy toward the wolf.
A soft, blue light emanates from your palms, and the wolf immediately
relaxes. Its eyes lose their fearful gleam, and it approaches you trustingly.

You notice the arrow in its leg and realize this is the Forest Guardian
in wolf form, testing your character."""
        
        self.animated_print(story_text, 0.04, Colors.BLUE)
        
        self.state.story_flags["used_magic_on_guardian"] = True
        self.wait_for_input()
        return self.help_wolf()

    def forest_crossroads(self):
        self.clear_screen()
        self.print_status_bar()
        
        story_text = """🔀 THE FOREST CROSSROADS 🔀

You arrive at a significant crossroads where four paths diverge.
Ancient stone markers point in different directions:

🏔️  North: "Misty Peaks - Crown of Wisdom"
🌳 East: "Ancient Oak - Sword of Courage"  
🕳️  South: "Deep Cave - Crystal of Light"
🏠 West: "Return to Cottage" """
        
        self.animated_print(story_text, 0.04, Colors.WHITE)
        
        if "received_wisdom" in self.state.story_flags:
            self.animated_print("Sage Willow's wisdom guides you - these are the three treasures she mentioned!", 0.04, Colors.YELLOW)
        
        print()
        choices = [
            "Head North to Misty Peaks",
            "Go East to Ancient Oak", 
            "Travel South to Deep Cave",
            "Return West to the Cottage"
        ]
        
        choice = self.get_choice(choices)
        
        if choice == 0:
            self.state.ending_path.append("wisdom_path")
            return self.misty_peaks()
        elif choice == 1:
            self.state.ending_path.append("courage_path")
            return self.ancient_oak()
        elif choice == 2:
            self.state.ending_path.append("light_path")
            return self.deep_cave()
        else:
            return self.old_cottage()

    def misty_peaks(self):
        self.clear_screen()
        self.print_status_bar()
        
        story_text = """🏔️  MISTY PEAKS 🏔️

You climb higher into the mountains where mist swirls around ancient peaks.
The air grows thin, and each step becomes more challenging.
Through the mist, you see the silhouette of a magnificent temple
built into the mountainside.

As you approach, three robed figures emerge from the temple."""
        
        self.animated_print(story_text, 0.04, Colors.CYAN)
        
        riddle_text = '''"Welcome, seeker," they speak in unison. "To claim the Crown of Wisdom,
you must answer our riddle correctly:

'I have cities, but no houses dwell within.
I have mountains, but no trees therein.
I have water, but no fish swim free.
I have roads, but no travelers you'll see.
What am I?'"'''
        
        self.animated_print(riddle_text, 0.04, Colors.MAGENTA)
        
        print()
        choices = [
            "A map",
            "A dream", 
            "A painting",
            "A book"
        ]
        
        choice = self.get_choice(choices)
        
        if choice == 0:
            return self.correct_riddle_wisdom()
        else:
            return self.incorrect_riddle()

    def ancient_oak(self):
        self.clear_screen()
        self.print_status_bar()
        
        story_text = """🌳 THE ANCIENT OAK 🌳

You stand before a colossal oak tree, its trunk so wide that dozens of people
couldn't wrap their arms around it. The tree pulses with ancient magic,
and its roots form intricate patterns in the earth.

Embedded in the trunk is a magnificent sword, glowing with inner light.
But as you approach, the tree begins to speak!"""
        
        self.animated_print(story_text, 0.04, Colors.GREEN)
        
        tree_dialogue = '''"Young one," the oak's voice rumbles like distant thunder,
"The Sword of Courage can only be claimed by one who has shown
true bravery. Tell me of your greatest act of courage in this forest."'''
        
        self.animated_print(tree_dialogue, 0.04, Colors.YELLOW)
        
        print()
        courage_choices = []
        
        if "forest_guardian_friend" in self.state.story_flags:
            courage_choices.append("I helped an injured wolf, even when I was afraid")
        if "used_magic_on_guardian" in self.state.story_flags:
            courage_choices.append("I used my magic to calm a dangerous creature")
        if "dangerous_path" in self.state.ending_path:
            courage_choices.append("I chose the dangerous path when others might have taken the safe route")
        
        courage_choices.extend([
            "I ventured into this mystical forest alone",
            "I'm not sure I've been truly courageous yet"
        ])
        
        choice = self.get_choice(courage_choices)
        
        if choice < len(courage_choices) - 1:
            return self.claim_sword_courage()
        else:
            return self.sword_trial()

    def deep_cave(self):
        self.clear_screen()
        self.print_status_bar()
        
        story_text = """🕳️  THE DEEP CAVE 🕳️

You descend into a vast underground cave system. Stalactites hang like
frozen waterfalls from the ceiling, and phosphorescent moss provides
an eerie blue-green glow.

Deep within the cave, you discover a chamber filled with crystalline
formations. At the center sits the Crystal of Light, blazing with
pure white radiance.

But blocking your path is a massive stone golem, its eyes glowing red!"""
        
        self.animated_print(story_text, 0.04, Colors.BLUE)
        
        print()
        choices = [
            "Challenge the golem to combat",
            "Try to sneak past while it's not looking",
            "Attempt to communicate with the golem",
            "Use magic to distract it"
        ]
        
        choice = self.get_choice(choices)
        
        if choice == 0:
            return self.fight_golem()
        elif choice == 1:
            return self.sneak_past_golem()
        elif choice == 2:
            return self.communicate_golem()
        else:
            return self.magic_distract_golem()

    def determine_ending(self):
        self.clear_screen()
        
        ending_score = 0
        treasures_found = 0
        
        if "Crown of Wisdom" in self.state.inventory:
            treasures_found += 1
            ending_score += 30
        if "Sword of Courage" in self.state.inventory:
            treasures_found += 1
            ending_score += 30
        if "Crystal of Light" in self.state.inventory:
            treasures_found += 1
            ending_score += 30
        
        if "forest_guardian_friend" in self.state.story_flags:
            ending_score += 20
        if "magical_enhancement" in self.state.story_flags:
            ending_score += 10
        if "physical_training" in self.state.story_flags:
            ending_score += 10
        if "received_wisdom" in self.state.story_flags:
            ending_score += 15
        
        ending_score += self.state.health // 5
        ending_score += self.state.magic // 2
        
        if treasures_found == 3:
            return self.legendary_hero_ending()
        elif ending_score >= 80:
            return self.hero_ending()
        elif ending_score >= 50:
            return self.adventurer_ending()
        elif ending_score >= 30:
            return self.survivor_ending()
        else:
            return self.lost_soul_ending()

    def legendary_hero_ending(self):
        ending_text = f"""🏆 LEGENDARY HERO ENDING 🏆

Congratulations, {Colors.BOLD + Colors.GOLD}{self.state.player_name}{Colors.RESET}!

You have achieved the impossible - claiming all three legendary treasures
of the Mystical Forest! The Crown of Wisdom upon your head grants you
infinite knowledge, the Sword of Courage in your hand makes you fearless,
and the Crystal of Light in your possession banishes all darkness.

The forest itself bows to your greatness. Animals gather to honor you,
the trees whisper songs of your deeds, and the very earth celebrates
your triumph. You have become a legend that will be told for generations!

The Forest Guardian appears before you one final time:
"You are now the true protector of this realm. The forest and all its
creatures are under your care. Use your power wisely, great hero!"

🌟 ACHIEVEMENT UNLOCKED: MASTER OF THE MYSTICAL FOREST 🌟"""
        
        self.print_boxed(ending_text, Colors.YELLOW + Colors.BOLD, Colors.BG_BLUE)
        return True

    def hero_ending(self):
        treasures = [item for item in self.state.inventory if item in ["Crown of Wisdom", "Sword of Courage", "Crystal of Light"]]
        
        ending_text = f"""⭐ HERO ENDING ⭐

Well done, {Colors.BOLD + Colors.GREEN}{self.state.player_name}{Colors.RESET}!

Your journey through the Mystical Forest has been remarkable.
You have proven yourself to be a true hero through your brave deeds
and wise choices."""
        
        if treasures:
            ending_text += f"\n\nYou successfully claimed: {', '.join(treasures)}"
            ending_text += "\nThese treasures will serve you well in future adventures!"
        
        ending_text += f"""

The forest creatures speak of your kindness and courage.
Your name will be remembered in the songs of the woodland folk.
Though you may not have found every treasure, you have found something
more valuable - the respect and friendship of the forest itself.

You return home as a changed person, wiser and braver than before.
The Mystical Forest will always welcome you back, dear friend.

🌟 ACHIEVEMENT UNLOCKED: HERO OF THE FOREST 🌟"""
        
        self.print_boxed(ending_text, Colors.GREEN + Colors.BOLD)
        return True

    def adventurer_ending(self):
        ending_text = f"""🎒 ADVENTURER ENDING 🎒

{Colors.BOLD + Colors.CYAN}{self.state.player_name}{Colors.RESET}, your adventure comes to a satisfying close.

You have experienced the wonders and mysteries of the Mystical Forest,
faced its challenges with determination, and learned valuable lessons
about courage, wisdom, and friendship.

While you may not have achieved legendary status, you have grown
as a person. The experiences you've gained and the memories you've
made will stay with you forever.

The forest path leads you safely home, where you'll have many
exciting stories to tell