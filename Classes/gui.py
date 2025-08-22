import tkinter as tk
from tkinter import *
from tkinter import ttk,filedialog,messagebox
from PIL import Image,ImageTk
# from CTSeparator import ctseparator
from .classes import Hover
from .initializeicons import InitIcons
from .menubar import Menubar
from .sidebar import Sidebar
from .treeview import Treeview
from .playbackbar import PlaybackBar

class GraphicalUserInterface:
    
    def __init__(self,master,style):
        self.main = master
        self.TopVar = tk.StringVar()
        self.Theme = style
      
    def CreateUserInterface(self):

        self.Icons = InitIcons()


        self.Theme.configure('sp.Horizontal.TSeparator',background='white',foreground='gray60',height=2)

        fg = "#3297fd"
        bg = "white"
        body_font = ("quicksand",11,"bold")

        # Main Menu
    
        self.Menubar = Menubar(self.main)
        
        self.main.config(menu=self.Menubar)

        #Playbackbar

        # -------------------------------------------- # Main Screen # -------------------------------------------------------------------------------
        self.MainScreen = tk.Frame(self.main,bg="black")
        self.MainScreen.pack(side=TOP,fill=BOTH,expand=1)
        self.MainScreen.rowconfigure(0,weight=1)
        self.MainScreen.columnconfigure(0,weight=1)
        
        self.AlbumArtFrame = tk.Frame(self.MainScreen,bg="black",width=300,height=300)
        self.AlbumArtFrame.grid_propagate(0)
        self.AlbumArtFrame.grid(row=0,column=0) #padx=490,pady=90

        self.AlbumArtFrame.rowconfigure(0,weight=1)
        self.AlbumArtFrame.columnconfigure(0,weight=1)
    
      

        self.AlbumArt = tk.Label(self.AlbumArtFrame,image=self.Icons.SangeetLogo,bg="black")
        self.AlbumArt.photo = self.Icons.SangeetLogo
        self.AlbumArt.grid(sticky="nsew") 
   
        # -------------------------------------------- # Playlist Screen # --------------------------------------------------------------------------------------
        self.PlaylistScreen = tk.Frame(self.main,bg="white")
        self.PlaylistScreen.pack(side=TOP,fill=BOTH,expand=1)
        self.PlaylistScreen.pack_forget()

        # PanedWindow # (Main/PlaylistScreen/PanedWin) --------------------------------------------------------------------------------------------------
    
        self.PanedWin = tk.PanedWindow(self.PlaylistScreen,sashwidth=0,bg="white",sashrelief="flat",bd=0,relief='flat')
        self.PanedWin.pack(side="top",fill="both",expand=1)
        #Sidebar Frame & its Child Widgets ----------------
        
        self.SidebarFrame = tk.Frame(self.PanedWin)
        self.SidebarFrame.pack(side="left")

        self.Sidebar = Sidebar(master=self.main,parent=self.SidebarFrame)
        self.Sidebar.CreateSidebar()

        # ttk.Separator(Sidebar,orient='horizontal',style='sp.TSeparator').grid(row=4,column=0,sticky='w',padx=5,ipadx=100)

        #TreeView Frame & its Child Widgets ----------------
    
        self.ContainerFrame = tk.Frame(self.PanedWin,bg="white")
        self.ContainerFrame.pack(side='top',fill="both")

        self.TopLabel = tk.Label(self.ContainerFrame,bg='white',fg='black',font=("quicksand",28,"normal"),text=" Library",height=1,anchor="w")
        self.TopLabel.pack(side='top',fill='x',padx=(14,0))

        self.ToolbarFrame = tk.Frame(self.ContainerFrame,bg="white",height=3)
        self.ToolbarFrame.pack(side="top",fill="both",expand=1,padx=(14,0))

        self.LibraryTray = tk.Frame(self.ToolbarFrame,bg=bg)
        self.LibraryTray.pack(side="left",fill="x",padx=(14,0))

        self.AddFolderBtn = tk.Button(self.LibraryTray,anchor='w',bg=bg,text="+ Folder",font=body_font,fg=fg,relief='flat',activebackground=bg,activeforeground=fg,bd=0,borderwidth=0,cursor='hand2')
        self.AddFolderBtn.grid(row=0,column=0)
        Hover(self.AddFolderBtn,onlyfg="gray45")
        
        self.AddFile = tk.Button(self.LibraryTray,anchor='w',bg=bg,text="+ Files",font=body_font,fg=fg,compound='left',relief='flat',bd=0,activebackground=bg,activeforeground=fg,borderwidth=0,cursor='hand2')
        self.AddFile.grid(row=0,column=1,padx=(15,0))
        Hover(self.AddFile,onlyfg="gray45")       

        self.TreeViewFrame = tk.Frame(self.ContainerFrame,bg="white")
        self.TreeViewFrame.pack(side='top',fill="both",expand=1,padx=(14,0))

        self.Tree = Treeview(self.TreeViewFrame,self.Theme)
        self.Tree.initTree()
        self.Tree.TreeView.pack(side='top',fill="both",expand=1) 
            
        self.Playbackbar = PlaybackBar(self.main,theme=self.Theme)
        self.Playbackbar.CreatePlaybackBar()

        self.PanedWin.paneconfig(self.SidebarFrame,minsize=200)
        self.PanedWin.paneconfig(self.ContainerFrame,minsize=1000)

        self.PanedWin.add(self.SidebarFrame)
        self.PanedWin.add(self.ContainerFrame)


