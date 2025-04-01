import tkinter  as tk 
my_w = tk.Tk()
my_w.geometry("350x170")  

counter = 0 
def my_time():
    global counter
    counter = counter + 1
    if counter < 0:
        return
    
    l1.config(text = str(counter))
    l1.after(1000, my_time) 
	
l1 = tk.Label(my_w, font = ('times', 10), width = 20)
l1.grid(row = 1, column = 1, padx = 50, pady = 30)

my_time() 
my_w.mainloop()    