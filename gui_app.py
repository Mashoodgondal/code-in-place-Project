# Algorithm Challenge App - Professional Design
# A comprehensive application for solving algorithm-based puzzles with modern UI

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random
import string
import math
from typing import List, Tuple, Optional
from abc import ABC, abstractmethod

class Challenge(ABC):
    """Abstract base class for all challenges"""
    
    def __init__(self, name: str, description: str, color: str, icon: str):
        self.name = name
        self.description = description
        self.color = color
        self.icon = icon
        self.completed = False
    
    @abstractmethod
    def generate_problem(self):
        """Generate a new problem instance"""
        pass
    
    @abstractmethod
    def check_solution(self, solution):
        """Check if the provided solution is correct"""
        pass
    
    @abstractmethod
    def get_hint(self):
        """Provide a hint for solving the problem"""
        pass
    
    @abstractmethod
    def get_solution(self):
        """Get the complete solution with explanation"""
        pass

class SudokuChallenge(Challenge):
    """Sudoku puzzle challenge"""
    
    def __init__(self):
        super().__init__("Sudoku Solver", "Solve a 9x9 Sudoku puzzle using logical deduction", 
                         "#FF6B6B", "🧩")
        self.board = None
        self.solution = None
    
    def generate_problem(self):
        """Generate a new Sudoku puzzle"""
        # Create a complete solved board
        self.solution = [[0 for _ in range(9)] for _ in range(9)]
        self._fill_board(self.solution)
        
        # Create puzzle by removing numbers
        self.board = [row[:] for row in self.solution]
        cells_to_remove = random.randint(40, 55)
        
        for _ in range(cells_to_remove):
            row, col = random.randint(0, 8), random.randint(0, 8)
            self.board[row][col] = 0
        
        return self._format_board(self.board)
    
    def _fill_board(self, board):
        """Fill the board using backtracking"""
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    numbers = list(range(1, 10))
                    random.shuffle(numbers)
                    for num in numbers:
                        if self._is_valid(board, i, j, num):
                            board[i][j] = num
                            if self._fill_board(board):
                                return True
                            board[i][j] = 0
                    return False
        return True
    
    def _is_valid(self, board, row, col, num):
        """Check if placing num at (row, col) is valid"""
        # Check row
        for j in range(9):
            if board[row][j] == num:
                return False
        
        # Check column
        for i in range(9):
            if board[i][col] == num:
                return False
        
        # Check 3x3 box
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if board[i][j] == num:
                    return False
        
        return True
    
    def _format_board(self, board):
        """Format board for display"""
        result = "🧩 Sudoku Puzzle (Enter digits 1-9, use 0 for empty cells):\n\n"
        for i, row in enumerate(board):
            if i % 3 == 0 and i != 0:
                result += "  ──────┼───────┼──────\n"
            for j, cell in enumerate(row):
                if j % 3 == 0 and j != 0:
                    result += " │ "
                elif j == 0:
                    result += "  "
                result += f"{cell if cell != 0 else '·'} "
            result += "\n"
        return result
    
    def check_solution(self, solution):
        """Check if the provided solution is correct"""
        try:
            lines = solution.strip().split('\n')
            user_board = []
            for line in lines:
                if any(c.isdigit() for c in line):
                    row = [int(c) for c in line if c.isdigit()]
                    if len(row) == 9:
                        user_board.append(row)
            
            if len(user_board) != 9:
                return False
            
            return user_board == self.solution
        except:
            return False
    
    def get_hint(self):
        """Provide a hint for Sudoku solving"""
        hints = [
            "🔍 Look for cells where only one number can fit",
            "📍 Check if a number can only go in one place in a row/column/box",
            "❌ Use the process of elimination to narrow down possibilities", 
            "🎯 Focus on rows, columns, or boxes with the most filled cells"
        ]
        return random.choice(hints)
    
    def get_solution(self):
        """Get the complete solution"""
        return f"✅ Complete Solution:\n\n{self._format_board(self.solution)}\n\n💡 Strategy: Use logical deduction by finding cells with only one possible number, then numbers that can only go in one place within a row, column, or 3x3 box."

class NumberSequenceChallenge(Challenge):
    """Number sequence pattern recognition challenge"""
    
    def __init__(self):
        super().__init__("Number Sequences", "Find the pattern in number sequences", 
                         "#4ECDC4", "🔢")
        self.sequence = None
        self.pattern_type = None
        self.next_numbers = None
    
    def generate_problem(self):
        """Generate a new number sequence problem"""
        patterns = [
            self._arithmetic_sequence,
            self._geometric_sequence,
            self._fibonacci_like,
            self._square_sequence,
            self._prime_sequence
        ]
        
        pattern_func = random.choice(patterns)
        self.sequence, self.pattern_type, self.next_numbers = pattern_func()
        
        display_sequence = self.sequence[:-2]  # Hide last 2 numbers
        return f"🔢 Find the next 2 numbers in this sequence:\n\n📊 Sequence: {', '.join(map(str, display_sequence))}, ?, ?\n\n🏷️  Pattern type: {self.pattern_type}\n\n💭 Enter the two missing numbers separated by comma or space"
    
    def _arithmetic_sequence(self):
        """Generate arithmetic sequence"""
        start = random.randint(1, 20)
        diff = random.randint(2, 10)
        sequence = [start + i * diff for i in range(8)]
        return sequence, "Arithmetic (constant difference)", sequence[-2:]
    
    def _geometric_sequence(self):
        """Generate geometric sequence"""
        start = random.randint(2, 5)
        ratio = random.randint(2, 3)
        sequence = [start * (ratio ** i) for i in range(6)]
        return sequence, "Geometric (constant ratio)", sequence[-2:]
    
    def _fibonacci_like(self):
        """Generate Fibonacci-like sequence"""
        a, b = random.randint(1, 5), random.randint(1, 5)
        sequence = [a, b]
        for _ in range(6):
            sequence.append(sequence[-1] + sequence[-2])
        return sequence, "Fibonacci-like (sum of previous two)", sequence[-2:]
    
    def _square_sequence(self):
        """Generate square number sequence"""
        start = random.randint(1, 3)
        sequence = [(start + i) ** 2 for i in range(7)]
        return sequence, "Perfect squares", sequence[-2:]
    
    def _prime_sequence(self):
        """Generate prime number sequence"""
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        start_idx = random.randint(0, 3)
        sequence = primes[start_idx:start_idx + 7]
        return sequence, "Prime numbers", sequence[-2:]
    
    def check_solution(self, solution):
        """Check if the provided solution is correct"""
        try:
            numbers = [int(x.strip()) for x in solution.replace(',', ' ').split()]
            return len(numbers) == 2 and numbers == self.next_numbers
        except:
            return False
    
    def get_hint(self):
        """Provide a hint for sequence solving"""
        hints = {
            "Arithmetic": "➕ Look at the differences between consecutive numbers",
            "Geometric": "✖️ Look at the ratios between consecutive numbers", 
            "Fibonacci-like": "🔄 Each number might be the sum of the previous two",
            "Perfect squares": "²️⃣ These might be perfect squares of consecutive integers",
            "Prime numbers": "🔢 These might be prime numbers in order"
        }
        for key in hints:
            if key in self.pattern_type:
                return hints[key]
        return "🧮 Look for mathematical relationships between the numbers"
    
    def get_solution(self):
        """Get the complete solution"""
        return f"✅ Complete sequence: {', '.join(map(str, self.sequence))}\n\n🎯 Pattern: {self.pattern_type}\n📊 Next two numbers: {', '.join(map(str, self.next_numbers))}"

class CryptographyChallenge(Challenge):
    """Simple cryptography puzzle challenge"""
    
    def __init__(self):
        super().__init__("Caesar Cipher", "Decode messages using Caesar cipher", 
                         "#45B7D1", "🔐")
        self.original_message = None
        self.encoded_message = None
        self.shift = None
    
    def generate_problem(self):
        """Generate a new cryptography problem"""
        messages = [
            "HELLO WORLD",
            "PYTHON IS GREAT", 
            "ALGORITHMS ARE FUN",
            "KEEP LEARNING",
            "SOLVE THE PUZZLE",
            "CRYPTOGRAPHY ROCKS",
            "SUCCESS AWAITS",
            "NEVER GIVE UP"
        ]
        
        self.original_message = random.choice(messages)
        self.shift = random.randint(1, 25)
        self.encoded_message = self._caesar_encode(self.original_message, self.shift)
        
        return f"🔐 Decode this Caesar cipher:\n\n📝 Encoded message: {self.encoded_message}\n\n💡 Hint: Each letter is shifted by the same amount (1-25 positions)\n\n🎯 Enter the decoded message (original text):"
    
    def _caesar_encode(self, message, shift):
        """Encode message using Caesar cipher"""
        result = ""
        for char in message:
            if char.isalpha():
                ascii_offset = ord('A') if char.isupper() else ord('a')
                result += chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
            else:
                result += char
        return result
    
    def _caesar_decode(self, message, shift):
        """Decode message using Caesar cipher"""
        return self._caesar_encode(message, -shift)
    
    def check_solution(self, solution):
        """Check if the provided solution is correct"""
        return solution.upper().strip() == self.original_message
    
    def get_hint(self):
        """Provide a hint for cryptography solving"""
        hints = [
            "🔤 The most common letter in English is 'E' - look for patterns",
            "🔄 Try different shift values systematically (1, 2, 3...)",
            "📚 Remember: A=0, B=1, C=2... Z=25",
            "🎯 Each letter is consistently shifted by the same amount"
        ]
        return random.choice(hints)
    
    def get_solution(self):
        """Get the complete solution"""
        return f"✅ Original message: {self.original_message}\n🔢 Shift amount: {self.shift}\n\n💡 To decode: shift each letter backwards by {self.shift} positions in the alphabet."

class ModernStyle:
    """Modern styling configuration"""
    
    # Color Palette
    COLORS = {
        'bg_primary': '#1a1a2e',      # Dark navy
        'bg_secondary': '#16213e',     # Darker navy
        'bg_tertiary': '#0f3460',      # Deep blue
        'accent_primary': '#e94560',   # Coral red
        'accent_secondary': '#f39c12', # Orange
        'text_primary': '#ffffff',     # White
        'text_secondary': '#a8a8a8',   # Light gray
        'success': '#27ae60',          # Green
        'warning': '#f39c12',          # Orange
        'error': '#e74c3c',            # Red
        'card_bg': '#252540',          # Card background
        'button_hover': '#2c2c54'      # Button hover
    }
    
    @staticmethod
    def configure_styles():
        """Configure modern ttk styles"""
        style = ttk.Style()
        
        # Configure modern button style
        style.configure('Modern.TButton',
                       font=('Segoe UI', 10, 'bold'),
                       padding=(20, 10),
                       relief='flat')
        
        # Configure challenge button styles
        style.configure('Challenge.TButton',
                       font=('Segoe UI', 11, 'bold'),
                       padding=(15, 8),
                       relief='flat')
        
        # Configure action button styles  
        style.configure('Action.TButton',
                       font=('Segoe UI', 9, 'bold'),
                       padding=(12, 6),
                       relief='flat')
        
        # Configure label styles
        style.configure('Title.TLabel',
                       font=('Segoe UI', 24, 'bold'),
                       foreground=ModernStyle.COLORS['text_primary'])
        
        style.configure('Subtitle.TLabel',
                       font=('Segoe UI', 12),
                       foreground=ModernStyle.COLORS['text_secondary'])
        
        style.configure('Header.TLabel',
                       font=('Segoe UI', 14, 'bold'),
                       foreground=ModernStyle.COLORS['text_primary'])

class AlgorithmChallengeApp:
    """Main application class with modern design"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🧠 Algorithm Challenge App")
        self.root.geometry("1000x700")
        self.root.configure(bg=ModernStyle.COLORS['bg_primary'])
        self.root.resizable(True, True)
        
        # Configure modern styles
        ModernStyle.configure_styles()
        
        # Initialize challenges
        self.challenges = [
            SudokuChallenge(),
            NumberSequenceChallenge(),
            CryptographyChallenge()
        ]
        self.current_challenge = None
        self.current_problem = None
        
        self.setup_ui()
        self.show_welcome()
    
    def setup_ui(self):
        """Set up the modern user interface"""
        # Create main container with padding
        main_container = tk.Frame(self.root, bg=ModernStyle.COLORS['bg_primary'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header section
        self.create_header(main_container)
        
        # Challenge selection section
        self.create_challenge_section(main_container)
        
        # Problem display section
        self.create_problem_section(main_container)
        
        # Solution input section
        self.create_solution_section(main_container)
        
        # Action buttons section
        self.create_action_section(main_container)
    
    def create_header(self, parent):
        """Create the header section"""
        header_frame = tk.Frame(parent, bg=ModernStyle.COLORS['bg_primary'])
        header_frame.pack(fill=tk.X, pady=(0, 30))
        
        # Main title with gradient effect
        title_frame = tk.Frame(header_frame, bg=ModernStyle.COLORS['bg_secondary'], 
                              relief='flat', bd=0)
        title_frame.pack(fill=tk.X, pady=10)
        
        title_label = tk.Label(title_frame, text="🧠 Algorithm Challenge App",
                              font=('Segoe UI', 26, 'bold'),
                              fg=ModernStyle.COLORS['text_primary'],
                              bg=ModernStyle.COLORS['bg_secondary'],
                              pady=15)
        title_label.pack()
        
        subtitle_label = tk.Label(header_frame, 
                                 text="Master algorithmic thinking through interactive challenges",
                                 font=('Segoe UI', 12),
                                 fg=ModernStyle.COLORS['text_secondary'],
                                 bg=ModernStyle.COLORS['bg_primary'])
        subtitle_label.pack(pady=(5, 0))
    
    def create_challenge_section(self, parent):
        """Create the challenge selection section"""
        section_frame = tk.Frame(parent, bg=ModernStyle.COLORS['bg_primary'])
        section_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Section header
        header_label = tk.Label(section_frame, text="🎯 Choose Your Challenge",
                               font=('Segoe UI', 16, 'bold'),
                               fg=ModernStyle.COLORS['text_primary'],
                               bg=ModernStyle.COLORS['bg_primary'])
        header_label.pack(anchor=tk.W, pady=(0, 15))
        
        # Challenge cards container
        cards_frame = tk.Frame(section_frame, bg=ModernStyle.COLORS['bg_primary'])
        cards_frame.pack(fill=tk.X)
        
        # Create challenge cards
        for i, challenge in enumerate(self.challenges):
            self.create_challenge_card(cards_frame, challenge, i)
    
    def create_challenge_card(self, parent, challenge, index):
        """Create a modern challenge card"""
        # Card frame
        card_frame = tk.Frame(parent, bg=ModernStyle.COLORS['card_bg'],
                             relief='flat', bd=0, padx=15, pady=15)
        card_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        # Challenge icon and name
        icon_label = tk.Label(card_frame, text=challenge.icon,
                             font=('Segoe UI', 24),
                             bg=ModernStyle.COLORS['card_bg'],
                             fg=challenge.color)
        icon_label.pack(pady=(5, 10))
        
        name_label = tk.Label(card_frame, text=challenge.name,
                             font=('Segoe UI', 12, 'bold'),
                             fg=ModernStyle.COLORS['text_primary'],
                             bg=ModernStyle.COLORS['card_bg'])
        name_label.pack(pady=(0, 5))
        
        desc_label = tk.Label(card_frame, text=challenge.description,
                             font=('Segoe UI', 9),
                             fg=ModernStyle.COLORS['text_secondary'],
                             bg=ModernStyle.COLORS['card_bg'],
                             wraplength=180, justify=tk.CENTER)
        desc_label.pack(pady=(0, 15))
        
        # Challenge button
        btn = tk.Button(card_frame, text="Start Challenge",
                       font=('Segoe UI', 10, 'bold'),
                       bg=challenge.color,
                       fg='white',
                       relief='flat',
                       bd=0,
                       pady=8,
                       cursor='hand2',
                       command=lambda c=challenge: self.start_challenge(c))
        btn.pack(fill=tk.X, padx=10)
        
        # Hover effects
        def on_enter(e):
            btn.configure(bg=self.darken_color(challenge.color))
        def on_leave(e):
            btn.configure(bg=challenge.color)
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
    
    def create_problem_section(self, parent):
        """Create the problem display section"""
        section_frame = tk.Frame(parent, bg=ModernStyle.COLORS['bg_primary'])
        section_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Section header
        header_label = tk.Label(section_frame, text="📋 Problem Statement",
                               font=('Segoe UI', 16, 'bold'),
                               fg=ModernStyle.COLORS['text_primary'],
                               bg=ModernStyle.COLORS['bg_primary'])
        header_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Problem display area with modern styling
        problem_frame = tk.Frame(section_frame, bg=ModernStyle.COLORS['card_bg'],
                                relief='flat', bd=0)
        problem_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.problem_text = scrolledtext.ScrolledText(
            problem_frame,
            font=('Consolas', 11),
            bg=ModernStyle.COLORS['card_bg'],
            fg=ModernStyle.COLORS['text_primary'],
            relief='flat',
            bd=0,
            padx=20,
            pady=20,
            wrap=tk.WORD,
            selectbackground=ModernStyle.COLORS['accent_primary'],
            insertbackground=ModernStyle.COLORS['text_primary']
        )
        self.problem_text.pack(fill=tk.BOTH, expand=True)
    
    def create_solution_section(self, parent):
        """Create the solution input section"""
        section_frame = tk.Frame(parent, bg=ModernStyle.COLORS['bg_primary'])
        section_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Section header
        header_label = tk.Label(section_frame, text="💡 Your Solution",
                               font=('Segoe UI', 16, 'bold'),
                               fg=ModernStyle.COLORS['text_primary'],
                               bg=ModernStyle.COLORS['bg_primary'])
        header_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Solution input area
        solution_frame = tk.Frame(section_frame, bg=ModernStyle.COLORS['card_bg'],
                                 relief='flat', bd=0)
        solution_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.solution_entry = scrolledtext.ScrolledText(
            solution_frame,
            height=4,
            font=('Consolas', 11),
            bg=ModernStyle.COLORS['card_bg'],
            fg=ModernStyle.COLORS['text_primary'],
            relief='flat',
            bd=0,
            padx=20,
            pady=15,
            wrap=tk.WORD,
            selectbackground=ModernStyle.COLORS['accent_primary'],
            insertbackground=ModernStyle.COLORS['text_primary']
        )
        self.solution_entry.pack(fill=tk.X)
    
    def create_action_section(self, parent):
        """Create the action buttons section"""
        section_frame = tk.Frame(parent, bg=ModernStyle.COLORS['bg_primary'])
        section_frame.pack(fill=tk.X)
        
        # Center the buttons
        button_container = tk.Frame(section_frame, bg=ModernStyle.COLORS['bg_primary'])
        button_container.pack(expand=True)
        
        # Action buttons with modern styling
        buttons_data = [
            ("✅ Check Solution", self.check_solution, ModernStyle.COLORS['success']),
            ("💡 Get Hint", self.get_hint, ModernStyle.COLORS['warning']),
            ("📖 Show Solution", self.show_solution, ModernStyle.COLORS['accent_secondary']),
            ("🔄 New Problem", self.new_problem, ModernStyle.COLORS['accent_primary'])
        ]
        
        self.action_buttons = []
        for i, (text, command, color) in enumerate(buttons_data):
            btn = tk.Button(button_container, text=text,
                           font=('Segoe UI', 10, 'bold'),
                           bg=color,
                           fg='white',
                           relief='flat',
                           bd=0,
                           padx=20,
                           pady=10,
                           cursor='hand2',
                           state='disabled',
                           command=command)
            btn.pack(side=tk.LEFT, padx=8)
            self.action_buttons.append(btn)
            
            # Hover effects
            def on_enter(e, button=btn, hover_color=self.darken_color(color)):
                if button['state'] != 'disabled':
                    button.configure(bg=hover_color)
            def on_leave(e, button=btn, original_color=color):
                if button['state'] != 'disabled':
                    button.configure(bg=original_color)
            
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
    
    def darken_color(self, color):
        """Darken a hex color for hover effects"""
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        darkened = tuple(max(0, int(c * 0.8)) for c in rgb)
        return f"#{darkened[0]:02x}{darkened[1]:02x}{darkened[2]:02x}"
    
    def show_welcome(self):
        """Display modern welcome message"""
        welcome_text = """🌟 Welcome to Algorithm Challenge App!

🎯 MISSION
Master algorithmic thinking through interactive, engaging challenges that build your problem-solving skills step by step.

🚀 AVAILABLE CHALLENGES

🧩 Sudoku Solver
   • Practice logical deduction with classic 9x9 puzzles
   • Learn systematic elimination techniques
   • Build pattern recognition skills

🔢 Number Sequences  
   • Decode mathematical patterns and relationships
   • Master arithmetic, geometric, and special sequences
   • Strengthen analytical thinking

🔐 Caesar Cipher
   • Explore the foundations of cryptography
   • Learn systematic decoding techniques  
   • Understand historical encryption methods

💡 HOW TO GET STARTED

1️⃣ Choose a challenge from the cards above
2️⃣ Read the problem statement carefully
3️⃣ Enter your solution in the input area
4️⃣ Use hints when you need guidance
5️⃣ Check your answer and learn from explanations

🎖️ FEATURES
• Interactive problem solving with instant feedback
• Progressive difficulty levels
• Detailed hints and complete solutions
• Professional learning environment

Ready to challenge your mind? Select a challenge above to begin your algorithmic journey! 🚀"""
        
        self.problem_text.delete(1.0, tk.END)
        self.problem_text.insert(tk.END, welcome_text)
    
    def start_challenge(self, challenge):
        """Start a new challenge with visual feedback"""
        self.current_challenge = challenge
        self.new_problem()
        
        # Enable action buttons with visual feedback
        for btn in self.action_buttons:
            btn.config(state='normal')
        
        # Show success message
        self.show_status_message(f"🎯 {challenge.name} challenge started!", "success")
    
    def new_problem(self):
        """Generate a new problem with enhanced formatting"""
        if not self.current_challenge:
            return
        
        self.current_problem = self.current_challenge.generate_problem()
        self.problem_text.delete(1.0, tk.END)
        
        # Enhanced problem display
        header = f"🎯 CHALLENGE: {self.current_challenge.name}\n"
        header += f"📝 DESCRIPTION: {self.current_challenge.description}\n"
        header += "═" * 60 + "\n\n"
        
        self.problem_text.insert(tk.END, header)
        self.problem_text.insert(tk.END, self.current_problem)
        
        # Clear solution entry
        self.solution_entry.delete(1.0, tk.END)
        self.solution_entry.insert(tk.END, "Enter your solution here...")
        
        # Focus on solution entry
        self.solution_entry.focus_set()
    
    def check_solution(self):
        """Check solution with enhanced feedback"""
        if not self.current_challenge:
            return
        
        solution = self.solution_entry.get(1.0, tk.END).strip()
        if not solution or solution == "Enter your solution here...":
            self.show_status_message("⚠️ Please enter your solution first!", "warning")
            return
        
        if self.current_challenge.check_solution(solution):
            self.show_status_message("🎉 Excellent! Your solution is correct!", "success")
            self.current_challenge.completed = True
        else:
            self.show_status_message("❌ Not quite right. Try again or use a hint!", "error")
    
    def get_hint(self):
        """Show hint with modern dialog"""
        if not self.current_challenge:
            return
        
        hint = self.current_challenge.get_hint()
        self.show_modern_dialog("💡 Hint", hint, "info")
    
    def show_solution(self):
        """Show complete solution in modern window"""
        if not self.current_challenge:
            return
        
        solution = self.current_challenge.get_solution()
        
        # Create modern solution window
        solution_window = tk.Toplevel(self.root)
        solution_window.title(f"📖 Complete Solution - {self.current_challenge.name}")
        solution_window.geometry("700x500")
        solution_window.configure(bg=ModernStyle.COLORS['bg_primary'])
        solution_window.resizable(True, True)
        
        # Header
        header_frame = tk.Frame(solution_window, bg=ModernStyle.COLORS['bg_secondary'])
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        header_label = tk.Label(header_frame, 
                               text=f"📖 Complete Solution: {self.current_challenge.name}",
                               font=('Segoe UI', 16, 'bold'),
                               fg=ModernStyle.COLORS['text_primary'],
                               bg=ModernStyle.COLORS['bg_secondary'],
                               pady=15)
        header_label.pack()
        
        # Solution text
        solution_text = scrolledtext.ScrolledText(
            solution_window,
            font=('Consolas', 11),
            bg=ModernStyle.COLORS['card_bg'],
            fg=ModernStyle.COLORS['text_primary'],
            relief='flat',
            bd=0,
            padx=20,
            pady=20,
            wrap=tk.WORD,
            selectbackground=ModernStyle.COLORS['accent_primary'],
            insertbackground=ModernStyle.COLORS['text_primary']
        )
        solution_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        solution_text.insert(tk.END, solution)
        solution_text.config(state='disabled')
    
    def show_status_message(self, message, msg_type):
        """Show status message with appropriate styling"""
        colors = {
            'success': ModernStyle.COLORS['success'],
            'warning': ModernStyle.COLORS['warning'],
            'error': ModernStyle.COLORS['error'],
            'info': ModernStyle.COLORS['accent_secondary']
        }
        
        # Create status popup
        status_window = tk.Toplevel(self.root)
        status_window.title("Status")
        status_window.geometry("400x150")
        status_window.configure(bg=ModernStyle.COLORS['bg_primary'])
        status_window.resizable(False, False)
        
        # Center the window
        status_window.transient(self.root)
        status_window.grab_set()
        
        # Status content
        content_frame = tk.Frame(status_window, bg=colors.get(msg_type, ModernStyle.COLORS['accent_primary']))
        content_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        message_label = tk.Label(content_frame, text=message,
                                font=('Segoe UI', 12, 'bold'),
                                fg='white',
                                bg=colors.get(msg_type, ModernStyle.COLORS['accent_primary']),
                                wraplength=350,
                                justify=tk.CENTER)
        message_label.pack(expand=True, pady=20)
        
        # OK button
        ok_btn = tk.Button(content_frame, text="OK",
                          font=('Segoe UI', 10, 'bold'),
                          bg='white',
                          fg=colors.get(msg_type, ModernStyle.COLORS['accent_primary']),
                          relief='flat',
                          bd=0,
                          padx=20,
                          pady=5,
                          cursor='hand2',
                          command=status_window.destroy)
        ok_btn.pack(pady=(0, 20))
        
        # Auto-close after 3 seconds for success messages
        if msg_type == 'success':
            status_window.after(3000, status_window.destroy)
    
    def show_modern_dialog(self, title, message, dialog_type):
        """Show modern dialog with enhanced styling"""
        dialog_window = tk.Toplevel(self.root)
        dialog_window.title(title)
        dialog_window.geometry("500x300")
        dialog_window.configure(bg=ModernStyle.COLORS['bg_primary'])
        dialog_window.resizable(True, True)
        
        # Center the window
        dialog_window.transient(self.root)
        dialog_window.grab_set()
        
        # Header
        header_frame = tk.Frame(dialog_window, bg=ModernStyle.COLORS['bg_secondary'])
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        header_label = tk.Label(header_frame, text=title,
                               font=('Segoe UI', 16, 'bold'),
                               fg=ModernStyle.COLORS['text_primary'],
                               bg=ModernStyle.COLORS['bg_secondary'],
                               pady=15)
        header_label.pack()
        
        # Message content
        message_text = scrolledtext.ScrolledText(
            dialog_window,
            font=('Segoe UI', 11),
            bg=ModernStyle.COLORS['card_bg'],
            fg=ModernStyle.COLORS['text_primary'],
            relief='flat',
            bd=0,
            padx=20,
            pady=20,
            wrap=tk.WORD,
            selectbackground=ModernStyle.COLORS['accent_primary']
        )
        message_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        message_text.insert(tk.END, message)
        message_text.config(state='disabled')
        
        # Close button
        button_frame = tk.Frame(dialog_window, bg=ModernStyle.COLORS['bg_primary'])
        button_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        close_btn = tk.Button(button_frame, text="Close",
                             font=('Segoe UI', 10, 'bold'),
                             bg=ModernStyle.COLORS['accent_primary'],
                             fg='white',
                             relief='flat',
                             bd=0,
                             padx=20,
                             pady=8,
                             cursor='hand2',
                             command=dialog_window.destroy)
        close_btn.pack(side=tk.RIGHT)
    
    def run(self):
        """Start the application with modern styling"""
        # Set window icon (if available)
        try:
            self.root.iconname("Algorithm Challenge")
        except:
            pass
        
        # Center the main window
        self.center_window()
        
        # Start the main loop
        self.root.mainloop()
    
    def center_window(self):
        """Center the main window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

def main():
    """Main function to run the application"""
    try:
        app = AlgorithmChallengeApp()
        app.run()
    except Exception as e:
        print(f"Error starting application: {e}")
        messagebox.showerror("Error", f"Failed to start application: {e}")

if __name__ == "__main__":
    main()
    #            cursor='hand2',
    #                       command=status_window.destroy)
    #     ok_btn.pack(pady=(0, 20))
        
    #     # Auto-close after 3 seconds for success messages
    #     if msg_type == 'success':
    #         status_window.after(3000, status_window.destroy)
    
    # def show_modern_dialog(self, title, message, dialog_type):
    #     """Show modern dialog with enhanced styling"""
    #     dialog_window = tk.Toplevel(self.root)
    #     dialog_window.title(title)
    #     dialog_window.geometry("500x300")
    #     dialog_window.configure(bg=ModernStyle.COLORS['bg_primary'])
    #     dialog_window.resizable(True, True)
        
    #     # Center the window
    #     dialog_window.transient(self.root)
    #     dialog_window.grab_set()
        
    #     # Header
    #     header_frame = tk.Frame(dialog_window, bg=ModernStyle.COLORS['bg_secondary'])
    #     header_frame.pack(fill=tk.X, padx=10, pady=10)
        
    #     header_label = tk.Label(header_frame, text=title,
    #                            font=('Segoe UI', 16, 'bold'),
    #                            fg=ModernStyle.COLORS['text_primary'],
    #                            bg=ModernStyle.COLORS['bg_secondary'],
    #                            pady=15)
    #     header_label.pack()
        
    #     # Message content
    #     message_text = scrolledtext.ScrolledText(
    #         dialog_window,
    #         font=('Segoe UI', 11),
    #         bg=ModernStyle.COLORS['card_bg'],
    #         fg=ModernStyle.COLORS['text_primary'],
    #         relief='flat',
    #         bd=0,
    #         padx=20,
    #         pady=20,
    #         wrap=tk.WORD,
    #         selectbackground=ModernStyle.COLORS['accent_primary']
    #     )
    #     message_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
    #     message_text.insert(tk.END, message)
    #     message_text.config(state='disabled')
        
    #     # Close button
    #     button_frame = tk.Frame(dialog_window, bg=ModernStyle.COLORS['bg_primary'])
    #     button_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
    #     close_btn = tk.Button(button_frame, text="Close",
    #                          font=('Segoe UI', 10, 'bold'),
    #                          bg=ModernStyle.COLORS['accent_primary'],
    #                          fg='white',
    #                          relief='flat',
    #                          bd=0,
    #                          padx=20,
    #                          pady=8,
    #                          cursor='hand2',
    #                          command=dialog_window.destroy)
    #     close_btn.pack(side=tk.RIGHT)
    
    # def run(self):
    #     """Start the application with modern styling"""
    #     # Set window icon (if available)
    #     try:
    #         self.root.iconname("Algorithm Challenge")
    #     except:
    #         pass
        
    #     # Center the main window
    #     self.center_window()
        
    #     # Start the main loop
    #     self.root.mainloop()
    
    # def center_window(self):
    #     """Center the main window on screen"""
    #     self.root.update_idletasks()
    #     width = self.root.winfo_width()
    #     height = self.root.winfo_height()
    #     x = (self.root.winfo_screenwidth() // 2) - (width // 2)
    #     y = (self.root.winfo_screenheight() // 2) - (height // 2)
    #     self.root.geometry(f'{width}x{height}+{x}+{y}')























#     <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>Problem Solving Hub</title>
#     <style>
#         * {
#             margin: 0;
#             padding: 0;
#             box-sizing: border-box;
#         }

#         body {
#             font-family: 'Arial', sans-serif;
#             background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#             min-height: 100vh;
#             color: #333;
#         }

#         .container {
#             max-width: 1200px;
#             margin: 0 auto;
#             padding: 20px;
#             min-height: 100vh;
#             display: flex;
#             flex-direction: column;
#         }

#         .header {
#             text-align: center;
#             color: white;
#             margin-bottom: 30px;
#         }

#         .header h1 {
#             font-size: 3rem;
#             margin-bottom: 10px;
#             text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
#         }

#         .header p {
#             font-size: 1.2rem;
#             opacity: 0.9;
#         }

#         .main-content {
#             display: flex;
#             gap: 30px;
#             flex: 1;
#             align-items: stretch;
#         }

#         /* Challenge Selection Section - Made Smaller */
#         .challenge-section {
#             flex: 0 0 300px; /* Fixed smaller width */
#             background: rgba(255, 255, 255, 0.95);
#             border-radius: 15px;
#             padding: 20px;
#             box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
#             backdrop-filter: blur(10px);
#         }

#         .challenge-section h2 {
#             color: #4a5568;
#             margin-bottom: 15px;
#             font-size: 1.3rem;
#             text-align: center;
#         }

#         .challenge-grid {
#             display: grid;
#             grid-template-columns: 1fr;
#             gap: 10px;
#         }

#         .challenge-card {
#             background: linear-gradient(135deg, #ff6b6b, #feca57);
#             border: none;
#             border-radius: 10px;
#             padding: 15px;
#             color: white;
#             cursor: pointer;
#             transition: all 0.3s ease;
#             text-align: center;
#             font-weight: bold;
#             font-size: 0.9rem;
#         }

#         .challenge-card:hover {
#             transform: translateY(-2px);
#             box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
#         }

#         .challenge-card.active {
#             background: linear-gradient(135deg, #667eea, #764ba2);
#             transform: scale(1.02);
#         }

#         /* Problem Statement Section - Made Larger */
#         .problem-section {
#             flex: 1; /* Takes remaining space */
#             background: rgba(255, 255, 255, 0.95);
#             border-radius: 15px;
#             padding: 40px;
#             box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
#             backdrop-filter: blur(10px);
#             display: flex;
#             flex-direction: column;
#         }

#         .problem-section h2 {
#             color: #4a5568;
#             margin-bottom: 25px;
#             font-size: 2rem;
#             text-align: center;
#             border-bottom: 3px solid #667eea;
#             padding-bottom: 15px;
#         }

#         .problem-content {
#             flex: 1;
#             display: flex;
#             flex-direction: column;
#         }

#         .problem-display {
#             background: #f8f9fa;
#             border-radius: 12px;
#             padding: 30px;
#             margin-bottom: 25px;
#             border-left: 5px solid #667eea;
#             min-height: 200px;
#             flex: 1;
#         }

#         .problem-title {
#             font-size: 1.5rem;
#             font-weight: bold;
#             color: #2d3748;
#             margin-bottom: 15px;
#         }

#         .problem-description {
#             font-size: 1.1rem;
#             line-height: 1.6;
#             color: #4a5568;
#             margin-bottom: 20px;
#         }

#         .problem-details {
#             background: white;
#             border-radius: 8px;
#             padding: 20px;
#             margin-top: 15px;
#         }

#         .detail-item {
#             margin-bottom: 12px;
#             padding: 8px 0;
#             border-bottom: 1px solid #e2e8f0;
#         }

#         .detail-label {
#             font-weight: bold;
#             color: #667eea;
#             display: inline-block;
#             width: 120px;
#         }

#         .solution-area {
#             background: #e6fffa;
#             border-radius: 12px;
#             padding: 25px;
#             border: 2px dashed #38b2ac;
#         }

#         .solution-area h3 {
#             color: #38b2ac;
#             margin-bottom: 15px;
#             font-size: 1.3rem;
#         }

#         .solution-input {
#             width: 100%;
#             min-height: 120px;
#             border: 2px solid #e2e8f0;
#             border-radius: 8px;
#             padding: 15px;
#             font-size: 1rem;
#             resize: vertical;
#             transition: border-color 0.3s ease;
#         }

#         .solution-input:focus {
#             outline: none;
#             border-color: #667eea;
#             box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
#         }

#         .action-buttons {
#             display: flex;
#             gap: 15px;
#             margin-top: 20px;
#             justify-content: center;
#         }

#         .btn {
#             padding: 12px 25px;
#             border: none;
#             border-radius: 8px;
#             cursor: pointer;
#             font-weight: bold;
#             transition: all 0.3s ease;
#             font-size: 1rem;
#         }

#         .btn-primary {
#             background: linear-gradient(135deg, #667eea, #764ba2);
#             color: white;
#         }

#         .btn-secondary {
#             background: linear-gradient(135deg, #ffecd2, #fcb69f);
#             color: #8b4513;
#         }

#         .btn:hover {
#             transform: translateY(-2px);
#             box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
#         }

#         .empty-state {
#             text-align: center;
#             color: #718096;
#             font-size: 1.1rem;
#             padding: 60px 20px;
#         }

#         .empty-state i {
#             font-size: 4rem;
#             margin-bottom: 20px;
#             opacity: 0.5;
#         }

#         @media (max-width: 768px) {
#             .main-content {
#                 flex-direction: column;
#             }
            
#             .challenge-section {
#                 flex: none;
#                 order: 2;
#             }
            
#             .problem-section {
#                 order: 1;
#                 margin-bottom: 20px;
#             }
#         }
#     </style>
# </head>
# <body>
#     <div class="container">
#         <div class="header">
#             <h1>🧠 Problem Solving Hub</h1>
#             <p>Choose a challenge and develop your solution</p>
#         </div>

#         <div class="main-content">
#             <!-- Smaller Challenge Selection Section -->
#             <div class="challenge-section">
#                 <h2>📋 Choose Challenge</h2>
#                 <div class="challenge-grid">
#                     <button class="challenge-card" onclick="selectChallenge('algorithm')">
#                         🔢 Algorithm Problem
#                     </button>
#                     <button class="challenge-card" onclick="selectChallenge('design')">
#                         🎨 Design Challenge
#                     </button>
#                     <button class="challenge-card" onclick="selectChallenge('business')">
#                         💼 Business Case
#                     </button>
#                     <button class="challenge-card" onclick="selectChallenge('technical')">
#                         ⚙️ Technical Issue
#                     </button>
#                     <button class="challenge-card" onclick="selectChallenge('creative')">
#                         💡 Creative Problem
#                     </button>
#                     <button class="challenge-card" onclick="selectChallenge('logic')">
#                         🧩 Logic Puzzle
#                     </button>
#                 </div>
#             </div>

#             <!-- Larger Problem Statement Section -->
#             <div class="problem-section">
#                 <h2>📝 Problem Statement & Solution</h2>
#                 <div class="problem-content">
#                     <div class="problem-display" id="problemDisplay">
#                         <div class="empty-state">
#                             <div style="font-size: 4rem; margin-bottom: 20px;">🎯</div>
#                             <p>Select a challenge from the left to see the problem statement</p>
#                         </div>
#                     </div>
                    
#                     <div class="solution-area" id="solutionArea" style="display: none;">
#                         <h3>💭 Your Solution</h3>
#                         <textarea 
#                             class="solution-input" 
#                             id="solutionInput"
#                             placeholder="Write your solution approach here...
                            
# • Break down the problem
# • List your assumptions  
# • Outline your strategy
# • Describe implementation steps
# • Consider edge cases and alternatives"
#                         ></textarea>
#                         <div class="action-buttons">
#                             <button class="btn btn-primary" onclick="submitSolution()">
#                                 ✅ Submit Solution
#                             </button>
#                             <button class="btn btn-secondary" onclick="clearSolution()">
#                                 🔄 Clear & Restart
#                             </button>
#                         </div>
#                     </div>
#                 </div>
#             </div>
#         </div>
#     </div>

#     <script>
#         const problems = {
#             algorithm: {
#                 title: "Two Sum Algorithm",
#                 description: "Given an array of integers and a target sum, find two numbers in the array that add up to the target. Return their indices.",
#                 details: {
#                     "Difficulty": "Medium",
#                     "Time Limit": "30 minutes",
#                     "Input": "Array: [2, 7, 11, 15], Target: 9",
#                     "Expected Output": "[0, 1] (because 2 + 7 = 9)",
#                     "Constraints": "Each input has exactly one solution"
#                 }
#             },
#             design: {
#                 title: "Mobile App Navigation Design",
#                 description: "Design an intuitive navigation system for a food delivery app that needs to handle 5 main sections: Home, Search, Orders, Profile, and Cart.",
#                 details: {
#                     "Difficulty": "Medium",
#                     "Time Limit": "45 minutes",
#                     "Users": "Busy professionals, students",
#                     "Key Requirements": "One-handed usage, quick access to cart",
#                     "Constraints": "Mobile-first, accessibility compliant"
#                 }
#             },
#             business: {
#                 title: "Customer Retention Strategy",
#                 description: "A SaaS company is losing 25% of customers after their first month. Develop a comprehensive strategy to improve first-month retention to 90%.",
#                 details: {
#                     "Difficulty": "Hard",
#                     "Time Limit": "60 minutes",
#                     "Current Metrics": "75% first-month retention",
#                     "Budget": "$50K for implementation",
#                     "Target": "90% retention rate"
#                 }
#             },
#             technical: {
#                 title: "Database Performance Optimization",
#                 description: "A web application's database queries are taking 5+ seconds to load user dashboards. The database has 1M+ user records and 10M+ transaction records.",
#                 details: {
#                     "Difficulty": "Hard",
#                     "Time Limit": "45 minutes",
#                     "Current Performance": "5+ seconds load time",
#                     "Database Size": "1M users, 10M transactions",
#                     "Target": "Under 500ms load time"
#                 }
#             },
#             creative: {
#                 title: "Sustainable Packaging Innovation",
#                 description: "Design an eco-friendly packaging solution for online clothing retailers that protects items during shipping while being completely biodegradable.",
#                 details: {
#                     "Difficulty": "Medium",
#                     "Time Limit": "45 minutes",
#                     "Requirements": "100% biodegradable materials",
#                     "Constraints": "Cost-effective, protective",
#                     "Target Market": "Online fashion retailers"
#                 }
#             },
#             logic: {
#                 title: "The Bridge Crossing Puzzle",
#                 description: "Four people need to cross a bridge at night with only one flashlight. The bridge can hold only two people at once. They walk at different speeds: 1, 2, 5, and 10 minutes. How can all four cross in 17 minutes?",
#                 details: {
#                     "Difficulty": "Medium",
#                     "Time Limit": "20 minutes",
#                     "People": "A(1min), B(2min), C(5min), D(10min)",
#                     "Constraints": "Bridge holds max 2 people, need flashlight",
#                     "Target": "All cross in exactly 17 minutes"
#                 }
#             }
#         };

#         function selectChallenge(type) {
#             // Remove active class from all cards
#             document.querySelectorAll('.challenge-card').forEach(card => {
#                 card.classList.remove('active');
#             });
            
#             // Add active class to selected card
#             event.target.classList.add('active');
            
#             // Display problem
#             const problem = problems[type];
#             const problemDisplay = document.getElementById('problemDisplay');
#             const solutionArea = document.getElementById('solutionArea');
            
#             problemDisplay.innerHTML = `
#                 <div class="problem-title">${problem.title}</div>
#                 <div class="problem-description">${problem.description}</div>
#                 <div class="problem-details">
#                     ${Object.entries(problem.details).map(([key, value]) => `
#                         <div class="detail-item">
#                             <span class="detail-label">${key}:</span>
#                             <span>${value}</span>
#                         </div>
#                     `).join('')}
#                 </div>
#             `;
            
#             solutionArea.style.display = 'block';
#             document.getElementById('solutionInput').value = '';
#         }

#         function submitSolution() {
#             const solution = document.getElementById('solutionInput').value.trim();
#             if (!solution) {
#                 alert('Please write your solution before submitting!');
#                 return;
#             }
            
#             alert('Solution submitted successfully! 🎉\n\nGreat work on tackling this problem. In a real scenario, this would be reviewed by mentors or peers.');
#         }

#         function clearSolution() {
#             document.getElementById('solutionInput').value = '';
#             document.getElementById('solutionInput').focus();
#         }
#     </script>
# </body>
# </html>