from tkinter import *
import datetime
import webbrowser
import os
import pandas
from difflib import get_close_matches
from tkinter import ttk

#Create a class for an activity
class activity:
    def __init__(self, starttime, endtime, day, link, clipboard, file, name):
        self.starttime = starttime
        self.endtime = endtime
        self.day = day
        self.link = link
        self.clipboard = clipboard
        self.file = file
        self.name = name
    def open_link(self):
        if isinstance(self.link, str):
            return webbrowser.open(self.link)
    def open_file(self):
        if os.path.exists and isinstance(self.file, str):
            return os.system(self.file)
    def should_it_be_done(self):
        today =datetime.datetime.now()
        time = today.strftime("%H:%M:%S")
        day = today.strftime("%A")
        return self.day == day and str(self.starttime) <= time and str(self.endtime) >= time

def find_data():
    global data, name, starttime, endtime, day, link, clipboard, file
    data = pandas.read_excel("Data.xlsx")
    name = list(data["name"])
    starttime = list(data["starttime"])
    endtime = list(data["endtime"])
    day = list(data["day"])
    link = list(data["link"])
    clipboard = list(data["clipboard"])
    file = list(data["file"])

find_data()

#Start creating classes
classData = []
for n, s, e, d, l, c, f in zip(name, starttime, endtime, day, link, clipboard, file):
    classData.append(activity(str(s), str(e), d, l, c, f, n))

def autoMode():
    global classData
    for i in classData:
        if i.should_it_be_done():
            return (i.open_link())
    else:
        return ttk.Label(AutoMode, text = "You are free at the moment.").grid()

def manMode(na):
    global classData, name
    na = na.capitalize()
    try:
        na = get_close_matches(na, name)[0]
    except:
        ttk.Label(ManualMode, text = "This activity was not found").grid()
    for i in classData:
        if i.name == na:
            i.open_link()
            return i.open_file()

#Create Tkinter GUI stuff
root = Tk()
root.title("The Ultimate Automator. Developed by Rishi Murali")
root.geometry("500x500")

#Create two tabs
tabControl = ttk.Notebook(root)
AutoMode = ttk.Frame(tabControl)
ManualMode = ttk.Frame(tabControl)
tabControl.add(AutoMode, text='Automatic Mode')
tabControl.add(ManualMode, text='Manual Mode')
tabControl.pack(expand=1, fill="both")

#Create Automatic Mode stuff
RunButton = ttk.Button(AutoMode, text = "Run", command = autoMode)
RunButton.grid()
RefreshButton = ttk.Button(AutoMode, text = "Refresh", command = find_data)
RefreshButton.grid()

#Create Manual Mode stuff
InputBox = ttk.Entry(ManualMode)
InputBox.grid()
OpenButton = ttk.Button(ManualMode, text = "Run", command = lambda: manMode(InputBox.get()))
OpenButton.grid()
RefreshButton = ttk.Button(ManualMode, text = "Refresh", command = find_data)
RefreshButton.grid()

root.mainloop()