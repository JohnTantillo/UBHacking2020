import tkinter as tk
from Hacking import popup, database

def sendName():
    popup.administrative_popup(name.get(), database.get_worker(name.get()))
    # TODO: Write code



window = tk.Tk()
w = 400     # popup window width
h = 200     # popup window height
sw = window.winfo_screenwidth()
sh = window.winfo_screenheight()
x = (sw - w)/2
y = (sh - h)/2
window.geometry('%dx%d+%d+%d' % (w, h, x, y))
label = tk.Label(text="Name:")
name = tk.Entry(
    text="Enter Name Here!",
    width=25
)

submit = tk.Button(
    text="Submit",
    width=25,
    command=sendName
)
label.pack()
name.pack()
submit.pack()
window.mainloop()
