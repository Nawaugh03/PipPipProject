import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sys
from threading import *
from TweetCollector import TweetManager as TM
from win10toast import ToastNotifier
import time

width=550#self.winfo_screenwidth()
height=550#self.winfo_screenheight()
currentFrame=1
class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        W=width
        H=height
        #self.geometry("%dx%d"%(W, H))
        self.title("Pip-Pip")
        self._container=tk.Frame(self)
        self._container.pack(side="top",fill="both",expand=True)
        self._container.configure(bg="red")
        self._container.grid_rowconfigure(0, weight=1)
        self._container.grid_columnconfigure(0, weight=1)
        self.BorderDesign1=tk.Label(self, bg="red", height=60)
        self.BorderDesign1.place(relx=0)
        self.BorderDesign2 = tk.Label(bg="red", height=60)
        self.BorderDesign2.place(relx=1, anchor='e')
        #self.center_screen()
        self.frames={}
        index=0
        for F in (MainPage, ListPage, AddPage, RemovePage):
            frame = F(self._container, self)
            self.frames[F]=frame
            frame.grid(row=2,column=2,rowspan=2, columnspan=2, sticky="nsew")
            index+=1
        self.show_frame(MainPage)
    def center_screen(self):
        self.eval('tk::PlaceWindow . center')

    def show_frame(self, page_name):
        frame=self.frames[page_name]
        frame.tkraise()
        #self.center_screen()

    def UpdateFrame(self, I):
        self.frames.clear()
        for F in (MainPage, ListPage, AddPage, RemovePage):
            frame = F(self._container, self)
            self.frames[F] = frame
            frame.grid(row=2,column=2,rowspan=2, columnspan=2, sticky="nsew")
        if I==1:
            self.show_frame(MainPage)
        elif I == 2:
            self.show_frame(ListPage)
        elif I == 3:
            self.show_frame(AddPage)
        elif I == 4:
            self.show_frame(RemovePage)




class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,width=width,height=height)
        self.controller = controller
        global currentFrame
        currentFrame=1
        self.clickCheck=False
        self.configure(bg='red')
        Title=tk.Label(self,text="Pip-pip", bg="red",font=("Arial",50))
        Title.grid(column=3)
        resize_image=Image.open('clipart733659.png').resize((200,200))
        logo=ImageTk.PhotoImage(resize_image)
        label = tk.Label(self,image=logo)
        label.image=logo
        label.grid(column=3)
        ListButton=tk.Button(self, bg="lightblue",text="Go to Lists",command= lambda: controller.show_frame(ListPage))
        ListButton.grid(column=3)
        ListButton.grid_rowconfigure(2, weight=1)
        ListButton.grid_columnconfigure(2, weight=1)
        OffButton = tk.Button(self, text="Exit", fg="white", bg="#263D42", command=controller.destroy)
        OffButton.grid(column=3)

class ListPage(tk.Frame):
    def __init__(self,parent, controller):
        self.labels=[]
        global currentFrame
        currentFrame = 2
        tk.Frame.__init__(self, parent,width=width,height=height)
        self.parent=parent
        self.controller = controller
        self.configure(bg='red')
        Title = tk.Label(self, text="Lists of Users and tweets",padx=5,pady=5)
        Title.grid(column=2)
        
        for i in range(len(TM().ReadContent())):
            LabelMsg=str(TM().ReadContent()[i][1])+"\n"+str(TM().ReadContent()[i][2])
            self.labels.append(tk.Label(self,bg='red',text=LabelMsg, padx=5, pady=5))
            self.labels[i].grid(column=2)
        MainButton = tk.Button(self, bg="lightblue", text="Main Page", command=lambda: controller.show_frame(MainPage))
        MainButton.grid(column=2)
        MainButton.grid_rowconfigure(1,weight=1)
        MainButton.grid_columnconfigure(1,weight=1)
        AddButton=tk.Button(self, bg="lightblue", text="Add User", command=lambda : controller.show_frame(AddPage))
        AddButton.grid(column=2)
        RemoveButton = tk.Button(self, bg="lightblue", text="Remove User", command=lambda: controller.show_frame(RemovePage))
        RemoveButton.grid(column=2)
        RefreshButton = tk.Button(self, bg="lightblue", text="Refresh", command=lambda: self.Refresh())
        RefreshButton.grid(column=2)
    def Refresh(self):
        self.controller.UpdateFrame(2)

class AddPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,width=width,height=height)
        self.controller=controller
        global currentFrame
        currentFrame = 3
        Title = tk.Label(self, text="Insert Name and click which option",padx=5, pady=5)
        Title.grid()
        self.configure(bg='red')
        Exampletext=tk.Label(self, text="Example: '@johndoe' or '@janedoe,@johndoe'")
        Exampletext.grid()
        self.entry=tk.Entry(self, width=30, borderwidth=5)
        self.entry.focus_set()
        self.entry.grid()
        SubmitButton=tk.Button(self, bg="lightblue", text="Submit", command=lambda: self.SubmitUsers(self.entry.get()))
        SubmitButton.grid()
        ListButton = tk.Button(self, bg="lightblue", text="Go Back", command=lambda: controller.show_frame(ListPage))
        ListButton.grid()
        ListButton.grid_rowconfigure(1, weight=1)
        ListButton.grid_columnconfigure(1, weight=1)

    def SubmitUsers(self, Input):
        self.entry.delete(0, len(self.entry.get()))
        A=str(TM().AddUser(Input))
        TM().AddTwitterMessagestoFile()
        self.controller.UpdateFrame(3)
        messagebox.showinfo("Submission Alert", A)

class RemovePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,width=width,height=height)
        self.controller = controller
        global currentFrame
        currentFrame = 4
        self.configure(bg='red')
        Title = tk.Label(self, text="click which User you want to delete",padx=5, pady=5)
        Title.grid(row=0, column=2)
        self.Buttons={}
        for i in range(len(TM().ReadContent())):
            LabelMsg=str(TM().ReadContent()[i][1])
            self.Buttons[LabelMsg]=(tk.Button(self, bg="lightblue",text=LabelMsg, command=lambda a=LabelMsg: self.Remove(a)))
            self.Buttons[LabelMsg].grid(column=2)
        ListButton = tk.Button(self, bg="lightblue", text="Go Back", command=lambda: controller.show_frame(ListPage))
        ListButton.grid(column=2)
        ListButton.grid_rowconfigure(1, weight=1)
        ListButton.grid_columnconfigure(1, weight=1)

    def Remove(self,Userid):
        TM().RemoveUser(Userid)
        self.Buttons[Userid].destroy()
        self.controller.UpdateFrame(4)


endthread = False
def running():
    A=Application()
    A.mainloop()
    global endthread
    endthread = True

def Update():
            n = ToastNotifier()
            while True:
                global endthread
                #print("Checking Updates\n")
                time.sleep(5)
                if endthread:
                    break
                elif TM().CheckUpdates():
                    print(TM().ReadContent())
                    #Message = TM().SetNotifications()
                    #print(Message)
                    #self.controller.UpdateFrame(currentFrame)
                    #for i in range(len(Message)):
                    #    n.show_toast(Message[i][0], Message[i][1], duration=10)
                #time.sleep(2)

def Main():
    t1=Thread(target=Update)
    t2=Thread(target=running)
    t1.start()
    t2.start()

Main()
#A=Application()
#A.mainloop()
#Update()
#print(TM().ReadContent())
'''theanything_bot'''
