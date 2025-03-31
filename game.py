from tkinter import *
from tkinter import messagebox
from random import randint
import sys

class Bombe:
    def __init__(self, grille, row, col):
        self.grille = grille
        self.row = row
        self.col = col
        self.is_bomb = False
        self._neighbor_bombs = 0
        self.revealed = False

    def set_bomb(self):
        self.is_bomb = True

    def get_neighbor_bombs(self):
        return self._neighbor_bombs

    def set_neighbor_bombs(self, value):
        self._neighbor_bombs = value

    def reveal(self):
        if self.revealed or self.grille.flags[self.row][self.col] != 0:
            return
       
        self.revealed = True
        btn = self.grille.buttons[self.row][self.col]
        btn.config(state=DISABLED, relief=SUNKEN)
        
        if self.is_bomb:
            btn.config(text="💣", bg="red")
            if messagebox.showerror("Game Over", "You clicked on a bomb !"):
                self.grille.restart_game()
        else:
            if self._neighbor_bombs > 0:
                btn.config(text=str(self._neighbor_bombs))
            else:
                btn.config(text="", bg="pink")
                self.reveal_adjacent()
            
            if self.grille.check_win():
                if messagebox.showinfo("Congracts", "You won!"):
                    self.grille.restart_game()

    def reveal_adjacent(self):
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dr, dc in directions:
            nr, nc = self.row + dr, self.col + dc
            if 0 <= nr < self.grille.rows and 0 <= nc < self.grille.columns:
                self.grille.bombs[nr][nc].reveal()

class Grille:
    def __init__(self, master, rows=9, columns=9, width=800, height=400):
        self.master = master
        self.master.title("Démineur")
        self.master.geometry(f"{width}x{height}")
        Grid.rowconfigure(master, 0, weight=1)
        Grid.columnconfigure(master, 0, weight=1)
        
        self.frame = Frame(master)
        self.frame.grid(row=0, column=0, sticky=N+S+E+W)

        self.rows = rows
        self.columns = columns
        self.buttons = []
        self.bombs = []
        self.flags = []

        self.create_grid()

    def create_grid(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
            
        self.buttons = []
        self.bombs = []
        self.flags = [[0 for _ in range(self.columns)] for _ in range(self.rows)]

        for row_index in range(self.rows):
            Grid.rowconfigure(self.frame, row_index, weight=1)
            button_row = []
            bomb_row = []
            
            for col_index in range(self.columns):
                Grid.columnconfigure(self.frame, col_index, weight=1)

                bomb = Bombe(self, row_index, col_index)
                bomb_row.append(bomb)

                btn = Button(self.frame, 
                           command=lambda r=row_index, c=col_index: self.on_click(r, c),
                           width=3, height=2)
                btn.bind("<Button-3>", lambda event, r=row_index, c=col_index: self.toggle_flag(r,c))
                btn.grid(row=row_index, column=col_index, sticky=N+S+E+W)
                
                button_row.append(btn)
            
            self.buttons.append(button_row)
            self.bombs.append(bomb_row)

    def on_click(self, row, col):
        if not hasattr(self, 'bombs_placed'):
            self.bombs_placed = True
            if self.rows == 9 and self.columns == 9:
                self.place_bombs(10, row, col)
            elif self.rows == 16 and self.columns == 16:
                self.place_bombs(40, row, col)
            elif self.rows == 16 and self.columns == 30:
                self.place_bombs(99, row, col)
    
        if self.flags[row][col] == 0:
            self.bombs[row][col].reveal()

    def toggle_flag(self, row, col):
        if self.bombs[row][col].revealed:
            return
            
        btn = self.buttons[row][col]
        self.flags[row][col] = (self.flags[row][col] + 1) % 3

        if self.flags[row][col] == 1:
            btn.config(text="🚩", fg="green")
        elif self.flags[row][col] == 2:
            btn.config(text="❓", fg="blue")
        else:
            btn.config(text="")
    
    def place_bombs(self, bomb_count, first_click_row, first_click_col):
        bombs_placed = 0
        
        while bombs_placed < bomb_count:
            row = randint(0, self.rows-1)
            col = randint(0, self.columns-1)
            
            if (abs(row - first_click_row) <= 1 and abs(col - first_click_col) <= 1):
                continue
                
            if not self.bombs[row][col].is_bomb:
                self.bombs[row][col].set_bomb()
                bombs_placed += 1
                
        self.calculate_neighbors()

    def calculate_neighbors(self):
        for row in range(self.rows):
            for col in range(self.columns):
                if not self.bombs[row][col].is_bomb:
                    count = 0
                    for r in range(max(0, row-1), min(self.rows, row+2)):
                        for c in range(max(0, col-1), min(self.columns, col+2)):
                            if self.bombs[r][c].is_bomb:
                                count += 1
                    self.bombs[row][col].set_neighbor_bombs(count)

    def update_grid(self, rows, columns):
        self.rows = rows
        self.columns = columns
        if hasattr(self, 'bombs_placed'):
            del self.bombs_placed
        self.create_grid()

    def check_win(self):
        
        for row in range(self.rows):
            for col in range(self.columns):
                if not self.bombs[row][col].is_bomb and not self.bombs[row][col].revealed:
                    return False
        return True

    def restart_game(self):
        
        if hasattr(self, 'bombs_placed'):
            del self.bombs_placed
        self.create_grid()

def set_difficulty(grille, difficulty):
    if difficulty == "Easy":
        grille.update_grid(9, 9)
    elif difficulty == "Medium":
        grille.update_grid(16, 16)
    elif difficulty == "Hard":
        grille.update_grid(16, 30)

def quit_game():
    root.destroy()
    sys.exit()

if __name__ == "__main__":
    root = Tk()
    grille = Grille(root)

    menu_bar = Menu(root)
    
    difficulty_menu = Menu(menu_bar, tearoff=0)
    difficulty_menu.add_command(label="Easy", command=lambda: set_difficulty(grille, "Easy"))
    difficulty_menu.add_command(label="Medium", command=lambda: set_difficulty(grille, "Medium"))
    difficulty_menu.add_command(label="Hard", command=lambda: set_difficulty(grille, "Hard"))
    menu_bar.add_cascade(label="Difficulty", menu=difficulty_menu)
    
    menu_bar.add_command(label="Quit", command=quit_game)
    menu_bar.add_command(label="Restart", command=grille.restart_game)
    
    root.config(menu=menu_bar)
    root.mainloop()