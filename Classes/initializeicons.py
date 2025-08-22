from tkinter import *
from PIL import Image,ImageTk
class InitIcons():
    def __init__(self):

        self.PlayIcon = PhotoImage(file="Icons/Play.png")
        self.Playx16Icon = PhotoImage(file="Icons/Playx16.png")

        self.ResumeIcon = PhotoImage(file="Icons/Play.png")
        self.PauseIcon = PhotoImage(file="Icons/Pause.png")

        self.PreviousIcon = PhotoImage(file="Icons/Previous.png")
        self.Previousx16Icon = PhotoImage(file="Icons/Previousx16.png")

        self.NextIcon = PhotoImage(file="Icons/Next.png")
        self.Nextx16Icon = PhotoImage(file="Icons/Nextx16.png")

        self.StopIcon = PhotoImage(file="Icons/Stop.png")
        self.Stopx16Icon = PhotoImage(file="Icons/Stopx16.png")

        self.TogglePlaylistIcon = PhotoImage(file="Icons/TogglePlaylist.png")
        # self.TogglePlaylistSmallIcon = tk.PhotoImage(file="Icons/TogglePlaylist Small.png")
        self.AddFolderIcon = PhotoImage(file="Icons/AddFolder.png")
        self.AddFolderx16Icon = PhotoImage(file="Icons/AddFolderx16.png")

        self.FolderIcon = PhotoImage(file="Icons/Folder.png")
        self.FileIcon = PhotoImage(file="Icons/File.png")
        self.Filex16Icon = PhotoImage(file="Icons/Filex16.png")

        self.Fil = PhotoImage(file="Icons/Img.png")
        self.Sangeet_logo = PhotoImage(file="Icons/Sangeet Text.png")

        img = Image.open("Icons/SangeetLogo.png")
        res = img.resize((300,300))
        self.SangeetLogo = ImageTk.PhotoImage(res)
        
        self.LibraryIcon = PhotoImage(file="Icons/Library.png")
        self.DirectoryIcon = PhotoImage(file="Icons/Directory.png")

