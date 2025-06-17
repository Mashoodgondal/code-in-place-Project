import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random
import string
import math

class AlgorithmChallengeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Algorithm Challenge Hub")
        self.root.geometry("1200x800")
        self.root.configure(bg="#0f172a")
        
        self.colors = {
            'primary': '#3b82f6',
            'secondary': '#8b5cf6',
            'accent': '#06d6a0',
            'warning': '#f59e0b',
            'danger': '#ef4444',
            'dark': '#0f172a',
            'darker': '#020617',
            'light': '#f1f5f9',
            'gray': '#64748b',
            'card': '#1e293b'
        }
        
        self.setup_styles()
        self.create_main_interface()
        
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('Custom.TButton',
                       background=self.colors['primary'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       font=('Arial', 11, 'bold'))
        
        style.map('Custom.TButton',
                 background=[('active', '#2563eb')])
        
        style.configure('Secondary.TButton',
                       background=self.colors['secondary'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       font=('Arial', 10))
        
        style.map('Secondary.TButton',
                 background=[('active', '#7c3aed')])
        
        style.configure('Success.TButton',
                       background=self.colors['accent'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       font=('Arial', 10))
        
        style.map('Success.TButton',
                 background=[('active', '#059669')])
    
    def create_main_interface(self):
        main_container = tk.Frame(self.root, bg=self.colors['dark'])
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        header_frame = tk.Frame(main_container, bg=self.colors['dark'], height=80)
        header_frame.pack(fill='x', pady=(0, 20))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, 
                              text="Algorithm Challenge Hub",
                              font=('Arial', 28, 'bold'),
                              fg=self.colors['light'],
                              bg=self.colors['dark'])
        title_label.pack(side='left', pady=20)
        
        subtitle_label = tk.Label(header_frame,
                                 text="Master algorithms through interactive puzzles",
                                 font=('Arial', 14),
                                 fg=self.colors['gray'],
                                 bg=self.colors['dark'])
        subtitle_label.pack(side='left', padx=(20, 0), pady=20)
        
        content_frame = tk.Frame(main_container, bg=self.colors['dark'])
        content_frame.pack(fill='both', expand=True)
        
        canvas = tk.Canvas(content_frame, bg=self.colors['dark'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg=self.colors['dark'])
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        self.create_challenge_cards()
    
    def create_challenge_cards(self):
        challenges = [
            {
                'title': 'Sudoku Solver',
                'description': 'Solve 9x9 Sudoku puzzles using backtracking algorithm',
                'color': self.colors['primary'],
                'action': self.open_sudoku
            },
            {
                'title': 'Number Sequence Predictor',
                'description': 'Identify patterns in mathematical sequences',
                'color': self.colors['secondary'],
                'action': self.open_sequence_predictor
            },
            {
                'title': 'Caesar Cipher Decoder',
                'description': 'Decode encrypted messages using classical cryptography',
                'color': self.colors['accent'],
                'action': self.open_caesar_cipher
            },
            {
                'title': 'Sorting Algorithm Visualizer',
                'description': 'Learn sorting algorithms through visual demonstrations',
                'color': self.colors['warning'],
                'action': self.open_sorting_visualizer
            },
            {
                'title': 'Prime Number Generator',
                'description': 'Generate prime numbers using the Sieve of Eratosthenes',
                'color': self.colors['danger'],
                'action': self.open_prime_generator
            }
        ]
        
        for i, challenge in enumerate(challenges):
            row = i // 2
            col = i % 2
            
            card_frame = tk.Frame(self.scrollable_frame, 
                                 bg=self.colors['card'],
                                 relief='flat',
                                 bd=2)
            card_frame.grid(row=row, column=col, padx=15, pady=15, sticky='ew')
            
            self.scrollable_frame.grid_columnconfigure(col, weight=1)
            
            title_frame = tk.Frame(card_frame, bg=challenge['color'], height=60)
            title_frame.pack(fill='x')
            title_frame.pack_propagate(False)
            
            title_label = tk.Label(title_frame,
                                  text=challenge['title'],
                                  font=('Arial', 16, 'bold'),
                                  fg='white',
                                  bg=challenge['color'])
            title_label.pack(pady=15)
            
            content_frame = tk.Frame(card_frame, bg=self.colors['card'])
            content_frame.pack(fill='both', expand=True, padx=20, pady=20)
            
            desc_label = tk.Label(content_frame,
                                 text=challenge['description'],
                                 font=('Arial', 12),
                                 fg=self.colors['light'],
                                 bg=self.colors['card'],
                                 wraplength=300,
                                 justify='left')
            desc_label.pack(pady=(0, 15))
            
            launch_btn = ttk.Button(content_frame,
                                   text="Launch Challenge",
                                   style='Custom.TButton',
                                   command=challenge['action'])
            launch_btn.pack()
    
    def open_sudoku(self):
        sudoku_window = tk.Toplevel(self.root)
        sudoku_window.title("Sudoku Solver Challenge")
        sudoku_window.geometry("600x700")
        sudoku_window.configure(bg=self.colors['dark'])
        
        header = tk.Label(sudoku_window,
                         text="Sudoku Solver",
                         font=('Arial', 20, 'bold'),
                         fg=self.colors['light'],
                         bg=self.colors['dark'])
        header.pack(pady=20)
        
        grid_frame = tk.Frame(sudoku_window, bg=self.colors['dark'])
        grid_frame.pack(pady=20)
        
        self.sudoku_entries = []
        for i in range(9):
            row = []
            for j in range(9):
                entry = tk.Entry(grid_frame, width=3, justify='center',
                               font=('Arial', 14, 'bold'),
                               bg=self.colors['light'],
                               fg=self.colors['dark'])
                entry.grid(row=i, column=j, padx=1, pady=1)
                row.append(entry)
            self.sudoku_entries.append(row)
        
        button_frame = tk.Frame(sudoku_window, bg=self.colors['dark'])
        button_frame.pack(pady=20)
        
        generate_btn = ttk.Button(button_frame,
                                 text="Generate Puzzle",
                                 style='Secondary.TButton',
                                 command=self.generate_sudoku_puzzle)
        generate_btn.pack(side='left', padx=10)
        
        solve_btn = ttk.Button(button_frame,
                              text="Solve Puzzle",
                              style='Success.TButton',
                              command=self.solve_sudoku_puzzle)
        solve_btn.pack(side='left', padx=10)
        
        clear_btn = ttk.Button(button_frame,
                              text="Clear Grid",
                              style='Custom.TButton',
                              command=self.clear_sudoku_grid)
        clear_btn.pack(side='left', padx=10)
        
        info_text = tk.Text(sudoku_window, height=8, width=70,
                           bg=self.colors['card'],
                           fg=self.colors['light'],
                           font=('Arial', 10))
        info_text.pack(pady=20, padx=20)
        info_text.insert('1.0', 
            "How to use Sudoku Solver:\n\n"
            "1. Click 'Generate Puzzle' to create a random Sudoku puzzle\n"
            "2. Fill in numbers 1-9 in empty cells\n"
            "3. Each row, column, and 3x3 box must contain all digits 1-9\n"
            "4. Click 'Solve Puzzle' to see the solution using backtracking algorithm\n"
            "5. Use 'Clear Grid' to start fresh\n\n"
            "The backtracking algorithm tries each number and backtracks when it hits a dead end.")
        info_text.config(state='disabled')
    
    def generate_sudoku_puzzle(self):
        puzzle = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]
        
        for i in range(9):
            for j in range(9):
                self.sudoku_entries[i][j].delete(0, 'end')
                if puzzle[i][j] != 0:
                    self.sudoku_entries[i][j].insert(0, str(puzzle[i][j]))
    
    def solve_sudoku_puzzle(self):
        grid = []
        for i in range(9):
            row = []
            for j in range(9):
                val = self.sudoku_entries[i][j].get()
                if val == '':
                    row.append(0)
                else:
                    try:
                        row.append(int(val))
                    except ValueError:
                        row.append(0)
            grid.append(row)
        
        if self.solve_sudoku(grid):
            for i in range(9):
                for j in range(9):
                    self.sudoku_entries[i][j].delete(0, 'end')
                    self.sudoku_entries[i][j].insert(0, str(grid[i][j]))
        else:
            messagebox.showerror("Error", "No solution exists for this puzzle!")
    
    def solve_sudoku(self, grid):
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    for num in range(1, 10):
                        if self.is_valid_sudoku(grid, i, j, num):
                            grid[i][j] = num
                            if self.solve_sudoku(grid):
                                return True
                            grid[i][j] = 0
                    return False
        return True
    
    def is_valid_sudoku(self, grid, row, col, num):
        for j in range(9):
            if grid[row][j] == num:
                return False
        
        for i in range(9):
            if grid[i][col] == num:
                return False
        
        start_row = row - row % 3
        start_col = col - col % 3
        for i in range(3):
            for j in range(3):
                if grid[i + start_row][j + start_col] == num:
                    return False
        
        return True
    
    def clear_sudoku_grid(self):
        for i in range(9):
            for j in range(9):
                self.sudoku_entries[i][j].delete(0, 'end')
    
    def open_sequence_predictor(self):
        seq_window = tk.Toplevel(self.root)
        seq_window.title("Number Sequence Predictor")
        seq_window.geometry("700x600")
        seq_window.configure(bg=self.colors['dark'])
        
        header = tk.Label(seq_window,
                         text="Number Sequence Predictor",
                         font=('Arial', 20, 'bold'),
                         fg=self.colors['light'],
                         bg=self.colors['dark'])
        header.pack(pady=20)
        
        input_frame = tk.Frame(seq_window, bg=self.colors['dark'])
        input_frame.pack(pady=20)
        
        tk.Label(input_frame,
                text="Enter sequence (comma-separated):",
                font=('Arial', 12),
                fg=self.colors['light'],
                bg=self.colors['dark']).pack()
        
        self.sequence_entry = tk.Entry(input_frame, width=50,
                                      font=('Arial', 12),
                                      bg=self.colors['light'])
        self.sequence_entry.pack(pady=10)
        
        button_frame = tk.Frame(seq_window, bg=self.colors['dark'])
        button_frame.pack(pady=10)
        
        analyze_btn = ttk.Button(button_frame,
                               text="Analyze Sequence",
                               style='Custom.TButton',
                               command=self.analyze_sequence)
        analyze_btn.pack(side='left', padx=10)
        
        generate_btn = ttk.Button(button_frame,
                                text="Generate Example",
                                style='Secondary.TButton',
                                command=self.generate_example_sequence)
        generate_btn.pack(side='left', padx=10)
        
        self.sequence_result = scrolledtext.ScrolledText(seq_window,
                                                        height=15, width=80,
                                                        bg=self.colors['card'],
                                                        fg=self.colors['light'],
                                                        font=('Arial', 10))
        self.sequence_result.pack(pady=20, padx=20, fill='both', expand=True)
        
        self.sequence_result.insert('1.0',
            "Number Sequence Analysis:\n\n"
            "This tool analyzes mathematical sequences and predicts the next numbers.\n"
            "Try these examples:\n"
            "• Arithmetic: 2, 4, 6, 8, 10\n"
            "• Geometric: 1, 2, 4, 8, 16\n"
            "• Fibonacci: 1, 1, 2, 3, 5, 8\n"
            "• Squares: 1, 4, 9, 16, 25\n"
            "• Prime: 2, 3, 5, 7, 11\n\n"
            "Click 'Generate Example' for random sequences to practice with!")
    
    def analyze_sequence(self):
        try:
            sequence_str = self.sequence_entry.get()
            sequence = [int(x.strip()) for x in sequence_str.split(',')]
            
            if len(sequence) < 3:
                messagebox.showerror("Error", "Please enter at least 3 numbers!")
                return
            
            analysis = self.detect_sequence_pattern(sequence)
            
            self.sequence_result.delete('1.0', 'end')
            self.sequence_result.insert('1.0', analysis)
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers separated by commas!")
    
    def detect_sequence_pattern(self, seq):
        result = f"Sequence Analysis for: {', '.join(map(str, seq))}\n\n"
        
        differences = [seq[i+1] - seq[i] for i in range(len(seq)-1)]
        result += f"First differences: {', '.join(map(str, differences))}\n"
        
        if all(d == differences[0] for d in differences):
            result += f"Pattern: Arithmetic sequence with common difference {differences[0]}\n"
            next_val = seq[-1] + differences[0]
            result += f"Next number: {next_val}\n"
            result += f"Formula: a(n) = {seq[0]} + {differences[0]}*(n-1)\n\n"
        
        ratios = []
        geometric = True
        for i in range(1, len(seq)):
            if seq[i-1] != 0:
                ratios.append(seq[i] / seq[i-1])
            else:
                geometric = False
                break
        
        if geometric and len(ratios) > 0 and all(abs(r - ratios[0]) < 0.001 for r in ratios):
            result += f"Pattern: Geometric sequence with ratio {ratios[0]:.2f}\n"
            next_val = int(seq[-1] * ratios[0])
            result += f"Next number: {next_val}\n\n"
        
        if len(seq) >= 3:
            is_fibonacci = True
            for i in range(2, len(seq)):
                if seq[i] != seq[i-1] + seq[i-2]:
                    is_fibonacci = False
                    break
            
            if is_fibonacci:
                result += "Pattern: Fibonacci sequence\n"
                next_val = seq[-1] + seq[-2]
                result += f"Next number: {next_val}\n\n"
        
        squares = [i*i for i in range(1, len(seq)+1)]
        if seq == squares:
            result += "Pattern: Perfect squares\n"
            next_val = (len(seq)+1)**2
            result += f"Next number: {next_val}\n\n"
        
        if len(differences) > 1:
            second_differences = [differences[i+1] - differences[i] for i in range(len(differences)-1)]
            result += f"Second differences: {', '.join(map(str, second_differences))}\n"
            
            if all(d == second_differences[0] for d in second_differences):
                result += "Pattern: Quadratic sequence (constant second differences)\n"
        
        result += "\nAlgorithm used: Pattern recognition through difference analysis"
        return result
    
    def generate_example_sequence(self):
        patterns = [
            ([2, 5, 8, 11, 14], "Arithmetic sequence"),
            ([3, 6, 12, 24, 48], "Geometric sequence"),
            ([1, 1, 2, 3, 5, 8], "Fibonacci sequence"),
            ([1, 4, 9, 16, 25], "Perfect squares"),
            ([2, 3, 5, 7, 11], "Prime numbers")
        ]
        
        sequence, description = random.choice(patterns)
        self.sequence_entry.delete(0, 'end')
        self.sequence_entry.insert(0, ', '.join(map(str, sequence)))
        
        self.sequence_result.delete('1.0', 'end')
        self.sequence_result.insert('1.0', f"Example sequence generated: {description}\n\n"
                                   f"Sequence: {', '.join(map(str, sequence))}\n\n"
                                   "Click 'Analyze Sequence' to see the pattern analysis!")
    
    def open_caesar_cipher(self):
        cipher_window = tk.Toplevel(self.root)
        cipher_window.title("Caesar Cipher Decoder")
        cipher_window.geometry("800x650")
        cipher_window.configure(bg=self.colors['dark'])
        
        header = tk.Label(cipher_window,
                         text="Caesar Cipher Decoder",
                         font=('Arial', 20, 'bold'),
                         fg=self.colors['light'],
                         bg=self.colors['dark'])
        header.pack(pady=20)
        
        input_frame = tk.Frame(cipher_window, bg=self.colors['dark'])
        input_frame.pack(pady=10, padx=20, fill='x')
        
        tk.Label(input_frame,
                text="Enter text to encrypt/decrypt:",
                font=('Arial', 12),
                fg=self.colors['light'],
                bg=self.colors['dark']).pack(anchor='w')
        
        self.cipher_input = tk.Text(input_frame, height=4, width=80,
                                   bg=self.colors['light'],
                                   fg=self.colors['dark'],
                                   font=('Arial', 11))
        self.cipher_input.pack(pady=5, fill='x')
        
        shift_frame = tk.Frame(cipher_window, bg=self.colors['dark'])
        shift_frame.pack(pady=10)
        
        tk.Label(shift_frame,
                text="Shift value:",
                font=('Arial', 12),
                fg=self.colors['light'],
                bg=self.colors['dark']).pack(side='left')
        
        self.shift_var = tk.StringVar(value="3")
        shift_spinbox = tk.Spinbox(shift_frame, from_=1, to=25,
                                  textvariable=self.shift_var,
                                  width=5, font=('Arial', 11))
        shift_spinbox.pack(side='left', padx=10)
        
        button_frame = tk.Frame(cipher_window, bg=self.colors['dark'])
        button_frame.pack(pady=15)
        
        encrypt_btn = ttk.Button(button_frame,
                               text="Encrypt",
                               style='Custom.TButton',
                               command=lambda: self.caesar_cipher_operation(True))
        encrypt_btn.pack(side='left', padx=10)
        
        decrypt_btn = ttk.Button(button_frame,
                               text="Decrypt",
                               style='Secondary.TButton',
                               command=lambda: self.caesar_cipher_operation(False))
        decrypt_btn.pack(side='left', padx=10)
        
        brute_force_btn = ttk.Button(button_frame,
                                   text="Brute Force Decode",
                                   style='Success.TButton',
                                   command=self.brute_force_decode)
        brute_force_btn.pack(side='left', padx=10)
        
        result_frame = tk.Frame(cipher_window, bg=self.colors['dark'])
        result_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        tk.Label(result_frame,
                text="Result:",
                font=('Arial', 12, 'bold'),
                fg=self.colors['light'],
                bg=self.colors['dark']).pack(anchor='w')
        
        self.cipher_result = scrolledtext.ScrolledText(result_frame,
                                                      height=12, width=80,
                                                      bg=self.colors['card'],
                                                      fg=self.colors['light'],
                                                      font=('Arial', 11))
        self.cipher_result.pack(fill='both', expand=True)
        
        self.cipher_result.insert('1.0',
            "Caesar Cipher Information:\n\n"
            "The Caesar cipher shifts each letter by a fixed number of positions.\n"
            "For example, with shift 3: A→D, B→E, C→F, etc.\n\n"
            "Usage:\n"
            "1. Enter your text above\n"
            "2. Set the shift value (1-25)\n"
            "3. Click Encrypt or Decrypt\n"
            "4. Use Brute Force Decode to try all possible shifts\n\n"
            "Try encrypting: 'HELLO WORLD' with shift 3")
    
    def caesar_cipher_operation(self, encrypt=True):
        try:
            text = self.cipher_input.get('1.0', 'end-1c').strip().upper()
            shift = int(self.shift_var.get())
            
            if not encrypt:
                shift = -shift
            
            result = self.caesar_cipher(text, shift)
            
            operation = "Encryption" if encrypt else "Decryption"
            self.cipher_result.delete('1.0', 'end')
            self.cipher_result.insert('1.0',
                f"{operation} Result (Shift: {abs(int(self.shift_var.get()))}):\n\n"
                f"Original: {text}\n"
                f"Result: {result}\n\n"
                f"Algorithm: Each letter is shifted {abs(shift)} positions in the alphabet.")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid shift value!")
    
    def caesar_cipher(self, text, shift):
        result = ""
        for char in text:
            if char.isalpha():
                ascii_offset = ord('A')
                shifted = (ord(char) - ascii_offset + shift) % 26
                result += chr(shifted + ascii_offset)
            else:
                result += char
        return result
    
    def brute_force_decode(self):
        text = self.cipher_input.get('1.0', 'end-1c').strip().upper()
        
        if not text:
            messagebox.showerror("Error", "Please enter text to decode!")
            return
        
        self.cipher_result.delete('1.0', 'end')
        self.cipher_result.insert('1.0', "Brute Force Decoding - All Possible Shifts:\n\n")
        
        for shift in range(1, 26):
            decoded = self.caesar_cipher(text, -shift)
            self.cipher_result.insert('end', f"Shift {shift:2d}: {decoded}\n")
        
        self.cipher_result.insert('end', 
            "\nLook for the shift that produces readable English text!")
    
    def open_sorting_visualizer(self):
        sort_window = tk.Toplevel(self.root)
        sort_window.title("Sorting Algorithm Visualizer")
        sort_window.geometry("900x700")
        sort_window.configure(bg=self.colors['dark'])
        
        header = tk.Label(sort_window,
                         text="Sorting Algorithm Visualizer",
                         font=('Arial', 20, 'bold'),
                         fg=self.colors['light'],
                         bg=self.colors['dark'])
        header.pack(pady=20)
        
        control_frame = tk.Frame(sort_window, bg=self.colors['dark'])
        control_frame.pack(pady=10)
        
        self.sort_algorithm = tk.StringVar(value="Bubble Sort")
        algorithm_menu = ttk.Combobox(control_frame,
                                    textvariable=self.sort_algorithm,
                                    values=["Bubble Sort", "Selection Sort", "Insertion Sort"],
                                    state="readonly")
        algorithm_menu.pack(side='left', padx=10)
        
        generate_btn = ttk.Button(control_frame,
                                text="Generate Array",
                                style='Secondary.TButton',
                                command=self.generate_sort_array)
        generate_btn.pack(side='left', padx=10)
        
        sort_btn = ttk.Button(control_frame,
                            text="Sort Array",
                            style='Custom.TButton',
                            command=self.sort_array)
        sort_btn.pack(side='left', padx=10)
        
        self.sort_canvas = tk.Canvas(sort_window, width=800, height=300,
                                   bg=self.colors['card'],
                                   highlightthickness=0)
        self.sort_canvas.pack(pady=20)
        
        self.sort_info.delete('1.0', 'end')
        # self.sort_info.insert('1.0',
        #     f"Algorithm: {self.sort_algorithm.get()}\n\n"
        #     algorithm_info.get(self.sort_algorithm.get(), '') + "\n\n"
        #     f"Generated array: {self.sort_array}\n\n"
        #     "Click 'Sort Array' to see the algorithm in action!")
        self.sort_info.insert('1.0',
          f"Algorithm: {self.sort_algorithm.get()}\n\n" +
          algorithm_info.get(self.sort_algorithm.get(), '') + "\n\n" +
          f"Generated array: {self.sort_array}\n\n" +
          "Click 'Sort Array' to see the algorithm in action!")

    def draw_array(self):
        self.sort_canvas.delete("all")
        canvas_width = 800
        canvas_height = 300
        bar_width = canvas_width // len(self.sort_array)
        
        for i, value in enumerate(self.sort_array):
            x1 = i * bar_width
            y1 = canvas_height - value
            x2 = x1 + bar_width - 2
            y2 = canvas_height
            
            color = self.colors['primary'] if i % 2 == 0 else self.colors['secondary']
            self.sort_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='white')
            self.sort_canvas.create_text(x1 + bar_width//2, y2 - 10, 
                                       text=str(value), fill='white', font=('Arial', 8))
    
    def sort_array(self):
        algorithm = self.sort_algorithm.get()
        original_array = self.sort_array.copy()
        
        if algorithm == "Bubble Sort":
            steps = self.bubble_sort_steps()
        elif algorithm == "Selection Sort":
            steps = self.selection_sort_steps()
        else:
            steps = self.insertion_sort_steps()
        
        self.sort_info.delete('1.0', 'end')
        self.sort_info.insert('1.0',
            f"Sorting with {algorithm}:\n\n"
            f"Original array: {original_array}\n"
            f"Sorted array: {self.sort_array}\n\n"
            f"Steps performed: {len(steps)}\n"
            f"Comparisons and swaps:\n\n")
        
        for i, step in enumerate(steps[:20]):
            self.sort_info.insert('end', f"Step {i+1}: {step}\n")
        
        if len(steps) > 20:
            self.sort_info.insert('end', f"... and {len(steps) - 20} more steps\n")
        
        self.draw_array()
    
    def bubble_sort_steps(self):
        steps = []
        n = len(self.sort_array)
        
        for i in range(n):
            for j in range(0, n - i - 1):
                steps.append(f"Compare {self.sort_array[j]} and {self.sort_array[j+1]}")
                if self.sort_array[j] > self.sort_array[j + 1]:
                    self.sort_array[j], self.sort_array[j + 1] = self.sort_array[j + 1], self.sort_array[j]
                    steps.append(f"Swap {self.sort_array[j+1]} and {self.sort_array[j]}")
        
        return steps
    
    def selection_sort_steps(self):
        steps = []
        n = len(self.sort_array)
        
        for i in range(n):
            min_idx = i
            steps.append(f"Finding minimum from position {i}")
            
            for j in range(i + 1, n):
                if self.sort_array[j] < self.sort_array[min_idx]:
                    min_idx = j
                    steps.append(f"New minimum found: {self.sort_array[min_idx]} at position {min_idx}")
            
            if min_idx != i:
                self.sort_array[i], self.sort_array[min_idx] = self.sort_array[min_idx], self.sort_array[i]
                steps.append(f"Swap {self.sort_array[min_idx]} with {self.sort_array[i]}")
        
        return steps
    
    def insertion_sort_steps(self):
        steps = []
        
        for i in range(1, len(self.sort_array)):
            key = self.sort_array[i]
            j = i - 1
            steps.append(f"Insert {key} into sorted portion")
            
            while j >= 0 and self.sort_array[j] > key:
                self.sort_array[j + 1] = self.sort_array[j]
                steps.append(f"Move {self.sort_array[j]} to position {j+1}")
                j -= 1
            
            self.sort_array[j + 1] = key
            steps.append(f"Place {key} at position {j+1}")
        
        return steps
    
    def open_prime_generator(self):
        prime_window = tk.Toplevel(self.root)
        prime_window.title("Prime Number Generator")
        prime_window.geometry("800x650")
        prime_window.configure(bg=self.colors['dark'])
        
        header = tk.Label(prime_window,
                         text="Prime Number Generator",
                         font=('Arial', 20, 'bold'),
                         fg=self.colors['light'],
                         bg=self.colors['dark'])
        header.pack(pady=20)
        
        input_frame = tk.Frame(prime_window, bg=self.colors['dark'])
        input_frame.pack(pady=20)
        
        tk.Label(input_frame,
                text="Generate primes up to:",
                font=('Arial', 12),
                fg=self.colors['light'],
                bg=self.colors['dark']).pack(side='left')
        
        self.prime_limit = tk.StringVar(value="100")
        limit_entry = tk.Entry(input_frame, textvariable=self.prime_limit,
                              width=10, font=('Arial', 12))
        limit_entry.pack(side='left', padx=10)
        
        button_frame = tk.Frame(prime_window, bg=self.colors['dark'])
        button_frame.pack(pady=15)
        
        sieve_btn = ttk.Button(button_frame,
                             text="Sieve of Eratosthenes",
                             style='Custom.TButton',
                             command=self.generate_primes_sieve)
        sieve_btn.pack(side='left', padx=10)
        
        trial_btn = ttk.Button(button_frame,
                             text="Trial Division",
                             style='Secondary.TButton',
                             command=self.generate_primes_trial)
        trial_btn.pack(side='left', padx=10)
        
        check_btn = ttk.Button(button_frame,
                             text="Check Single Number",
                             style='Success.TButton',
                             command=self.check_prime)
        check_btn.pack(side='left', padx=10)
        
        self.prime_result = scrolledtext.ScrolledText(prime_window,
                                                     height=20, width=90,
                                                     bg=self.colors['card'],
                                                     fg=self.colors['light'],
                                                     font=('Arial', 10))
        self.prime_result.pack(pady=20, padx=20, fill='both', expand=True)
        
        self.prime_result.insert('1.0',
            "Prime Number Generator\n\n"
            "Two algorithms available:\n\n"
            "1. Sieve of Eratosthenes:\n"
            "   - Most efficient for finding all primes up to a limit\n"
            "   - Time complexity: O(n log log n)\n"
            "   - Works by eliminating multiples of each prime\n\n"
            "2. Trial Division:\n"
            "   - Tests each number individually\n"
            "   - Time complexity: O(n√n)\n"
            "   - Good for checking individual numbers\n\n"
            "Enter a limit and click on an algorithm to see it in action!")
    
    def generate_primes_sieve(self):
        try:
            limit = int(self.prime_limit.get())
            if limit < 2:
                messagebox.showerror("Error", "Please enter a number >= 2")
                return
            
            primes, steps = self.sieve_of_eratosthenes(limit)
            
            self.prime_result.delete('1.0', 'end')
            self.prime_result.insert('1.0',
                f"Sieve of Eratosthenes - Primes up to {limit}:\n\n"
                f"Algorithm steps:\n")
            
            for step in steps[:15]:
                self.prime_result.insert('end', f"{step}\n")
            
            if len(steps) > 15:
                self.prime_result.insert('end', f"... and {len(steps) - 15} more steps\n")
            
            self.prime_result.insert('end',
                f"\nFound {len(primes)} prime numbers:\n"
                f"{', '.join(map(str, primes[:50]))}")
            
            if len(primes) > 50:
                self.prime_result.insert('end', f"\n... and {len(primes) - 50} more primes")
            
            self.prime_result.insert('end',
                f"\n\nLargest prime found: {max(primes) if primes else 'None'}")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number!")
    
    def sieve_of_eratosthenes(self, limit):
        if limit < 2:
            return [], []
        
        sieve = [True] * (limit + 1)
        sieve[0] = sieve[1] = False
        steps = []
        
        for i in range(2, int(math.sqrt(limit)) + 1):
            if sieve[i]:
                steps.append(f"Marking multiples of {i}")
                for j in range(i * i, limit + 1, i):
                    sieve[j] = False
        
        primes = [i for i in range(2, limit + 1) if sieve[i]]
        return primes, steps
    
    def generate_primes_trial(self):
        try:
            limit = int(self.prime_limit.get())
            if limit < 2:
                messagebox.showerror("Error", "Please enter a number >= 2")
                return
            
            primes = []
            steps = []
            
            for num in range(2, limit + 1):
                if self.is_prime_trial(num):
                    primes.append(num)
                    steps.append(f"{num} is prime")
                else:
                    steps.append(f"{num} is not prime")
                
                if len(steps) > 100:
                    break
            
            self.prime_result.delete('1.0', 'end')
            self.prime_result.insert('1.0',
                f"Trial Division - Primes up to {limit}:\n\n"
                f"Algorithm: Test each number by dividing by all smaller primes\n\n"
                f"Steps (showing first 100):\n")
            
            for step in steps[:20]:
                self.prime_result.insert('end', f"{step}\n")
            
            self.prime_result.insert('end',
                f"\nFound {len(primes)} prime numbers:\n"
                f"{', '.join(map(str, primes[:50]))}")
            
            if len(primes) > 50:
                self.prime_result.insert('end', f"\n... and {len(primes) - 50} more primes")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number!")
    
    def is_prime_trial(self, n):
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        
        for i in range(3, int(math.sqrt(n)) + 1, 2):
            if n % i == 0:
                return False
        return True
    
    def check_prime(self):
        try:
            num = int(self.prime_limit.get())
            if num < 2:
                messagebox.showerror("Error", "Please enter a number >= 2")
                return
            
            is_prime = self.is_prime_trial(num)
            factors = []
            
            if not is_prime:
                for i in range(2, int(math.sqrt(num)) + 1):
                    if num % i == 0:
                        factors.append(i)
                        if i != num // i:
                            factors.append(num // i)
            
            self.prime_result.delete('1.0', 'end')
            
            if is_prime:
                self.prime_result.insert('1.0',
                    f"Prime Check for {num}:\n\n"
                    f"Result: {num} IS PRIME\n\n"
                    f"Verification: Tested divisibility by all numbers from 2 to {int(math.sqrt(num))}\n"
                    f"No divisors found, therefore {num} is prime.\n\n"
                    f"Properties:\n"
                    f"- Only divisible by 1 and {num}\n"
                    f"- Cannot be expressed as a product of smaller integers")
            else:
                factors.sort()
                self.prime_result.insert('1.0',
                    f"Prime Check for {num}:\n\n"
                    f"Result: {num} IS NOT PRIME\n\n"
                    f"Factors found: {factors}\n"
                    f"Prime factorization: {self.prime_factorization(num)}\n\n"
                    f"Since {num} has factors other than 1 and itself, it is composite.")
        
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number!")
    
    def prime_factorization(self, n):
        factors = []
        d = 2
        while d * d <= n:
            while n % d == 0:
                factors.append(d)
                n //= d
            d += 1
        if n > 1:
            factors.append(n)
        
        if len(factors) == 1:
            return str(factors[0])
        
        factor_counts = {}
        for factor in factors:
            factor_counts[factor] = factor_counts.get(factor, 0) + 1
        
        result = []
        for factor, count in sorted(factor_counts.items()):
            if count == 1:
                result.append(str(factor))
            else:
                result.append(f"{factor}^{count}")
        
        return " × ".join(result)

if __name__ == "__main__":

   class AlgorithmChallengeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Algorithm Visualizer")
        self.colors = {
            'card': '#2b2b2b',
            'light': '#ffffff'
        }

        # Sort window (can be a Frame or Toplevel)
        sort_window = tk.Frame(self.root)
        sort_window.pack(pady=20)

        # Scrolled Text for algorithm info
        self.sort_info = scrolledtext.ScrolledText(sort_window,
                                                   height=12, width=100,
                                                   bg=self.colors['card'],
                                                   fg=self.colors['light'],
                                                   font=('Arial', 10))
        self.sort_info.pack(pady=20, padx=20, fill='both', expand=True)

        # Array for sorting
        self.sort_array = []
        self.generate_sort_array()

    def generate_sort_array(self):
        self.sort_array = [random.randint(10, 280) for _ in range(20)]
        self.draw_array()

        algorithm_info = {
            "Bubble Sort": "Bubble Sort compares adjacent elements and swaps them if they're in wrong order.\nTime Complexity: O(n²), Space: O(1)\nBest for: Educational purposes, small datasets",
            "Selection Sort": "Selection Sort finds the minimum element and places it at the beginning.\nTime Complexity: O(n²), Space: O(1)\nBest for: Small datasets, memory-constrained environments",
            "Insertion Sort": "Insertion Sort builds the sorted array one element at a time.\nTime Complexity: O(n²), Space: O(1)\nBest for: Small datasets, nearly sorted data"
        }

        self.sort_info.insert(tk.END, "\n\n".join(
            [f"{name}:\n{desc}" for name, desc in algorithm_info.items()]))

    def draw_array(self):
        # Add your array-drawing logic here, possibly using Canvas
        pass

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = AlgorithmChallengeApp(root)
    root.mainloop()





        # self.sort_info.insert('1.0',
        #     f"Algorithm: {self.sort_algorithm.get()}\n\n"
        #     algorithm_info.get(self.sort_algorithm.get(), '') + "\n\n"
        #     f"Generated array: {self.sort_array}\n\n"
        #     "Click 'Sort Array' to see the algorithm in action!")

                # self.sort_info.insert('1.0',
        #     f"Algorithm: {self.sort_algorithm.get()}\n\n"
        #     algorithm_info.get(self.sort_algorithm.get(), '') + "\n\n"
        #     f"Generated array: {self.sort_array}\n\n"
        #     "Click 'Sort Array' to see the algorithm in action!")
                # self.sort_info.insert('1.0',
        #     f"Algorithm: {self.sort_algorithm.get()}\n\n"
        #     algorithm_info.get(self.sort_algorithm.get(), '') + "\n\n"
        #     f"Generated array: {self.sort_array}\n\n"
        #     "Click 'Sort Array' to see the algorithm in action!")
                # self.sort_info.insert('1.0',
        #     f"Algorithm: {self.sort_algorithm.get()}\n\n"
        #     algorithm_info.get(self.sort_algorithm.get(), '') + "\n\n"
        #     f"Generated array: {self.sort_array}\n\n"
        #     "Click 'Sort Array' to see the algorithm in action!")
                # self.sort_info.insert('1.0',
        #     f"Algorithm: {self.sort_algorithm.get()}\n\n"
        #     algorithm_info.get(self.sort_algorithm.get(), '') + "\n\n"
        #     f"Generated array: {self.sort_array}\n\n"
        #     "Click 'Sort Array' to see the algorithm in action!")
        # # print(reversed(str))
# reverse = ''
# for char in str:
#     reverse = char + reverse
    
# if reverse == str:
#     print("true")
# else:
#     print("false")
     #     algorithm_info.get(self.sort_algorithm.get(), '') + "\n\n"
        #     f"Generated array: {self.sort_array}\n\n"
        #     "Click 'Sort Array' to see the algorithm in action!")
        # # print(reversed(str))
# reverse = ''
# for char in str:
#     reverse = char + reverse
    
# if reverse == str:
#     print("true")
# else:
#     print("false")
