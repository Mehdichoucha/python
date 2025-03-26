from tkinter import * 

class Grille:
    def __init__(self, master, rows=5, columns=10, width=800, height=400):

        self.master = master
        self.master.title("Grille dynamique") 
        self.master.geometry(f"{width}x{height}")
        Grid.rowconfigure(master, 0, weight=1)
        Grid.columnconfigure(master, 0, weight=1)

        self.frame = Frame(master)
        self.frame.grid(row=0, column=0, sticky=N+S+E+W)

        self.rows = rows
        self.columns = columns
        self.grid_data = [[0 for _ in range(columns)] for _ in range(rows)]
        self.buttons = [[None for _ in range(columns)] for _ in range(rows)]
        self.flags = {} 
        self.revealed = set()
        
        self.place_fixed_mine()
        self.calculate_numbers()
        self.create_grid()

    def place_fixed_mine(self):
        mine_row, mine_col = 2, 2
        self.grid_data[mine_row][mine_col] = -1
        self.grid_data[mine_row][mine_col] = -1 

    def calculate_numbers(self):
        """ Calculate the number of mines around each square. """
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for r in range(self.rows):
            for c in range(self.columns):
                if self.grid_data[r][c] == -1:
                    continue
                count = 0
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.rows and 0 <= nc < self.columns and self.grid_data[nr][nc] == -1:
                        count += 1
                self.grid_data[r][c] = count 

    def create_grid(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        for r in range(self.rows):
            Grid.rowconfigure(self.frame, r, weight=1)
            for c in range(self.columns):
                Grid.columnconfigure(self.frame, c, weight=1)
                btn = Button(self.frame, text="", width=3, height=2)
                btn.grid(row=r, column=c, sticky=N+S+E+W)
                btn.bind("<Button-1>", lambda e, x=r, y=c: self.reveal_cell(x, y))
                btn.bind("<Button-3>", lambda e, x=r, y=c: self.toggle_flag(x, y))
                self.buttons[r][c] = btn
                self.flags[(r, c)] = 0
                
    def reveal_cell(self, row, col):
        """ Reveals a square and triggers recursion if it is a 0. """
        if (row, col) in self.revealed or self.flags[(row, col)] > 0:
            return 

        self.revealed.add((row, col))
        btn = self.buttons[row][col]
        value = self.grid_data[row][col]

        if value == -1:
            btn.config(text="*", bg="red") 
        else:
            btn.config(text=str(value) if value > 0 else "", bg="lightgray")
            btn.config(state=DISABLED)

            if value == 0:
                self.reveal_adjacent(row, col)

    def reveal_adjacent(self, row, col):
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < self.rows and 0 <= nc < self.columns:
                self.reveal_cell(nr, nc)

    def toggle_flag(self, row, col):
        """Alternates flag (🚩), question mark (❓) and blank. """
        btn = self.buttons[row][col]
        self.flags[(row, col)] = (self.flags[(row, col)] + 1) % 3

        if self.flags[(row, col)] == 1:
            btn.config(text="🚩", fg="red")
        elif self.flags[(row, col)] == 2:
            btn.config(text="❓", fg="blue")
        else:
            btn.config(text="") 
            
def set_difficulty(grille, difficulty): 
    if difficulty == "Easy": 
        grille.__init__(grille.master, rows=3, columns=5) 
    elif difficulty == "Medium": 
        grille.__init__(grille.master, rows=5, columns=10) 
    elif difficulty == "Hard": 
        grille.__init__(grille.master, rows=8, columns=15) 

def quit_game():
    root.quit() 
        
if __name__ == "__main__":
    root = Tk()
    grille = Grille(root)

    menu_bar = Menu(root)
    difficulty_menu = Menu(menu_bar, tearoff=0)
    difficulty_menu.add_command(label="Easy", command=lambda: set_difficulty(grille, "Easy"))
    difficulty_menu.add_command(label="Medium", command=lambda: set_difficulty(grille, "Medium"))
    difficulty_menu.add_command(label="Hard", command=lambda: set_difficulty(grille, "Hard"))
    menu_bar.add_cascade(label="Difficulty", menu=difficulty_menu)
    

    quit_menu = Menu(menu_bar, tearoff=0)
    quit_menu.add_command(label="Quit", command=lambda:quit_game(grille, "Quit"))
    menu_bar.add_cascade(label="Quit", menu=quit_menu)

    root.config(menu=menu_bar)
    root.mainloop()