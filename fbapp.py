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

    login_frame = Frame(self)
    self.create_fbapp_login_frame(login_frame)
    login_frame.pack(fill = X, pady = 10)

    setting_frame = Frame(self)
    self.create_fbapp_setting_frame(setting_frame)
    setting_frame.pack(fill = X, pady = 20)
    

    # self.OutputText = Text(self, width = 35, height = 20, wrap = WORD)
    # self.OutputText.grid(row = 6, column = 0, columnspan = 4, sticky = S)
    
  def create_fbapp_login_frame(self, parnet_frame):
    Label(parnet_frame, text="電子郵件或電話 : ").grid(row= 0, sticky=E)
    Label(parnet_frame, text="密碼 : ").grid(row = 1, sticky=E)

    self.UserName = Entry(parnet_frame)
    self.UserName.grid(row = 0, column = 1, sticky=E)
    self.PassWord = Entry(parnet_frame, show = "*")
    self.PassWord.grid(row = 1, column = 1, sticky=E)

    self.StartBtn = Button(parnet_frame, text="開始", command = self.login_facebook).grid(row = 0, rowspan = 2, column = 2, sticky = NS)
    self.quitBtn  = Button(parnet_frame, text="離開", command = self.application_quit).grid(row = 0, rowspan = 2, column = 3, sticky = NS)

  def create_fbapp_setting_frame(self, parnet_frame):
    f1 = Frame(parnet_frame)
    Label(f1, text="每一篇文章間隔(秒)").pack(side = LEFT)
    self.each_article_delay_min = Entry(f1, width = 5)
    self.each_article_delay_min.pack(side = LEFT)
    Label(f1, text=" ~ ").pack(side = LEFT)
    self.each_article_delay_max = Entry(f1, width = 5)
    self.each_article_delay_max.pack(side = LEFT)
    f1.pack(fill = X)

    f2 = Frame(parnet_frame)
    Label(f2, text="每發").pack(side = LEFT)
    self.how_many_article_should_pause = Entry(f2, width = 5)
    self.how_many_article_should_pause.pack(side = LEFT)
    Label(f2, text="篇文章，休息").pack(side = LEFT)
    self.fbapp_pause_sec_min = Entry(f2, width = 5)
    self.fbapp_pause_sec_min.pack(side = LEFT)
    Label(f2, text = " ~ ").pack(side = LEFT)
    self.fbapp_pause_sec_max = Entry(f2, width = 5)
    self.fbapp_pause_sec_max.pack(side = LEFT)
    Label(f2, text = "秒").pack(side = LEFT)
    f2.pack(fill = X)

    f3 = Frame(parnet_frame)
    Label(f3, text = "搜集社團最大數量:").pack(side = LEFT)
    self.max_collect_groups = Entry(f3, width = 5)
    self.max_collect_groups.pack(side = LEFT)
    f3.pack(fill = X)

    f4 = Frame(parnet_frame)
    self.check_comment_after_post = IntVar()
    Checkbutton(f4, text="發完文是否要留言", variable=self.check_comment_after_post, anchor = W).grid(row = 3, sticky=E)
    f4.pack(fill = X)

  def login_facebook(self):
    username            = self.UserName.get()
    password            = self.PassWord.get()
    article_delay_min   = self.each_article_delay_min.get()
    article_delay_max   = self.each_article_delay_max.get()
    article_count_delay = self.how_many_article_should_pause.get()
    app_pause_min       = self.fbapp_pause_sec_min.get()
    app_pause_max       = self.fbapp_pause_sec_max.get()
    fb_max_groups_count = self.max_collect_groups.get()
    is_comment          = self.check_comment_after_post.get()

    if(username == "") or (password == ""):
      messagebox.showwarning("錯誤", "請輸入帳號及密碼")
      return

    if not ((article_delay_min.isdigit()) or (article_delay_max.isdigit()) or
           (article_count_delay.isdigit()) or
           (app_pause_min.isdigit()) or (app_pause_max.isdigit()) or
           (fb_max_groups_count.isdigit())):
      messagebox.showwarning("錯誤", "請輸入正確的數值")
      return




    # self.th = threading.Thread(target = self.facebook_auto)
    # self.th.start()
  
  def application_quit(self):
    self.parent.destroy()

  def facebook_auto(self):
    username = self.UserName.get()
    password = self.PassWord.get()
    fb.facebook_login(username,password)
    fb.facebook_collect_groups_id(200)

root = Tk()
# root.geometry("250x150+300+300")
root.geometry("500x500")
app = FacebookApp(root)
root.mainloop()
