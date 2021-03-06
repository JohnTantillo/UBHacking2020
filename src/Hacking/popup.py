import tkinter
import webbrowser
from tkinter import *
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure


import numpy as np


def administrative_popup(employee_name, array_of_hours):
    root = tkinter.Tk()
    root.wm_title("Hourly Work Percentages Breakdown of " + employee_name)
    fig = Figure(figsize=(5,5), dpi=100)
    a = fig.add_subplot(111)
   #print(array_of_hours["data"])
    a.plot(["9am", "10am", "11am", "12pm", "1pm", "2pm", "3pm","4pm"],array_of_hours["data"])

    a.set_ylabel('Percentage Makeup of the Days Productivity')
    a.set_xlabel('Hour')
    canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.

    canvas.draw()
    # pack_toolbar=False will make it easier to use a layout manager later on.
    toolbar = NavigationToolbar2Tk(canvas, root, pack_toolbar=False)
    toolbar.update()
    canvas.mpl_connect(
    "key_press_event", lambda event: print(f"you pressed {event.key}"))
    canvas.mpl_connect("key_press_event", key_press_handler)
    button = tkinter.Button(master=root, text="Quit", command=root.quit)
    button.pack(side=tkinter.BOTTOM)
    toolbar.pack(side=tkinter.BOTTOM, fill=tkinter.X)
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
    tkinter.mainloop()

def callback(url):
    webbrowser.open_new(url)

def hourly_popup(title, message, path):
    """Generate a pop-up window for special messages."""
    root = Tk()
    root.title(title)
    w = 400     # popup window width
    h = 200     # popup window height
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = (sw - w)/2
    y = (sh - h)/2
    root.geometry('%dx%d+%d+%d' % (w, h, x, y)) #basic layout of the window
    if(path == "survey"): #for the survey popup with the forum
        link2 = Label(root, text="\n\n" + message + "\n\n\n\n\n", fg="blue", cursor="hand2")
        link2.pack()
        link2.bind("<Button-1>", lambda e: callback("https://forms.gle/4U3zj3wGVwtXkHNw5"))
        b = Button(root, text="See you tomorrow!", command=root.destroy, width=25)
        b.pack()
    else:#layout of Generic text message you can see some examples bellow.
        m = message
        m += '\n'
        m += path
        w = Label(root, text=m, width=120, height=10)
        w.pack()
        b = Button(root, text="OK", command=root.destroy, width=10)
        b.pack()
    mainloop()
#Examples
#hourly_popup("Mental Health Report", "Seems Like You're Hitting A Rough Patch Go take a Break", "You're Doing Great - Josh")
#hourly_popup("You Doing Alright?", "Could you fill out this form? We just wanna check in with you.", "survey")
