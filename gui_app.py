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
    GOLD = '\033[33m'  # Added missing GOLD color
    
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
            self.animated_print("You've already searched this area thoroughly.", 0.04)
            self.animated_print(failure_text, 0.04, Colors.RED)
            self.state.health = max(10, self.state.health - 15)

            self.wait_for_input()
        return self.forest_crossroads()

        # else:
        #     self.animated_print("You've already searched this area thoroughly.", 0.
        #                         self.animated_print(failure_text, 0.04, Colors.RED)
        # self.state.health = max(10, self.state.health - 15)
        
        # self.wait_for_input()
        # return self.forest_crossroads()

    def ancient_oak(self):
        self.clear_screen()
        self.print_status_bar()
        
        story_text = """🌳 THE ANCIENT OAK 🌳

You approach a massive oak tree that seems older than time itself.
Its trunk is so wide that twenty people holding hands couldn't encircle it.
Carved into the bark are symbols that glow with a faint blue light.

At the base of the tree, a magnificent sword is embedded in a stone,
surrounded by a circle of smaller stones. The blade gleams silver
even in the dappled forest light."""
          
        self.animated_print(story_text, 0.04, Colors.GREEN)

        challenge_text = """A deep voice echoes from the tree itself:
"To claim the Sword of Courage, you must prove your bravery.
Choose your trial:
- Face your greatest fear in combat
- Sacrifice something precious for another's benefit
- Stand guard over the forest's most vulnerable creatures"
"""

        self.animated_print(challenge_text, 0.04, Colors.CYAN)

        
#         self.animated_print(story_text, 0.04, Colors.GREEN)
        
#         challenge_text = """A deep voice echoes from the tree itself:
# "To claim the Sword of Courage, you must prove your bravery.
# Choose your trial:
# - Face your greatest fear in combat
# - Sacrifice something precious for another's benefit
# - Stand guard over the forest's most vulnerable creatures""""
        
#         self.animated_print(challenge_text, 0.04, Colors.CYAN)
        
        print()
        choices = [
            "Face your greatest fear",
            "Make a sacrifice for others",
            "Protect the vulnerable",
            "Leave the sword and return"
        ]
        
        choice = self.get_choice(choices)
        
        if choice == 0:
            return self.face_greatest_fear()
        elif choice == 1:
            return self.make_sacrifice()
        elif choice == 2:
            return self.protect_creatures()
        else:
            return self.forest_crossroads()

    def face_greatest_fear(self):
        self.clear_screen()
        self.print_status_bar()
        
        fear_text = """😰 FACING YOUR GREATEST FEAR 😰

The world around you shifts and warps. You find yourself in a dark cavern
face-to-face with a massive shadow version of yourself - but this shadow
represents all your doubts, fears, and failures.

"You are not worthy," the shadow speaks in your voice. "You will fail like always."

The shadow attacks! You must choose how to respond."""
        
        self.animated_print(fear_text, 0.04, Colors.RED)
        
        print()
        choices = [
            "Fight the shadow with physical strength",
            "Use magic to dispel the illusion",
            "Accept your fears and embrace them",
            "Try to reason with your shadow self"
        ]
        
        choice = self.get_choice(choices)
        
        if choice == 2:  # Accepting fears shows true courage
            return self.courage_success()
        else:
            return self.courage_partial()

    def make_sacrifice(self):
        self.clear_screen()
        self.print_status_bar()
        
        if not self.state.inventory:
            sacrifice_text = """💔 THE SACRIFICE 💔

You want to make a sacrifice, but you have nothing to give.
The tree's voice speaks again: "True sacrifice comes from the heart,
not from possessions. Give of yourself."

You offer your own life force to heal the forest."""
            
            self.animated_print(sacrifice_text, 0.04, Colors.YELLOW)
            
            self.state.health = max(20, self.state.health - 30)
            return self.courage_success()
        else:
            item_to_sacrifice = self.state.inventory[0]
            sacrifice_text = f"""💔 THE SACRIFICE 💔

You take your {item_to_sacrifice} and place it at the base of the ancient oak.
"I offer this freely to help protect the forest and its creatures."

The item glows brightly and dissolves into pure light that flows into the tree.
You feel the forest itself acknowledging your selfless act."""
            
            self.animated_print(sacrifice_text, 0.04, Colors.YELLOW)
            
            self.state.inventory.remove(item_to_sacrifice)
            return self.courage_success()

    def protect_creatures(self):
        self.clear_screen()
        self.print_status_bar()
        
        protect_text = """🛡️ PROTECTING THE VULNERABLE 🛡️

Suddenly, you hear frightened chirping from above. A family of baby birds
has fallen from their nest, and a hungry fox approaches menacingly.

You step between the fox and the helpless birds, spreading your arms wide.
"You'll have to go through me first," you declare bravely."""
        
        self.animated_print(protect_text, 0.04, Colors.BLUE)
        
        if "Animal Communication" in self.state.inventory:
            communicate_text = """Using your ability to communicate with animals, you speak to the fox:
"Friend fox, I understand you're hungry, but these babies are defenseless.
Let me help you find other food instead." """
            
            self.animated_print(communicate_text, 0.04, Colors.GREEN)
            return self.courage_success()
        else:
            if random.randint(1, 100) <= 75:
                success_text = """The fox looks into your determined eyes and, sensing your resolve,
turns away to hunt elsewhere. You gently return the baby birds to their nest."""
                self.animated_print(success_text, 0.04, Colors.GREEN)
                return self.courage_success()
            else:
                failure_text = """The fox attacks! You fight bravely but sustain injuries protecting the birds.
Your courage is noted, though you wish you had been stronger."""
                self.animated_print(failure_text, 0.04, Colors.RED)
                self.state.health = max(15, self.state.health - 25)
                return self.courage_partial()

    def courage_success(self):
        self.clear_screen()
        self.print_status_bar()
        
        success_text = """⚔️ SWORD OF COURAGE OBTAINED ⚔️

"You have shown true courage," the ancient oak declares.
"Not the absence of fear, but the willingness to act despite it."

The sword slides effortlessly from the stone into your hand.
It feels perfectly balanced, and you sense its power flowing through you.
Your physical strength and confidence increase dramatically!"""
        
        self.animated_print(success_text, 0.04, Colors.GOLD)
        
        self.state.inventory.append("Sword of Courage")
        self.state.health = min(100, self.state.health + 40)
        self.state.story_flags["courage_sword"] = True
        
        self.wait_for_input()
        return self.determine_ending()

    def courage_partial(self):
        self.clear_screen()
        self.print_status_bar()
        
        partial_text = """⚔️ COURAGE RECOGNIZED ⚔️

"You have shown courage, though not without struggle," the oak says.
"Take this lesser blade as recognition of your efforts."

A smaller but still beautiful sword appears in your hands.
It's not the legendary Sword of Courage, but it will serve you well."""
        
        self.animated_print(partial_text, 0.04, Colors.CYAN)
        
        self.state.inventory.append("Oak Blade")
        self.state.health = min(100, self.state.health + 15)
        
        self.wait_for_input()
        return self.forest_crossroads()

    def deep_cave(self):
        self.clear_screen()
        self.print_status_bar()
        
        story_text = """🕳️ THE DEEP CAVE 🕳️

You descend into a vast underground cavern. Stalactites hang like teeth
from the ceiling, and somewhere in the darkness, water drips steadily.
Your footsteps echo ominously in the depths.

As you venture deeper, you notice the walls beginning to glow with
an ethereal blue light. At the heart of the cavern, you discover
a magnificent crystal formation pulsing with pure light energy.

But guarding the crystal is a massive stone guardian, its eyes
glowing red in the darkness."""
        
        self.animated_print(story_text, 0.04, Colors.BLUE)
        
        guardian_text = """The stone guardian speaks in a voice like grinding rocks:
"Who dares seek the Crystal of Light? Prove you are worthy
by demonstrating the three virtues: Wisdom, Courage, and Compassion." """
        
        self.animated_print(guardian_text, 0.04, Colors.WHITE)
        
        print()
        choices = [
            "Show wisdom through clever reasoning",
            "Display courage by facing the guardian",
            "Demonstrate compassion for others",
            "Try to sneak past the guardian"
        ]
        
        choice = self.get_choice(choices)
        
        if choice == 0:
            return self.wisdom_test()
        elif choice == 1:
            return self.courage_test()
        elif choice == 2:
            return self.compassion_test()
        else:
            return self.sneak_attempt()

    def wisdom_test(self):
        self.clear_screen()
        self.print_status_bar()
        
        wisdom_text = """🧠 TEST OF WISDOM 🧠

"Answer me this," rumbles the guardian. "A merchant has three items:
a lamp that reveals truth, a mirror that shows the future, and a key
that opens any lock. He can only keep one. Which should he choose
and why?" """
        
        self.animated_print(wisdom_text, 0.04, Colors.YELLOW)
        
        print()
        choices = [
            "The lamp - Truth is the foundation of all wisdom",
            "The mirror - Knowing the future prevents mistakes",
            "The key - Freedom and opportunity are most valuable",
            "None - True wisdom comes from within, not objects"
        ]
        
        choice = self.get_choice(choices)
        
        if choice == 3:  # The philosophical answer
            wisdom_success_text = """✨ WISDOM PROVEN ✨

"Excellent!" the guardian booms. "You understand that external tools
are merely aids - true wisdom comes from within. You have passed
the test of wisdom." """
            
            self.animated_print(wisdom_success_text, 0.04, Colors.GOLD)
            self.state.story_flags["passed_wisdom"] = True
        else:
            wisdom_partial_text = """The guardian nods slowly. "A reasonable answer, but not the deepest truth.
You show some wisdom, but have more to learn." """
            
            self.animated_print(wisdom_partial_text, 0.04, Colors.CYAN)
        
        self.wait_for_input()
        return self.check_crystal_worthiness()

    def courage_test(self):
        self.clear_screen()
        self.print_status_bar()
        
        courage_text = """⚔️ TEST OF COURAGE ⚔️

The stone guardian rises to its full, imposing height and brandishes
massive stone fists. "Face me in combat, little one, and show me
your courage!"

But as it prepares to attack, you notice something - the guardian's
movements are stiff and painful. Ancient cracks run through its body."""
        
        self.animated_print(courage_text, 0.04, Colors.RED)
        
        print()
        choices = [
            "Attack the guardian with full force",
            "Offer to help heal the guardian's cracks",
            "Stand your ground but refuse to fight",
            "Try to dodge and tire the guardian out"
        ]
        
        choice = self.get_choice(choices)
        
        if choice == 1:  # Helping shows true courage
            courage_success_text = """❤️ TRUE COURAGE SHOWN ❤️

"You would help your opponent?" the guardian asks, surprised.
"This is true courage - compassion in the face of danger."

You use your magic to help seal the ancient cracks. The guardian's
eyes change from red to warm gold."""
            
            self.animated_print(courage_success_text, 0.04, Colors.GREEN)
            self.state.story_flags["passed_courage"] = True
            self.state.magic = max(5, self.state.magic - 15)
        else:
            courage_partial_text = """The guardian tests your mettle in combat but pulls back before
serious harm. "You have some courage, but true bravery shows
compassion even for enemies." """
            
            self.animated_print(courage_partial_text, 0.04, Colors.YELLOW)
            self.state.health = max(20, self.state.health - 20)
        
        self.wait_for_input()
        return self.check_crystal_worthiness()

    def compassion_test(self):
        self.clear_screen()
        self.print_status_bar()
        
        compassion_text = """💖 TEST OF COMPASSION 💖

The guardian steps aside, revealing a small, injured cave creature
trapped under fallen rocks. It whimpers pitifully.

"This creature has been trapped here for days," the guardian explains.
"What will you do? Helping it will cost you time and energy, and the
crystal might be claimed by another while you delay." """
        
        self.animated_print(compassion_text, 0.04, Colors.MAGENTA)
        
        print()
        choices = [
            "Immediately help free the creature",
            "Help, but quickly to save time",
            "Ignore it - the crystal is more important",
            "Ask the guardian to help instead"
        ]
        
        choice = self.get_choice(choices)
        
        if choice == 0:  # Immediate help shows pure compassion
            compassion_success_text = """🌟 PURE COMPASSION SHOWN 🌟

Without hesitation, you rush to help the trapped creature.
You carefully move the rocks and tend to its wounds, using
your own supplies to make it comfortable.

"True compassion acts without thought of reward," the guardian
says approvingly. "You have passed the test." """
            
            self.animated_print(compassion_success_text, 0.04, Colors.GREEN)
            self.state.story_flags["passed_compassion"] = True
            if "Healing Potion" in self.state.inventory:
                self.state.inventory.remove("Healing Potion")
        else:
            compassion_partial_text = """You help the creature, but your hesitation was noticed.
"Compassion that calculates is not pure compassion," the guardian
observes. "But you still chose to help." """
            
            self.animated_print(compassion_partial_text, 0.04, Colors.CYAN)
        
        self.wait_for_input()
        return self.check_crystal_worthiness()

    def sneak_attempt(self):
        self.clear_screen()
        self.print_status_bar()
        
        sneak_text = """🤐 ATTEMPTING TO SNEAK 🤐

You try to creep around the stone guardian while it's not looking.
Step by careful step, you make your way toward the crystal..."""
        
        self.animated_print(sneak_text, 0.04, Colors.DIM)
        
        if random.randint(1, 100) <= 30:
            sneak_success_text = """Somehow, you manage to reach the crystal undetected!
But as you touch it, the guardian's voice booms:
"Cleverness without virtue is hollow. Take your prize,
but know that you have learned nothing." """
            
            self.animated_print(sneak_success_text, 0.04, Colors.YELLOW)
            self.state.inventory.append("Dim Crystal")
        else:
            sneak_failure_text = """The guardian's eyes swivel toward you.
"Sneaking shows neither wisdom, courage, nor compassion.
Face the tests properly, or leave my domain." """
            
            self.animated_print(sneak_failure_text, 0.04, Colors.RED)
        
        self.wait_for_input()
        return self.deep_cave()

    def check_crystal_worthiness(self):
        tests_passed = sum([
            "passed_wisdom" in self.state.story_flags,
            "passed_courage" in self.state.story_flags,
            "passed_compassion" in self.state.story_flags
        ])
        
        if tests_passed == 3:
            return self.crystal_perfect_success()
        elif tests_passed >= 2:
            return self.crystal_good_success()
        else:
            return self.crystal_partial_success()

    def crystal_perfect_success(self):
        self.clear_screen()
        self.print_status_bar()
        
        perfect_text = """💎 CRYSTAL OF LIGHT OBTAINED 💎

"You have proven yourself in all three virtues," the guardian proclaims.
"Wisdom, Courage, and Compassion - the true foundations of light."

The Crystal of Light floats toward you, pulsing with pure, warm energy.
As you grasp it, light fills every corner of the cave, and you feel
an incredible surge of magical power and inner peace."""
        
        self.animated_print(perfect_text, 0.04, Colors.GOLD)
        
        self.state.inventory.append("Crystal of Light")
        self.state.magic = 50  # Full magic restoration
        self.state.health = min(100, self.state.health + 25)
        self.state.story_flags["light_crystal"] = True
        
        self.wait_for_input()
        return self.determine_ending()

    def crystal_good_success(self):
        self.clear_screen()
        self.print_status_bar()
        
        good_text = """💎 BRIGHT CRYSTAL OBTAINED 💎

"You have shown worthy character in most virtues," the guardian says.
"Take this Bright Crystal as recognition of your efforts."

A smaller but still radiant crystal appears in your hands.
It fills you with warmth and restores some of your energy."""
        
        self.animated_print(good_text, 0.04, Colors.CYAN)
        
        self.state.inventory.append("Bright Crystal")
        self.state.magic = min(50, self.state.magic + 20)
        self.state.health = min(100, self.state.health + 15)
        
        self.wait_for_input()
        return self.determine_ending()

    def crystal_partial_success(self):
        self.clear_screen()
        self.print_status_bar()
        
        partial_text = """💎 SMALL CRYSTAL OBTAINED 💎

"You have much to learn," the guardian says, not unkindly.
"But your effort is noted. Take this Small Crystal and continue
your journey toward wisdom."

A modest crystal appears, glowing softly in your palm."""
        
        self.animated_print(partial_text, 0.04, Colors.WHITE)
        
        self.state.inventory.append("Small Crystal")
        self.state.magic = min(50, self.state.magic + 10)
        
        self.wait_for_input()
        return self.forest_crossroads()

    def determine_ending(self):
        # Count legendary items
        legendary_items = sum([
            "Crown of Wisdom" in self.state.inventory,
            "Sword of Courage" in self.state.inventory,
            "Crystal of Light" in self.state.inventory
        ])
        
        if legendary_items == 3:
            return self.legendary_hero_ending()
        elif legendary_items == 2:
            return self.noble_hero_ending()
        elif legendary_items == 1:
            return self.aspiring_hero_ending()
        else:
            return self.humble_adventurer_ending()

    def legendary_hero_ending(self):
        self.clear_screen()
        self.print_status_bar()
        
        legendary_text = f"""🏆 LEGENDARY HERO ENDING 🏆

{self.state.player_name}, you have achieved the impossible!

With the Crown of Wisdom upon your head, the Sword of Courage in your hand,
and the Crystal of Light illuminating your path, you have become a true
legendary hero of the Mystical Forest.

The three artifacts resonate with each other, creating a harmony of power
that transforms not just you, but the entire forest. Dark creatures flee,
lost travelers find their way, and the very trees sing songs of hope.

You are now the Guardian of the Mystical Forest, protector of all who
seek adventure within its borders. Your legend will be told for
generations to come.

CONGRATULATIONS! You achieved the PERFECT ENDING!"""
        
        self.animated_print(legendary_text, 0.04, Colors.GOLD)
        
        return self.show_final_stats("LEGENDARY HERO")

    def noble_hero_ending(self):
        self.clear_screen()
        self.print_status_bar()
        
        noble_text = f"""🌟 NOBLE HERO ENDING 🌟

{self.state.player_name}, you have proven yourself a true hero!

With two of the three legendary artifacts, you have gained great power
and wisdom. Though not complete, your collection of sacred items marks
you as one of the greatest adventurers to ever enter the Mystical Forest.

You become a respected guardian of the forest, helping other adventurers
and protecting the innocent. Your deeds inspire others to seek their
own paths to heroism.

The forest spirits smile upon you, and you know you can always return
to seek the remaining artifact when you're ready.

EXCELLENT! You achieved a HEROIC ENDING!"""
        
        self.animated_print(noble_text, 0.04, Colors.GREEN)
        
        return self.show_final_stats("NOBLE HERO")

    def aspiring_hero_ending(self):
        self.clear_screen()
        self.print_status_bar()
        
        aspiring_text = f"""⭐ ASPIRING HERO ENDING ⭐

{self.state.player_name}, you have taken your first steps toward greatness!

With one legendary artifact in your possession, you have proven that
you have the potential for true heroism. Your journey through the
Mystical Forest has taught you valuable lessons and granted you
significant power.

You leave the forest changed, with new abilities and a clear purpose.
The artifact you carry serves as both a tool and a reminder of what
you can achieve when you set your mind to it.

The path to legendary status still lies before you, but you now
have the experience and wisdom to walk it.

GOOD JOB! You achieved an ASPIRING HERO ENDING!"""
        
        self.animated_print(aspiring_text, 0.04, Colors.CYAN)
        
        return self.show_final_stats("ASPIRING HERO")

    def humble_adventurer_ending(self):
        self.clear_screen()
        self.print_status_bar()
        
        humble_text = f"""🌿 HUMBLE ADVENTURER ENDING 🌿

{self.state.player_name}, your adventure through the Mystical Forest
has come to an end.

Though you didn't obtain any legendary artifacts, your journey was
not in vain. You've gained valuable experience, met interesting
characters, and learned important lessons about yourself and the world.

Sometimes the greatest adventures are not about the treasures we find,
but about the growth we experience along the way. You leave the forest
wiser and more experienced than when you entered.

The forest will always welcome you back when you're ready for another
adventure. Perhaps next time, you'll be prepared for even greater
challenges.

You achieved a HUMBLE ADVENTURER ENDING!"""
        
        self.animated_print(humble_text, 0.04, Colors.WHITE)
        
        return self.show_final_stats("HUMBLE ADVENTURER")

    def show_final_stats(self, ending_type: str):
        self.clear_screen()
        
        stats_text = f"""
╔══════════════════════════════════════════╗
║              FINAL STATISTICS            ║
╠══════════════════════════════════════════╣
║ Player Name: {self.state.player_name:<27} ║
║ Ending Type: {ending_type:<27} ║
║ Final Health: {self.state.health:<26} ║
║ Final Magic: {self.state.magic:<27} ║
║ Items Collected: {len(self.state.inventory):<20} ║
║ Locations Visited: {len(self.state.visited_locations):<16} ║
╚══════════════════════════════════════════╝
        """
        
        self.print_centered(stats_text, Colors.YELLOW)
        
        if self.state.inventory:
            self.print_centered("🎒 Final Inventory:", Colors.CYAN)
            for item in self.state.inventory:
                self.print_centered(f"  • {item}", Colors.WHITE)
        
        print()
        self.print_centered("Thank you for playing Mystical Forest Quest!", Colors.GREEN)
        
        print()
        choices = [
            "Play again",
            "Exit game"
        ]
        
        choice = self.get_choice(choices)
        
        if choice == 0:
            return self.restart_game()
        else:
            return self.exit_game()

    def restart_game(self):
        self.state = GameState()
        return self.start_game()

    def exit_game(self):
        self.clear_screen()
        
        goodbye_text = """
╔══════════════════════════════════════════╗
║     Thank you for playing!               ║
║     🌲 MYSTICAL FOREST QUEST 🌲          ║
║                                          ║
║     May your adventures continue...      ║
╚══════════════════════════════════════════╝
        """
        
        self.print_centered(goodbye_text, Colors.GREEN + Colors.BOLD)
        print()
        self.animated_print("Goodbye, brave adventurer!", 0.05, Colors.CYAN)
        return

    def start_game(self):
        """Main game loop"""
        self.show_title_screen()
        self.get_player_name()
        return self.forest_entrance()

        class Colors:
    RED = '\033[91m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'

class AdventureGame:
    def start_game(self):
        print("Welcome to the Adventure Game!")

def main():
    """Entry point for the game"""
    try:
        game = AdventureGame()
        game.start_game()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Game interrupted. Thanks for playing!{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}An error occurred: {e}{Colors.RESET}")

if __name__ == "__main__":
    main()