from tkinter import *

window = Tk()
window.geometry("800x400")
window.title("Démineur")
window['bg'] = "#ffffff"
window.resizable(height = True, width = True )

def play_command():
    window.destroy()
    import menu

def difficulty_command():
    import menu

def quit_command():
    window.quit()



label = Label(window, text = "Mines Weeper", bg = "#ffffff", font = ("Helvetica", 40))
label.place(x = 240, y = 20)

menu_button = Button(window, text = "Play", bg = "#C8BFE7", height = 2, width = 14, font = ("Helvetica", 15), command = play_command)
menu_button.place(x = 320, y = 120)

difficulty_button = Button(window, text = "Difficulty", bg = "#C8BFE7", height = 2, width = 14, font = ("Helvetica", 15), command = difficulty_command)
difficulty_button.place(x = 320, y = 210)

quit_button = Button(window, text = "Quit", bg = "#C8BFE7", height = 2, width = 14, font = ("Helvetica", 15), command = quit_command)
quit_button.place(x = 320, y = 300)


window.mainloop()