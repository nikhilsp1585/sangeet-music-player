from os import sep
import tkinter as tk
from Classes.initializeicons import InitIcons
from Classes.classes import Hover

class ShowHide:
    def __init__(self,W1,Controller):
        self.w = W1
        self.ctrlr = Controller
    def show(self):
        self.w.grid()
        self.ctrlr.config(command=self.hide)
    def hide(self):
        self.w.grid_remove()        
        self.ctrlr.config(command=self.show)
        
class Sidebar:
    def __init__(self,master,parent):
        self.main = master
        self.parent = parent
        self.Icons = InitIcons()  
        
    def CreateSidebar(self):

        fg ="#b3b1b1"
        bg = "#1c1c1c"#"#121212"
        textlogocol = "#f2aa4cef"
        logotext_font = ("Helvetica",14,"bold") 
        heading_font = ("Helvetica",11,"bold") 
        body_font = ("Helvetica",10,"normal")

        self.Sidebar = tk.Frame(self.parent,bg=bg,relief='groove')
        self.Sidebar.pack(side='left',fill='both',expand=1)

        self.Sidebar.columnconfigure(0,weight=1)
        self.Sidebar.rowconfigure(8,weight=1)
        
        self.LogoText = tk.Label(self.Sidebar,anchor='center',bg=bg,image=self.Icons.Sangeet_logo,font=logotext_font)
        self.LogoText .grid(row=0,column=0,sticky='nsew',pady=5)

        self.Library = tk.Button(self.Sidebar,image=self.Icons.LibraryIcon,activebackground=bg,activeforeground=fg,compound="left",cursor="hand2",relief='flat',bd=0,anchor='w',fg=fg,bg=bg,text="Library",font=heading_font)
        self.Library.grid(row=3,column=0,sticky='nsew',padx=20,pady=(10,0))
        Hover(self.Library,onlyfg="white")
              
        self.DirectoryText = tk.Button(self.Sidebar,anchor='w',activebackground=bg,activeforeground=fg,image=self.Icons.DirectoryIcon,cursor="hand2",compound="left",fg=fg,bg=bg,bd=0,text="Directory",font=heading_font)
        self.DirectoryText.grid(row=6,column=0,sticky='nsew',padx=20)
        Hover(self.DirectoryText,onlyfg="white")

        self.DirectoryTray = tk.Frame(self.Sidebar,bg=bg)
        self.DirectoryTray.grid(row=7,column=0,sticky='nsew',padx=45,pady=(0,4))
        self.DirectoryTray.grid_remove()

        self.showhide = ShowHide(self.DirectoryTray,Controller=self.DirectoryText)
        self.DirectoryText.config(command=self.showhide.show)

        self.MyMusic = tk.Button(self.DirectoryTray,anchor='w',text="My Music",bg=bg,font=body_font,fg=fg,compound='left',image=self.Icons.FolderIcon,relief='flat',bd=0,borderwidth=0,cursor='hand2')
        self.MyMusic.grid(row=0,column=0,sticky='nsew')
        Hover(self.MyMusic,onlyfg="white")

        self.SidebarCoverFrame = tk.Frame(self.Sidebar,height=180,width=180,bg=bg)
        self.SidebarCoverFrame.grid_propagate(0)
        self.SidebarCoverFrame.grid(row=8,column=0,padx=15,pady=15,sticky='s')

        self.SidebarCoverFrame.rowconfigure(0,weight=1)

        self.SidebarCover = tk.Label(self.SidebarCoverFrame,bg=bg)
        self.SidebarCover.grid(row=0,column=0,sticky="nsew")

        
        # self.SidebarCover.grid_remove()