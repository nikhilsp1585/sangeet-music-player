 
from tkinter import *
from tkinter import ttk,filedialog,messagebox
from Classes.initializeicons import InitIcons

class Menubar(Menu):
    def __init__(self,master):
        self.main = master
        Menu.__init__(self,master=master,bd=0,bg="black",fg="white")
        self.Icons = InitIcons()
        self.ShuffleCheckValue = BooleanVar()
        self.initMenus()
        self.assignMenustoMenubar()

    def initMenus(self):
        selectcolor = '#3297fd'
        font = None
        
        #File Menu
        self.FileMenu = Menu(tearoff=False,relief='flat', bd=0,activebackground=selectcolor,activeborderwidth=0,font=font)  
        #Playback Menu
        self.PlaybackMenu = Menu(tearoff=False,relief='flat', bd=0,activebackground=selectcolor,activeborderwidth=0,font=font)
        #Audio Menu
        self.AudioMenu = Menu(tearoff=False,relief='flat', bd=0,activebackground=selectcolor,activeborderwidth=0,font=font)
        #Settings Menu
        self.SettingsMenu = Menu(tearoff=False,relief='flat', bd=0,activebackground=selectcolor,activeborderwidth=0,font=font)
        #Help Menu
        self.HelpMenu = Menu(tearoff=False,relief='flat', bd=0,activebackground=selectcolor,activeborderwidth=0,font=font)

    def assignMenustoMenubar(self):
        #add menus to menubar
        self.add_cascade(label="File",menu=self.FileMenu)
        self.add_cascade(label="Playback",menu=self.PlaybackMenu)
        self.add_cascade(label="Audio",menu=self.AudioMenu)
        self.add_cascade(label="Settings",menu=self.SettingsMenu)
        self.add_cascade(label="Help",menu=self.HelpMenu)

    def getShuffleCheckValue(self):
        return self.ShuffleCheckValue.get()
