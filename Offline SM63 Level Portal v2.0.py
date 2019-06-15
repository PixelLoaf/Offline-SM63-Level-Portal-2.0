from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.messagebox import *
import pickle

VERSION = "2.1.0"

TITLE = "Offline SM63 Level Portal"

main = Tk()

main.title(TITLE)

file = pickle.load(open("database.pickle", "rb"))

levels = file["codes"]

levelCodes = file["ids"]

searchScope = levelCodes[:]

outText = None

scroll = None

def outputLevel(*args):
    level = levels[searchScope[outText.curselection()[0]][0]]
    try:
        import pyperclip
        pyperclip.copy(level)
    except:
        import subprocess
        subprocess.Popen("clip", stdin = subprocess.PIPE).communicate(level.encode())
    showinfo(TITLE, "Copied level code to clipboard!")
        
def reset():
    global outText, scroll, searchScope
    outText.destroy()
    scroll.destroy()
    resetButton.destroy()
    searchScope = levelCodes[:]
    outText = None
    scroll = None
    searchButton.config(text = "Search")

def search():
    
    global outText, scroll, searchScope
    
    if outText is not None:
        outText.destroy()
        scroll.destroy()
    else:
        searchButton.config(text = "Refine search")
        global resetButton
        resetButton = Button(searchButtonsFrame, text = "Reset search", command = reset, fg = "#FF0000")
        resetButton.pack(side = RIGHT)        
    
    results = []
    
    searchTerm = searchEntry.get()
    
    for i in searchScope:
        if any(searchTerm.lower() in j.lower() for j in i[1:3]):
            results.append(i)
    
    searchScope = results
    
    outText = Listbox(display, width = 75, height = min(len(results), 15))
    outText.pack(side = LEFT, fill = BOTH)
    
    outText.bind("<Double-1>", outputLevel)
    
    scroll = Scrollbar(display, orient = "vertical")
    scroll.config(command = outText.yview)
    scroll.pack(side = RIGHT, fill = Y)

    outText.config(yscrollcommand = scroll.set)

    [outText.insert(END, "{} by {}".format(i[1], i[2])) for i in results]
    
searchFrame = Frame(main)
searchFrame.pack()

searchLabel = Label(searchFrame, text = "Search term:")
searchLabel.pack(side = LEFT)

searchSubFrame = Frame(searchFrame)
searchSubFrame.pack(side = RIGHT)

searchEntry = Entry(searchSubFrame)
searchEntry.pack(side = LEFT)

searchButtonsFrame = Frame(searchSubFrame)
searchButtonsFrame.pack(side = RIGHT)

searchButton = Button(searchButtonsFrame, text = "Search", command = search)
searchButton.pack(side = LEFT)

display = Frame(main)
display.pack()

main.mainloop()