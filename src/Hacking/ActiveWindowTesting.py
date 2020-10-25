import pygetwindow as gw

productivePrograms = ["intellij", "word", "excel", "powerpoint", "command prompt", "powershell"]

while True:
    win = gw.getActiveWindow()
    if win != None:
        if win.title != None:
            for program in productivePrograms:
                if program in win.title.lower():
                    print(win.title)
