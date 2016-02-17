from tkinter import *
from tkinter import messagebox

import fb
import threading

class FacebookApp(Frame):
  def __init__(self, parent):
    Frame.__init__(self, parent)   
    self.parent = parent
    self.initUI()

  def initUI(self):
    self.parent.title("Facebook 自動行銷軟體")
    self.pack(fill=BOTH, expand=1)

    Label(self, text="電子郵件或電話").grid(row= 0, sticky=W)
    Label(self, text="密碼").grid(row = 1, sticky=W)

    self.UserName = Entry(self)
    self.UserName.grid(row = 0, column = 1, sticky=E)
    self.PassWord = Entry(self, show = "*")
    self.PassWord.grid(row = 1, column = 1, sticky=E)

    self.StartBtn = Button(self, text="開始", command = self.login_facebook).grid(row = 0, rowspan = 2, column = 3, sticky=E)
    self.quitBtn  = Button(self, text="離開", command = self.application_quit).grid(row = 0, rowspan = 2, column = 4, sticky=E)

    self.OutputText = Text(self, width = 35, height = 20, wrap = WORD)
    self.OutputText.grid(row = 6, column = 0, columnspan = 4, sticky = S)

  def login_facebook(self):
    username = self.UserName.get()
    password = self.PassWord.get()
    
    if(username == "") or (password == ""):
      messagebox.showwarning("錯誤", "請輸入帳號及密碼")
      return

    self.th = threading.Thread(target = self.facebook_auto)
    self.th.start()
  
  def application_quit(self):
    self.parent.destroy()

  def facebook_auto(self):
    username = self.UserName.get()
    password = self.PassWord.get()
    fb.chrome_intialization()
    fb.facebook_login(username,password)
    fb.facebook_collect_groups_id(200)

root = Tk()
# root.geometry("250x150+300+300")
root.geometry("400x300")
app = FacebookApp(root)
root.mainloop()
# Label(self, text="Username").grid(row=0, sticky=W)
# Label(self, text="Password").grid(row=1, sticky=W)
# UserName = Entry(self).grid(row=0, column=1, sticky=E)
# PassWord = Entry(self).grid(row=1, column=1, sticky=E)
# StartBtn = Button(root, text="Start", command = login).grid(row=2, column=1, sticky=E)
# StartBtn.pack()


