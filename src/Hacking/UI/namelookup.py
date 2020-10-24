import tkinter as tk

def sendName():
    print(name.get())
    # TODO: Write code


window = tk.Tk()
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
