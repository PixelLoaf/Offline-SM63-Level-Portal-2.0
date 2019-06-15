from tkinter import Button, Entry, Frame, Label, Listbox, Scrollbar, Tk, BOTH, END, LEFT, RIGHT, Y
from tkinter.scrolledtext import ScrolledText
from tkinter.messagebox import showinfo
from pickle import load

VERSION = "2.2.0"

TITLE = "Offline SM63 Level Portal"

class App(Tk):

    def __init__(self):
        Tk.__init__(self)
        
        self.title(TITLE)
        self.db = load(open("database.pickle", "rb"))
        self.codes = self.db["codes"]
        self.ids = self.db["ids"]
        self.searchScope = self.ids[:]
        self.outText = None
        self.scroll = None
        self.resetButton = None
        
        self.searchFrame = Frame(self)
        self.searchFrame.pack()
        
        self.searchLabel = Label(self.searchFrame, text = "Search term:")
        self.searchLabel.pack(side = LEFT)
        
        self.searchSubFrame = Frame(self.searchFrame)
        self.searchSubFrame.pack(side = RIGHT)
        
        self.searchEntry = Entry(self.searchSubFrame)
        self.searchEntry.pack(side = LEFT)
        
        self.searchButtonsFrame = Frame(self.searchSubFrame)
        self.searchButtonsFrame.pack(side = RIGHT)
        
        self.searchButton = Button(self.searchButtonsFrame, text = "Search", command = self.search)
        self.searchButton.pack(side = LEFT)
        
        self.display = Frame(self)
        self.display.pack()        

    def outputLevel(self, *args):
        level = self.codes[self.searchScope[self.outText.curselection()[0]][0]]
        try:
            import pyperclip
            pyperclip.copy(level)
        except:
            import subprocess
            subprocess.Popen("clip", stdin = subprocess.PIPE).communicate(level.encode())
        showinfo(TITLE, "Copied level code to clipboard!")
        
    def reset(self):
        self.outText.destroy()
        self.scroll.destroy()
        self.resetButton.destroy()
        self.searchScope = self.ids[:]
        self.outText = None
        self.scroll = None
        self.searchButton.config(text = "Search")

    def search(self):
        
        if self.outText is not None:
            self.outText.destroy()
            self.scroll.destroy()
        else:
            self.searchButton.config(text = "Refine search")
            
            self.resetButton = Button(self.searchButtonsFrame, text = "Reset search", command = self.reset, fg = "#FF0000")
            self.resetButton.pack(side = RIGHT)        
        
        results = []
        
        searchTerm = self.searchEntry.get()
        
        for i in self.searchScope:
            if any(searchTerm.lower() in j.lower() for j in i[1:3]):
                results.append(i)
        
        self.searchScope = results
        
        self.outText = Listbox(self.display, width = 75, height = min(len(results), 15))
        self.outText.pack(side = LEFT, fill = BOTH)
        
        self.outText.bind("<Double-1>", self.outputLevel)
        
        self.scroll = Scrollbar(self.display, orient = "vertical")
        self.scroll.config(command = self.outText.yview)
        self.scroll.pack(side = RIGHT, fill = Y)
    
        self.outText.config(yscrollcommand = self.scroll.set)
    
        [self.outText.insert(END, "{} by {}".format(i[1], i[2])) for i in results]

App().mainloop()