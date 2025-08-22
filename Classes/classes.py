from os.path import abspath
from tkinter import *
from tkinter import filedialog,messagebox,ttk
from tkinter.ttk import Progressbar
from mutagen.mp3 import MP3
from .initializeicons import InitIcons
from PIL import ImageTk,Image
import pygame
import stagger,datetime,io,os,threading,random,sys

class CustomScale(ttk.Scale):
    def __init__(self, master=None, **kw):
        kw.setdefault("orient", "vertical")
        ttk.Scale.__init__(self, master, **kw)
        self._style_name = '{}.custom.{}.TScale'.format(self, kw['orient'].capitalize())
        self['style'] = self._style_name


class Hover():
    def __init__(self,widget,onlyfg):
        # Have to chnage the if statement condition | Change the onlyfg var boolean to str
        self.wid = widget
        self.onlyfg =onlyfg
        self.defaultbg = self.wid.cget("bg")
        self.defaultfg = self.wid.cget("fg")
        # self.defaultFont = self.wid.cget("font")
        print(self.wid.cget("text"))
        self.wid.bind("<Enter>",self.enter)
        self.wid.bind("<Leave>",self.leave)

    def enter(self,e):
        if self.onlyfg == "":
            self.wid["bg"] = "#3297fd"
        
        self.wid["fg"] = self.onlyfg

    def leave(self,e):
        if not self.onlyfg:
        
            self.wid["bg"] = self.defaultbg

        self.wid["fg"] = self.defaultfg
        
class Thread():
    def __init__(self,callback):
        self.callback = callback
    def run(self):
        threading.Thread(target=self.callback).start()

class Metadata():

    def __init__(self):

        self.MusicTitle = None
        self.MusicAlbum=None
        self.MusicArtist=None
        self.MusicDuration=None

    def getCoverArt(self,Musicfile,alpha=None):
        MusicFileData = stagger.read_tag(Musicfile)
        BytesData = MusicFileData[stagger.id3.APIC][0].data 
        IoBytes = io.BytesIO(BytesData)
        ImageFile = Image.open(IoBytes)
        if alpha!=None:
            print("donnnene")
            ImageFile.putalpha(alpha=alpha)
        if ImageFile.height < 300:
            CoverArt = ImageTk.PhotoImage(ImageFile.resize((300,150)))
            SideCoverArt = ImageTk.PhotoImage(ImageFile.resize((180,90)))
        elif ImageFile.height >= 300:
            CoverArt = ImageTk.PhotoImage(ImageFile.resize((300,300)))
            SideCoverArt = ImageTk.PhotoImage(ImageFile.resize((180,180)))
        return CoverArt,SideCoverArt

    def getMetadata(self,MusicFile):
        
        self.MusicData = stagger.read_tag(MusicFile)
        self.DurationData = MP3(MusicFile)

        self.MusicTitle = self.MusicData.title
        
        self.MusicAlbum = self.MusicData.album
        self.MusicArtist = self.MusicData.artist
        self.MusicDuration = int(self.DurationData.info.length)
        self.CoverArt = self.getCoverArt(MusicFile)[0]
        self.SideCoverArt = self.getCoverArt(MusicFile)[1]

        self.Metadata = {"Title":self.MusicTitle,"Album":self.MusicAlbum,"Artist":self.MusicArtist,"Duration":self.MusicDuration,"CoverArt":self.CoverArt,"SideCoverArt":self.SideCoverArt}
        
        return self.Metadata
        
class FileOperations():
    def __init__(self,master,loadingdisplaywidget,Treeview,PlaybacksList):
        self.main = master
        self.Path = None
        self.Files = None
        self.ldw =  loadingdisplaywidget
        self.FolderIcon = InitIcons().FolderIcon
        self.FileIcon = InitIcons().FileIcon
        self.TreeView = Treeview
        self.PlaybacksList = PlaybacksList
        self.count = 0

    def getFolder(self): #A function to get a Folder from user through GUI Directory chooser provided by tkinter.
        try:
            #open directory chooser for user to select directory.
            FolderDir = filedialog.askdirectory(title='Select Music Folder')
            return FolderDir #Return that Folder Directory path which is selected by user before.
        except OSError: # Catch the exception if the user not select any directory or select invalid directory.
            messagebox.showerror(title="Invalid Folder Path",message="Please Select valid folder Path")
            #Show the Error through tkinter Messagebox to gui Window to user.
            return None #Return None if this function use in any other function or class so that ValueError stop to occurs.
    
    def getFiles(self): #A function to get a files from user through GUI Directory chooser provided by tkinter.
        try:
            #open files chooser for user to select directory.
            Files = filedialog.askopenfilenames(title='Please select music files',
                           filetypes=[('MP3 Files', ".mp3"),("WAV Files",".wav"),("All Files",".*")])
            # FilesList=list(Files)
            return Files #Return that files list which is selected by user before.
        except OSError: # Catch the exception if the user not select any file/files or select invalid file.
            messagebox.showerror(title="Invalid Selection",message="Please Select valid file/files to add")
            #Show the Error through tkinter Messagebox to gui Window to user.
            return None #Return None if this function use in any other function or class so that ValueError stop to occurs.
    
    def addParentPathNode(self,path,count):
        parentName = os.path.basename(path)
        if self.count%2==0:
            Parent = self.TreeView.insert('','end',text=parentName,value=(path,"",""),image=self.FolderIcon,tags=('even',))
            self.count+=1
        else:
            Parent = self.TreeView.insert('','end',text=parentName,value=(path,"",""),image=self.FolderIcon,tags=('odd',))
            self.count+=1
        return Parent

    def addChildFileNode(self,parent,values:tuple,count):
        if self.count%2==0:
            self.TreeView.insert(parent,'end',value=(values[0],values[1],values[2]),image = self.FileIcon,tags=("even",))
            self.count+=1
        else:
            self.TreeView.insert(parent,'end',value=(values[0],values[1],values[2]),image = self.FileIcon,tags=("odd",))
            self.count+=1

    def readAndSetData(self,path=None,parent=None,playlst=None):
        #A function to read data of file items of the given folder path
        self.ldw.config(text=" Loading...please wait..")
        playlist = []

        if playlst != None:
            for items in playlst:
                # if items.endswith((".mp3",".wav")):
                    
                playlist.append(items)
        
        else:
            for items in os.listdir(path):
                if items.endswith((".mp3",".wav")):
                    playlist.append(items)

        if path!= None:
            os.chdir(path)
            parentDir = f"{os.path.basename(path)}"
            if parent==None:
                Parent = self.addParentPathNode(path=path,count=self.count)
            else:
                Parent = parent
        else:
            parentDir= ''
            Parent = ''
     
        Mdata = Metadata()
        self.main.update_idletasks()
        
        for items in playlist:
            try:
                durationSec = Mdata.getMetadata(items)["Duration"]
                duration = datetime.timedelta(seconds=int(durationSec))
                artist = Mdata.getMetadata(items)["Artist"]
                
                self.addChildFileNode(parent=Parent,values=(items,duration,artist),count=self.count)
               
                    
            except Exception as e:
                if e == stagger.EmptyFrameWarning or e == stagger.Error:
                    print(stagger.Error().args())
                    print("error")
                else:
                    print(e)
            finally:
                self.ldw.config(text=f" Library")
        self.PlaybacksList[parentDir] =playlist
          
    def addFolder(self,path=''):# A function to read data of got folder and add that data to Gui Treeview
        if path == '':
            self.Path = self.getFolder()
        else:
            self.Path = path
        
        if self.Path != None:
            absPath = os.path.abspath(self.Path)
            threading.Thread(target=self.readAndSetData(absPath)).start()

    
    def addFiles(self,files=None):
        if files == None:
            self.Files = self.getFiles()
        else:
            self.Files = files
        
        if self.Files != None:
            threading.Thread(target=self.readAndSetData(playlst=self.Files)).start()          
    
class Player():
    def __init__(self,master,Treeview,PlaybackList):
        self.Main = master
        self.TreeView = Treeview
        self.PlaybacksList = PlaybackList

        self.AlbumArt = None
        self.SidebarCover = None
        self.TopLabel = None

        self.w1 = None
        self.w2 = None

        self.endvar = None
        self.startvar = None
        self.checkvar = None
        self.curSelectionIndex = 0

        self.paused = False
        self.ProgressSlider = None
        self.progress_id = None
        self.VolumeSlider = None

        self.Player = pygame.mixer_music

        # self.Player.init()

    def curselection(self):
        try:

            for selection in self.TreeView.selection():
                selectedItemId = selection
                selectedItemValue = self.TreeView.item(selectedItemId)
                selectedItem = selectedItemValue['values'][0]

                parent = self.TreeView.parent(selectedItemId) #Find Parent of selectedItem

                self.curSelectionIndex =  self.PlaybacksList[self.TreeView.item(parent)["text"]].index(selectedItem)
                # print(type(self.curSelectionIndex))

                selectedItemInfo = {"selectedItemId":selectedItemId,"selectedItem" : selectedItem,"selectedItemParent":parent}
                return selectedItemInfo
            
        except Exception as e :
            print(f"currseerror{e}")      

    def setCoverArt(self,image:ImageTk.PhotoImage,sideimage:ImageTk.PhotoImage):

        self.im = image
        self.sideim = sideimage

        self.AlbumArt.config(image=self.im)
        self.AlbumArt.image = self.im

        self.SidebarCover.config(image=self.sideim)
        self.SidebarCover.image = self.sideim
    
    def removeCoverArt(self):
        self.AlbumArt.config(image="")
        self.SidebarCover.config(image="")

    def setw1w2(self,w1,w2):
        self.w1 = w1
        self.w2 = w2

    def setvar(self,startvar,endvar,checkvar):
        self.startvar = startvar
        self.endvar = endvar
        self.checkvar = checkvar

    def setSliders(self,progress,volumeslider):
        self.ProgressSlider = progress
        self.VolumeSlider = volumeslider

    def setWidgets(self,widget:dict):
        if widget:
            self.AlbumArt = widget["AlbumArt"]
            self.SidebarCover = widget["SidebarCover"]
            self.TopLabel = widget["TopLabel"]

    def setstarttime(self,time):
        convtime = datetime.timedelta(seconds=int(time))
        if convtime!=0: 
            self.startvar.set(convtime)
        else:
            self.startvar.set("0:00:00")
        
    def setendtime(self,musicfile):
        endtimedata = Metadata().getMetadata(musicfile)["Duration"]
        self.endtime = datetime.timedelta(seconds=int(endtimedata))
        self.endvar.set(self.endtime)
        self.ProgressSlider['to'] = endtimedata
    
    def StartProgress(self):
        total_length = self.ProgressSlider["to"]
        real_pos = int(self.Player.get_pos()/1000)
        slider_pos = int(self.ProgressSlider.get())
        # print(f"Real Pos : {real_pos} , Slider Pos : {slider_pos}")

                    
        if not (slider_pos==total_length) and not self.paused:
            self.ProgressSlider.config(value=slider_pos)
            self.setstarttime(slider_pos)
            next_pos =  int(self.ProgressSlider.get()) + 1
            self.ProgressSlider.config(value=next_pos)


        # elif (real_pos==slider_pos):
        self.progress_id = self.ProgressSlider.after(1000,self.StartProgress)
        #     self.ProgressSlider.config(value=slider_pos)
        #     self.setstarttime(slider_pos)
        #     next_pos =  slider_pos + 1
        #     self.ProgressSlider.config(value=next_pos)
        if (slider_pos==total_length):
            self.StopProgress()
            self.ShuffleOrNext(self.checkvar)
        #     print("Same!
    def StopProgress(self):
        self.ProgressSlider.after_cancel(self.progress_id)
        self.Player.stop()

        self.ProgressSlider.config(value=0)
        self.setstarttime(0)
        self.removeCoverArt()
    def playmusic(self,musicfile,parent,stime=None): 

        # print(parent)
        # print(parent != "")
        self.w1.grid_remove()
        self.w2.grid()
        # self.Main.title(f"{selectedItem}")

        if parent!='':
            folderName = (self.TreeView.item(parent)["text"]) 
            '''get the foldername of parent for exact same
                selected song to search in related added folder playlist from the dictionary
                which contains all added folders.'''
            folderPath = (self.TreeView.item(parent)["values"][0]) 
            '''get the folder path to play audio from where the file is.'''
            os.chdir(folderPath)
        else:
            folderName = ''
            folderPath = ''
        '''change the cwd to folderPath'''
        # self.curSelectionIndex =  self.PlaybacksList[folderName].index(musicfile)
        # musicF = self.PlaybacksList[folderName][self.curSelectionIndex]
        self.Player.load(musicfile)
        if stime==None:
            self.Player.play()
            print(stime)
        else:
            self.Player.play(start=stime)
            print(stime)
        self.Main.title(musicfile)
        CoverArt = Metadata().getMetadata(self.PlaybacksList[folderName][self.curSelectionIndex])["CoverArt"]
        SideCoverArt = Metadata().getMetadata(self.PlaybacksList[folderName][self.curSelectionIndex])["SideCoverArt"]
        self.setCoverArt(image=CoverArt,sideimage=SideCoverArt)
        self.setendtime(musicfile)
        self.StartProgress()

    
    def slide(self):
        self.ProgressSlider.after_cancel(self.progress_id)
        parent = self.curselection()["selectedItemParent"]
        selectedItem = self.curselection()["selectedItem"]
        stime = int(self.ProgressSlider.get())
        self.playmusic(musicfile=selectedItem,parent=parent,stime=stime)
        # self.Player.set_pos(stime)
        self.setstarttime(stime)
    
    def play(self):
        if self.Player.get_busy():
            self.StopProgress()
        parent = self.curselection()["selectedItemParent"]
        selectedItem = self.curselection()["selectedItem"]
        self.w1.grid_remove()
        self.w2.grid()

        self.playmusic(musicfile=selectedItem,parent=parent)

    def resume(self):
        self.Player.unpause()
        self.w1.grid_remove()
        self.w2.grid()
        self.paused=False

    def pause(self):
        self.Player.pause()
        self.w2.grid_remove()
        self.w1.grid()
        self.w1.config(command= self.resume)
        self.paused=True
    
    def stop(self):
        self.StopProgress()
        self.Player.stop()
        self.removeCoverArt()
        self.w2.grid_remove()
        self.w1.grid()

        self.w1.config(command=self.play)

    def Shuffle(self):
        self.StopProgress()
        parent=self.TreeView.parent(self.TreeView.focus())
        self.curSelectionIndex = random.randint(0,len(self.PlaybacksList[self.TreeView.item(parent)["text"]]))
        mf = self.PlaybacksList[self.TreeView.item(parent)["text"]][self.curSelectionIndex]
        self.playmusic(musicfile=mf,parent=parent)
        curSelId = self.TreeView.get_children(parent)[self.curSelectionIndex]
        self.TreeView.focus(curSelId)

    def Next(self):
        self.StopProgress()
        self.curSelectionIndex+=1
        parent=self.TreeView.parent(self.TreeView.focus())
        mf = self.PlaybacksList[self.TreeView.item(parent)["text"]][self.curSelectionIndex]
        self.playmusic(musicfile=mf,parent=parent)
        curSelId = self.TreeView.get_children(parent)[self.curSelectionIndex]
        self.TreeView.selection_set(curSelId)

    def Previous(self):
        self.StopProgress()
        self.curSelectionIndex-=1
        parent=self.TreeView.parent(self.TreeView.focus())
        mf = self.PlaybacksList[self.TreeView.item(parent)["text"]][self.curSelectionIndex]
        self.playmusic(musicfile=mf,parent=parent)
        curSelId = self.TreeView.get_children(parent)[self.curSelectionIndex]
        self.TreeView.selection_set(curSelId)

    def ShuffleOrNext(self,condition):
        if condition:
            self.Shuffle()
        else:
            self.Next()
    
    def volumeController(self,e):
        vol = int(self.VolumeSlider.get())
        self.Player.set_volume(vol/100)
        self.VolumeSlider.set(vol)

    def volUP(self):
        cvol = int(pygame.mixer_music.get_volume()*100)
        self.Player.set_volume(self.Player.get_volume()+0.05)
        self.VolumeSlider.set(cvol+0.05)

    def volDOWN(self):
        cvol = int(pygame.mixer_music.get_volume()*100)
        self.Player.set_volume(self.Player.get_volume()-0.05)
        self.VolumeSlider.set(cvol-0.05)