import tkinter as tk
from time import sleep
from tkinter import ttk

HEIGHT = 500
WIDTH = 600


def mar1():
#   selection = "You selected the option " + str(var.get())
#   label.config(text = selection)
#   print("clicked")
    with open('restock-logs2021-03-21-to-2021-03-28.txt', 'r') as file:
        global txt
        txt = file.read()

def feb():
    with open('restock-logs2021-02-14-to-2021-02-19.txt', 'r') as file:
        global txt
        txt = file.read()

def mar2():
    with open('restock-logs2021-02-28-to-2021-04-01.txt', 'r') as file:
        global txt
        txt = file.read()

def shop():
    restock_choice = "1"

def vend():
    restock_choice = "2"

def turret():
    restock_choice = "3"

def indexed():
    print_choice = "1"

def print_users():
    print_choice = "2"

def len_users():
    print_choice = "3"

def max_restocks():
    print_choice = "4"


def print_all():
    global restock_choice
    global print_choice
    print(txt)
    print(restock_choice)
    print(print_choice)
    
root = tk.Tk()

log_var = tk.IntVar()
restock_var = tk.IntVar()
print_var = tk.IntVar()

root.title('~~~~Program~~~~')

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

# background_image = tk.PhotoImage(file='landscape.png')
# background_label = tk.Label(root, image=background_image)
# background_label.place(relwidth=1, relheight=1)

frame = tk.Frame(root, bg='#80c1ff', bd=5)
frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.75, anchor='n')

label = tk.Label(frame, text="SLDARLMCaP", font=50, bg='#80c1ff', bd=2)
label.place(relx=0.1, relwidth=0.8, relheight=0.15)

r1 = tk.Radiobutton(frame, text = "March (week) logs", variable = log_var, value = 1, command = mar1)
r2 = tk.Radiobutton(frame, text = "February (week) logs", variable = log_var, value = 2, command = feb)
r3 = tk.Radiobutton(frame, text = "March (month) logs", variable = log_var, value = 3, command = mar2)

r1.place(rely=0.20)
r2.place(rely=0.30)
r3.place(rely=0.40)

nextb = tk.Button(frame, text="Print all []", font=30, bd=2, command=print_all)
nextb.place(relx=0.50, rely=0.50)

# Seperator object
separator = ttk.Separator(frame, orient='horizontal')
separator.place(rely=0.49, relwidth=0.5)

rc1 = tk.Radiobutton(frame, text = "Shop restocks ...", variable = restock_var, value = 4, command = shop)
rc2 = tk.Radiobutton(frame, text = "Vending restocks", variable = restock_var, value = 5, command = vend)
rc3 = tk.Radiobutton(frame, text = "Turret restocks", variable = restock_var, value = 6, command = turret)

rc1.place(rely=0.55)
rc2.place(rely=0.65)
rc3.place(rely=0.75)
#####################################################################
separator2 = ttk.Separator(frame, orient='horizontal')
separator2.place(rely=0.85, relwidth=0.5)

pc1 = tk.Radiobutton(frame, text = "Lists indexed restocks", variable = print_var, value = 7, command = indexed)
pc2 = tk.Radiobutton(frame, text = "Print all restocks", variable = print_var, value = 8, command = print_users)
pc3 = tk.Radiobutton(frame, text = "Total of all restocks", variable = print_var, value = 9, command = len_users)
pc4 = tk.Radiobutton(frame, text = "Most restocks", variable = print_var, value = 10, command = len_users)

pc1.place(rely=0.90)
pc2.place(rely=0.95)
pc3.place(relx=0.3, rely=0.90)
pc4.place(relx=0.3, rely=0.95)



# entry = tk.Entry(frame, font=40)
# entry.place(relwidth=0.65, relheight=1)

#button = tk.Button(frame, text="Get Weather", font=40)
#button.place(relheight=0.1, relwidth=0.3)

# lower_frame = tk.Frame(root, bg='#ff0000', bd=10)
# lower_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor='n')

# label = tk.Label(lower_frame)
# label.place(relwidth=1, relheight=1)

root.mainloop()
