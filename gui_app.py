
import tkinter as tk
from tkinter import ttk, messagebox
import random
from collections import deque
import heapq
import time
import threading

class MazeCell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False
        self.is_path = False
        self.is_start = False
        self.is_end = False
        self.distance = float('inf')
        self.parent = None

class MazeSolver:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Professional Maze Solver")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        self.maze = []
        self.rows = 25
        self.cols = 25
        self.cell_size = 20
        self.start_pos = None
        self.end_pos = None
        self.solving = False
        
        self.colors = {
            'wall': '#2c3e50',
            'path': '#ecf0f1',
            'start': '#e74c3c',
            'end': '#27ae60',
            'solution': '#3498db',
            'visited': '#f39c12',
            'current': '#9b59b6'
        }
        
        self.setup_ui()
        self.generate_maze()
        self.draw_maze()
        
    def setup_ui(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(control_frame, text="Maze Solver", font=('Arial', 16, 'bold')).pack(side='left')
        
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(side='right')
        
        ttk.Button(button_frame, text="Generate New Maze", command=self.new_maze).pack(side='left', padx=2)
        ttk.Button(button_frame, text="Clear Path", command=self.clear_path).pack(side='left', padx=2)
        
        self.algorithm_var = tk.StringVar(value="A*")
        algorithm_combo = ttk.Combobox(button_frame, textvariable=self.algorithm_var, 
                                     values=["A*", "Dijkstra", "BFS", "DFS"], state="readonly", width=10)
        algorithm_combo.pack(side='left', padx=2)
        
        ttk.Button(button_frame, text="Solve Maze", command=self.solve_maze).pack(side='left', padx=2)
        
        size_frame = ttk.Frame(control_frame)
        size_frame.pack(side='right', padx=(20, 0))
        
        ttk.Label(size_frame, text="Size:").pack(side='left')
        self.size_var = tk.StringVar(value="25x25")
        size_combo = ttk.Combobox(size_frame, textvariable=self.size_var,
                                values=["15x15", "25x25", "35x35", "45x45"], state="readonly", width=8)
        size_combo.pack(side='left', padx=2)
        size_combo.bind('<<ComboboxSelected>>', self.change_size)
        
        canvas_frame = ttk.Frame(main_frame)
        canvas_frame.pack(fill='both', expand=True)
        
        self.canvas = tk.Canvas(canvas_frame, bg='white', highlightthickness=1, highlightbackground='#bdc3c7')
        
        h_scrollbar = ttk.Scrollbar(canvas_frame, orient='horizontal', command=self.canvas.xview)
        v_scrollbar = ttk.Scrollbar(canvas_frame, orient='vertical', command=self.canvas.yview)
        
        self.canvas.configure(xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)
        
        self.canvas.grid(row=0, column=0, sticky='nsew')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        
        canvas_frame.grid_rowconfigure(0, weight=1)
        canvas_frame.grid_columnconfigure(0, weight=1)
        
        self.canvas.bind('<Button-1>', self.on_click)
        self.canvas.bind('<B1-Motion>', self.on_drag)
        
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill='x', pady=(10, 0))
        
        self.status_var = tk.StringVar(value="Click to set start point (red), right-click to set end point (green)")
        ttk.Label(info_frame, textvariable=self.status_var, font=('Arial', 10)).pack(side='left')
        
        legend_frame = ttk.Frame(info_frame)
        legend_frame.pack(side='right')
        
        legend_items = [
            ("Start", self.colors['start']),
            ("End", self.colors['end']),
            ("Path", self.colors['solution']),
            ("Visited", self.colors['visited'])
        ]
        
        for text, color in legend_items:
            item_frame = ttk.Frame(legend_frame)
            item_frame.pack(side='left', padx=5)
            
            color_box = tk.Frame(item_frame, width=15, height=15, bg=color, relief='solid', bd=1)
            color_box.pack(side='left', padx=(0, 3))
            
            ttk.Label(item_frame, text=text, font=('Arial', 9)).pack(side='left')
    
    def change_size(self, event):
        size_str = self.size_var.get()
        size = int(size_str.split('x')[0])
        self.rows = self.cols = size
        
        if size <= 25:
            self.cell_size = 20
        elif size <= 35:
            self.cell_size = 15
        else:
            self.cell_size = 12
            
        self.new_maze()
    
    def generate_maze(self):
        self.maze = [[MazeCell(r, c) for c in range(self.cols)] for r in range(self.rows)]
        
        stack = []
        current = self.maze[0][0]
        current.visited = True
        
        while True:
            neighbors = self.get_unvisited_neighbors(current)
            
            if neighbors:
                next_cell = random.choice(neighbors)
                stack.append(current)
                self.remove_wall(current, next_cell)
                current = next_cell
                current.visited = True
            elif stack:
                current = stack.pop()
            else:
                break
        
        for row in self.maze:
            for cell in row:
                cell.visited = False
    
    def get_unvisited_neighbors(self, cell):
        neighbors = []
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        for dr, dc in directions:
            nr, nc = cell.row + dr, cell.col + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                if not self.maze[nr][nc].visited:
                    neighbors.append(self.maze[nr][nc])
        
        return neighbors
    
    def remove_wall(self, current, next_cell):
        dr = next_cell.row - current.row
        dc = next_cell.col - current.col
        
        if dr == 1:
            current.walls['bottom'] = False
            next_cell.walls['top'] = False
        elif dr == -1:
            current.walls['top'] = False
            next_cell.walls['bottom'] = False
        elif dc == 1:
            current.walls['right'] = False
            next_cell.walls['left'] = False
        elif dc == -1:
            current.walls['left'] = False
            next_cell.walls['right'] = False
    
    def draw_maze(self):
        self.canvas.delete('all')
        
        canvas_width = self.cols * self.cell_size
        canvas_height = self.rows * self.cell_size
        self.canvas.configure(scrollregion=(0, 0, canvas_width, canvas_height))
        
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.maze[r][c]
                x1, y1 = c * self.cell_size, r * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                
                color = self.colors['path']
                if cell.is_start:
                    color = self.colors['start']
                elif cell.is_end:
                    color = self.colors['end']
                elif cell.is_path:
                    color = self.colors['solution']
                elif cell.visited:
                    color = self.colors['visited']
                
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='')
                
                if cell.walls['top']:
                    self.canvas.create_line(x1, y1, x2, y1, fill=self.colors['wall'], width=2)
                if cell.walls['right']:
                    self.canvas.create_line(x2, y1, x2, y2, fill=self.colors['wall'], width=2)
                if cell.walls['bottom']:
                    self.canvas.create_line(x1, y2, x2, y2, fill=self.colors['wall'], width=2)
                if cell.walls['left']:
                    self.canvas.create_line(x1, y1, x1, y2, fill=self.colors['wall'], width=2)
    
    def on_click(self, event):
        if self.solving:
            return
            
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        
        col = int(canvas_x // self.cell_size)
        row = int(canvas_y // self.cell_size)
        
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.set_start_point(row, col)
    
    def on_drag(self, event):
        self.on_click(event)
    
    def set_start_point(self, row, col):
        if self.start_pos:
            old_r, old_c = self.start_pos
            self.maze[old_r][old_c].is_start = False
        
        self.start_pos = (row, col)
        self.maze[row][col].is_start = True
        self.draw_maze()
        
        if self.end_pos:
            self.status_var.set("Start and end points set. Click 'Solve Maze' to find the path.")
        else:
            self.status_var.set("Start point set. Right-click to set end point.")
    
    def set_end_point(self, row, col):
        if self.end_pos:
            old_r, old_c = self.end_pos
            self.maze[old_r][old_c].is_end = False
        
        self.end_pos = (row, col)
        self.maze[row][col].is_end = True
        self.draw_maze()
        
        if self.start_pos:
            self.status_var.set("Start and end points set. Click 'Solve Maze' to find the path.")
        else:
            self.status_var.set("End point set. Click to set start point.")
    
    def new_maze(self):
        self.start_pos = None
        self.end_pos = None
        self.solving = False
        self.generate_maze()
        self.draw_maze()
        self.status_var.set("New maze generated. Click to set start point, right-click to set end point.")
    
    def clear_path(self):
        if self.solving:
            return
            
        for row in self.maze:
            for cell in row:
                cell.is_path = False
                cell.visited = False
                cell.distance = float('inf')
                cell.parent = None
        
        self.draw_maze()
        self.status_var.set("Path cleared.")
    
    def solve_maze(self):
        if not self.start_pos or not self.end_pos:
            messagebox.showwarning("Warning", "Please set both start and end points.")
            return
        
        if self.solving:
            return
        
        self.clear_path()
        algorithm = self.algorithm_var.get()
        
        threading.Thread(target=self.run_algorithm, args=(algorithm,), daemon=True).start()
    
    def run_algorithm(self, algorithm):
        self.solving = True
        self.status_var.set(f"Solving maze using {algorithm} algorithm...")
        
        start_time = time.time()
        
        if algorithm == "A*":
            path = self.a_star()
        elif algorithm == "Dijkstra":
            path = self.dijkstra()
        elif algorithm == "BFS":
            path = self.bfs()
        elif algorithm == "DFS":
            path = self.dfs()
        
        end_time = time.time()
        
        if path:
            self.animate_solution(path)
            self.status_var.set(f"Path found! Length: {len(path)} steps. Time: {end_time - start_time:.3f}s")
        else:
            self.status_var.set("No path found!")
        
        self.solving = False
    
    def get_neighbors(self, cell):
        neighbors = []
        directions = [(-1, 0, 'top'), (0, 1, 'right'), (1, 0, 'bottom'), (0, -1, 'left')]
        
        for dr, dc, wall in directions:
            if not cell.walls[wall]:
                nr, nc = cell.row + dr, cell.col + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    neighbors.append(self.maze[nr][nc])
        
        return neighbors
    
    def heuristic(self, cell1, cell2):
        return abs(cell1.row - cell2.row) + abs(cell1.col - cell2.col)
    
    def a_star(self):
        start_cell = self.maze[self.start_pos[0]][self.start_pos[1]]
        end_cell = self.maze[self.end_pos[0]][self.end_pos[1]]
        
        open_set = [(0, start_cell)]
        start_cell.distance = 0
        
        while open_set:
            current_f, current = heapq.heappop(open_set)
            
            if current == end_cell:
                return self.reconstruct_path(end_cell)
            
            if current.visited:
                continue
                
            current.visited = True
            self.root.after(0, self.draw_maze)
            time.sleep(0.01)
            
            for neighbor in self.get_neighbors(current):
                if neighbor.visited:
                    continue
                
                tentative_g = current.distance + 1
                
                if tentative_g < neighbor.distance:
                    neighbor.distance = tentative_g
                    neighbor.parent = current
                    f_score = tentative_g + self.heuristic(neighbor, end_cell)
                    heapq.heappush(open_set, (f_score, neighbor))
        
        return None
    
    def dijkstra(self):
        start_cell = self.maze[self.start_pos[0]][self.start_pos[1]]
        end_cell = self.maze[self.end_pos[0]][self.end_pos[1]]
        
        pq = [(0, start_cell)]
        start_cell.distance = 0
        
        while pq:
            current_dist, current = heapq.heappop(pq)
            
            if current == end_cell:
                return self.reconstruct_path(end_cell)
            
            if current.visited:
                continue
                
            current.visited = True
            self.root.after(0, self.draw_maze)
            time.sleep(0.01)
            
            for neighbor in self.get_neighbors(current):
                if neighbor.visited:
                    continue
                
                new_dist = current.distance + 1
                
                if new_dist < neighbor.distance:
                    neighbor.distance = new_dist
                    neighbor.parent = current
                    heapq.heappush(pq, (new_dist, neighbor))
        
        return None
    
    def bfs(self):
        start_cell = self.maze[self.start_pos[0]][self.start_pos[1]]
        end_cell = self.maze[self.end_pos[0]][self.end_pos[1]]
        
        queue = deque([start_cell])
        start_cell.visited = True
        
        while queue:
            current = queue.popleft()
            
            if current == end_cell:
                return self.reconstruct_path(end_cell)
            
            self.root.after(0, self.draw_maze)
            time.sleep(0.01)
            
            for neighbor in self.get_neighbors(current):
                if not neighbor.visited:
                    neighbor.visited = True
                    neighbor.parent = current
                    queue.append(neighbor)
        
        return None
    
    def dfs(self):
        start_cell = self.maze[self.start_pos[0]][self.start_pos[1]]
        end_cell = self.maze[self.end_pos[0]][self.end_pos[1]]
        
        stack = [start_cell]
        start_cell.visited = True
        
        while stack:
            current = stack.pop()
            
            if current == end_cell:
                return self.reconstruct_path(end_cell)
            
            self.root.after(0, self.draw_maze)
            time.sleep(0.02)
            
            for neighbor in self.get_neighbors(current):
                if not neighbor.visited:
                    neighbor.visited = True
                    neighbor.parent = current
                    stack.append(neighbor)
        
        return None
    
    def reconstruct_path(self, end_cell):
        path = []
        current = end_cell
        
        while current:
            path.append(current)
            current = current.parent
        
        return path[::-1]
    
    def animate_solution(self, path):
        for cell in path:
            cell.is_path = True
            self.root.after(0, self.draw_maze)
            time.sleep(0.05)
    
    def run(self):
        self.canvas.bind('<Button-3>', lambda e: self.right_click(e))
        self.root.mainloop()
    
    def right_click(self, event):
        if self.solving:
            return
            
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        
        col = int(canvas_x // self.cell_size)
        row = int(canvas_y // self.cell_size)
        
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.set_end_point(row, col)

if __name__ == "__main__":
    maze_solver = MazeSolver()
    maze_solver.run()




