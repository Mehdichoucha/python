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
        self.create_grid()

    def create_grid(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        for row_index in range(self.rows):
            Grid.rowconfigure(self.frame, row_index, weight=1)
            for col_index in range(self.columns):
                Grid.columnconfigure(self.frame, col_index, weight=1)
                btn = Button(self.frame)  
                btn.grid(row=row_index, column=col_index, sticky=N+S+E+W)

    def update_grid(self,rows,columns):
        self.rows = rows
        self.colums = columns
        self.create_grid()

def set_difficulty(grille,difficulty):
    if difficulty == "Easy":
        grille.update_grid(3,5)
    elif difficulty == "Medium":
        grille.update_grid(5,10)
    elif difficulty == "Hard":
        grille.update_grid(8,15)

def quit_game():
        root.quit()

if __name__ == "__main__":
    root = Tk()
    grille = Grille(root)

    menu_bar = Menu(root)
    difficulty_menu = Menu(menu_bar, tearoff=0)
    difficulty_menu.add_command(label="Easy", command=lambda:set_difficulty(grille, "Easy"))
    difficulty_menu.add_command(label="Medium", command=lambda:set_difficulty(grille, "Medium"))
    difficulty_menu.add_command(label="Hard", command=lambda:set_difficulty(grille, "Hard"))
    menu_bar.add_cascade(label="Difficulty", menu=difficulty_menu)
    root.config(menu=menu_bar)

    quit_menu = Menu(menu_bar, tearoff=0)
    quit_menu.add_command(label="Quit", command=lambda:quit_game(grille, "Quit"))
    menu_bar.add_cascade(label="Quit", menu=quit_menu)




    root.mainloop()
