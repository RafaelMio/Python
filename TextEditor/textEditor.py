from tkinter import *
from tkinter import filedialog

filename = None

def newFile():
    global filename
    filename = "Untitled"
    text.delete(0.0, END)

def saveFile():
    global filename
    t = text.get(0.0, END)
    file = open(filename, 'w')
    file.write(t)
    file.close()

def saveAs():
    file = filedialog.asksaveasfilename(mode = 'w', defaultextension = '.txt')
    t = text.get(0.0, END)
    try:
        file.write(t.rstrip())
    except:
        filedialog.showerror(title="Erreur", message='Unable to save file')

def openFile():
    file = filedialog.askopenfile(mode = 'r')
    t = file.read()
    text.delete(0.0, END)
    text.insert(0.0, t)

root = Tk()
root.title("Python Text Editor")
root.minsize(width = 400, height = 400)
root.maxsize(width = 400, height = 400)

text = Text(root, width = 400, height = 400)
text.pack()

menuBar = Menu(root)
fileMenu = Menu(menuBar)
fileMenu.add_command(label = "New", command = newFile)
fileMenu.add_command(label = "Open", command = openFile)
fileMenu.add_command(label = "Save", command = saveFile)
fileMenu.add_command(label = "Save As", command = saveAs)
fileMenu.add_separator()
fileMenu.add_command(label = "Quit", command = root.quit)
menuBar.add_cascade(label = "File", menu = fileMenu)

root.config(menu = menuBar)
root.mainloop()
