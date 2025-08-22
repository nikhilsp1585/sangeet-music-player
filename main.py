from Classes.initializeicons import InitIcons
from tkinter import *
from tkinter import ttk
from Classes.classes import FileOperations, Player
from Classes.gui import GraphicalUserInterface
import pygame

def SwitchBetween(frame_from,frame_to,event=None):

    global CurrentFrame
    
    if CurrentFrame=='Main':
        frame_from.pack_forget()
        frame_to.pack(side=TOP,fill=BOTH,expand=1)
        CurrentFrame = 'Pla'

    else:
        frame_to.pack_forget()
        frame_from.pack(side=TOP,fill=BOTH,expand=1)
        CurrentFrame='Main' 
def play(e=None):
    global isplaying
    try:
        player.play()
    except TypeError:
        print("Select any music file.")
    isplaying = pygame.mixer.music.get_busy()
    print(isplaying)
def pause():
    if isplaying:
        player.pause()
def resume():
    if isplaying:
        player.resume()
def stop():
    if isplaying:
        player.stop()
def Next():
    if isplaying:
        player.ShuffleOrNext(gui.Menubar.getShuffleCheckValue())
def Previous():
    if isplaying:
        player.Previous()
def slide(e):
    if isplaying:
        player.slide()

def getCurSel(e):
    sel = None
    c = player.curselection()
    sel =c
    return sel

def handle_resize(event):
    column = gui.Tree.TreeView.identify_column(event.x) 
    if gui.Tree.TreeView.identify_region(event.x, event.y)=="nothing":
        
        gui.Tree.TreeView.selection_clear()

    elif gui.Tree.TreeView.identify_region(event.x, event.y)=="separator":
        if column == "#3":
            return "break"

def contextMenu(event):
    global lid
    tree = gui.Tree.TreeView
    cid = tree.identify("item",event.x,event.y)
    tree.selection_set(cid)
    lid = Menu(tree,tearoff=False)
    lid.add_command(label="DELETE")
    lid.post(event.x_root,event.y_root)

def rmvContextMenu(event):
    
    lid.destroy()

if __name__ == "__main__":

    main = Tk()
    main.geometry('1355x698')
    main.title('Sangeet music player')
    # main.iconbitmap("Icons/Sangeet.ico")
    main.minsize(width=500,height=500)

    pygame.init()
    icons = InitIcons()
    
    #Define Variables
    PlaybacksList = {}
    CurrentFrame = 'Main'
    ShuffleCheckValue = BooleanVar()
    isplaying = False

    style = ttk.Style(main)

    img_trough = PhotoImage(file="through.png",name="img_trough",master=main)
    img_slider = PhotoImage(file="slider.png",name="img_slider",master=main)

    style.element_create('custom.Scale.trough', 'image', "img_trough")
    style.element_create('custom.Scale.slider', 'image', "img_slider")
    style.layout('custom.Horizontal.TScale',[('custom.Scale.trough', {'sticky': 'ew'}),
                                                        ('custom.Scale.slider',{'side': 'left', 'sticky': '',})
                                                    ])

    style.configure("custom.Horizontal.TScale",background="#f4f4f4")

    gui = GraphicalUserInterface(main,style=style)
    gui.CreateUserInterface()
    gui.Menubar.config(bg = "GREEN",fg='white',activebackground='red',activeforeground='purple',activeborderwidth=0,font=("Verdana", 12))

    widgets = {"AlbumArt":gui.AlbumArt,"SidebarCover":gui.Sidebar.SidebarCover,"TopLabel":gui.TopLabel}

    fileOperations = FileOperations(master = main,loadingdisplaywidget = gui.TopLabel ,Treeview=gui.Tree.TreeView,PlaybacksList=PlaybacksList)
    gui.AddFolderBtn["command"] = fileOperations.addFolder
    gui.AddFile["command"] = fileOperations.addFiles

    player = Player(main,gui.Tree.TreeView,PlaybackList=PlaybacksList)
    player.setWidgets(widget=widgets)
    player.setvar(startvar = gui.Playbackbar.Startvar,endvar = gui.Playbackbar.Endvar,checkvar=ShuffleCheckValue.get())
    player.setSliders(progress=gui.Playbackbar.ProgressSlider,volumeslider=gui.Playbackbar.VolVar)
    player.setw1w2(w1 =gui.Playbackbar.PlayButton, w2= gui.Playbackbar.PauseButton)

    gui.Menubar.PlaybackMenu.add_checkbutton(label="  Shuffle",variable=ShuffleCheckValue,selectcolor="#3297FD",offvalue=0,onvalue=1)

    gui.Menubar.PlaybackMenu.add_command(label="  Play",command=play,compound="left",image=icons.Playx16Icon)
    gui.Menubar.PlaybackMenu.add_command(label="  Stop",command=stop,compound="left",image=icons.Stopx16Icon)
    gui.Menubar.PlaybackMenu.add_command(label="  Next",command=Next,compound="left",image=icons.Nextx16Icon)
    gui.Menubar.PlaybackMenu.add_command(label="  Previous",command=Previous,compound="left",image=icons.Previousx16Icon)
    
    gui.Menubar.FileMenu.add_command(label="+  Open Files",command=fileOperations.addFiles)
    gui.Menubar.FileMenu.add_command(label="+  Open Folder",command=fileOperations.addFolder)

    gui.Playbackbar.TogglePlaylistButton["command"] = lambda : SwitchBetween(frame_from=gui.MainScreen,frame_to=gui.PlaylistScreen)
    gui.Playbackbar.PlayButton.config(command=play) 
    gui.Playbackbar.NextButton.config(command=Next) 
    gui.Playbackbar.PreviousButton.config(command=Previous) 
    gui.Playbackbar.PauseButton.config(command=pause) 
    gui.Playbackbar.StopButton.config(command=stop) 
    gui.Playbackbar.ProgressSlider.config(command=slide)
    gui.Playbackbar.VolumeSlider.config(command=player.volumeController)

    gui.Tree.TreeView.bind("<<TreeviewSelect>>",getCurSel)
    gui.Tree.TreeView.bind("<Button-1>",handle_resize)
    gui.Tree.TreeView.bind("<Double-Button-1>",play)
    gui.Tree.TreeView.bind("<Button-3>",contextMenu)
    gui.Tree.TreeView.bind("<ButtonRelease-3>",contextMenu)
    main.config(bg="white")
    main.mainloop()
