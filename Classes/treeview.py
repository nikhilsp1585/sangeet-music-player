import tkinter as tk
from tkinter import *
from tkinter import ttk,filedialog,messagebox

class Treeview():
    
    def __init__(self,parent,style):
        self.parent = parent
        self.theme  = style

        self.theme.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])
        self.theme.configure('Treeview',rowheight=40,borderwidth=0,relief='flat',font=("Bahnschrift",10,"normal"))
        self.theme.configure('Treeview.Heading',font=('Bahnschrift',11,'normal'),foreground='#323232',background="#f5f5f5")
        self.theme.map('Treeview',background=[('selected','#3297fd')],foreground=[('selected','white')],font=[('selected',("Bahnschrift",10,"bold"))])

        self.TreeColumns = ['T','D','A']
        

    def initTree(self):

        self.TreeView = ttk.Treeview(self.parent,selectmode='extended',padding=15)

        self.SidebarYScroll = ttk.Scrollbar(self.parent,orient='vertical',command=self.TreeView.yview)
        self.SidebarYScroll.pack(side='right',fill='y')

        self.TreeView.config(columns=self.TreeColumns,yscrollcommand=self.SidebarYScroll.set)

        self.TreeView.column("#0",minwidth=100,width=100,anchor='center')
        self.TreeView.column("#1",minwidth=250,width=700,anchor='w')
        self.TreeView.column("#2",minwidth=40,width=60,anchor='center')
        self.TreeView.column("#3",minwidth=80,width=180,anchor='w',)

        self.TreeView.heading("#0",text="#")
        self.TreeView.heading("#1",text="Title")
        self.TreeView.heading("#2",text="Duration")
        self.TreeView.heading("#3",text="Artist")

        self.TreeView.tag_configure('even',background='gray95')
        self.TreeView.tag_configure('odd',background='white')



