from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import *

from statusbar import *

import fb
import threading

class FacebookApp(Frame):
  def __init__(self, parent):
    Frame.__init__(self, parent)   
    self.parent = parent
    self.parent.title("Facebook 自動行銷軟體")
    self.pack(fill=BOTH, expand=1)

    self.status_bar = StatusBar(self)
    self.status_bar.set("Status:")
    self.status_bar.pack(fill = X, side = BOTTOM)

    self.initUI()

    self.group_list = None
    self.start_button_thread = threading.Thread(name = "start_btn_thread", target = self.thread_start_button_function)
    self.start_button_thread.daemon = True

  def initUI(self):
    left_frame = Frame(self)
    self.create_left_frame_ui(left_frame)
    left_frame.pack(fill = BOTH, expand = 1, side = LEFT)

    # center_frame = Frame(self)
    # s = ttk.Separator(center_frame, orient = VERTICAL)
    # s.grid(padx = 10)
    # center_frame.pack(fill = BOTH, expand = 1, side = LEFT)

    right_frame = Frame(self)
    self.create_right_frame_ui(right_frame)
    right_frame.pack(fill = BOTH, expand = 1, side = LEFT)

 
  def create_left_frame_ui(self, parent_frame):
    login_frame = Frame(parent_frame)
    self.create_fbapp_login_frame(login_frame)
    login_frame.pack(fill = X, pady = 10)

    setting_frame = Frame(parent_frame)
    self.create_fbapp_setting_frame(setting_frame)
    setting_frame.pack(fill = X, pady = 20)
    
    self.textPad = ScrolledText(parent_frame, pady = 30, width = 70, height = 10, bg = "gray", bd = 3)
    self.textPad.pack(fill = X)

 
  def create_right_frame_ui(self, parent_frame):

    self.random_sel_group = IntVar()
    Checkbutton(parent_frame, text="是否要隨機挑選群組", variable=self.random_sel_group, anchor = W).pack(side = TOP, anchor = W)

    group_list_frame = Frame(parent_frame)
    group_list_frame.pack(side = TOP)

    self.group_listbox = Treeview(group_list_frame, columns = ("members", "privacy"))
    self.group_listbox.pack(side = LEFT)

    self.group_listbox.heading("#0", text="社團名稱", anchor = W)
    self.group_listbox.column("#0", stretch = True)

    self.group_listbox.heading("members", text="社團人數", anchor = W)   
    self.group_listbox.column("members", stretch = True)

    self.group_listbox.heading("privacy", text="社團隱私", anchor = W)   
    self.group_listbox.column("privacy", stretch = True)

    ysb = ttk.Scrollbar(group_list_frame, orient=VERTICAL,   command = self.group_listbox.yview)
    self.group_listbox['yscroll'] = ysb.set

    xsb = ttk.Scrollbar(group_list_frame, orient=HORIZONTAL, command = self.group_listbox.xview)
    self.group_listbox['xscroll'] = xsb.set

    # add tree and scrollbars to frame
    self.group_listbox.grid(row=0, column=0, sticky=NSEW)
    ysb.grid(row=0, column=1, sticky=NS)
    xsb.grid(row=1, column=0, sticky=EW)
         


    # for digit in range(120):
    #   members = digit * 20
    #   attrs   = "open"
    #   self.group_listbox.insert("" , "end", text=digit, values=('123', members, attrs))

  def create_fbapp_login_frame(self, parnet_frame):
    Label(parnet_frame, text="電子郵件或電話 : ").grid(row= 0, sticky=E)
    Label(parnet_frame, text="密碼 : ").grid(row = 1, sticky=E)

    self.UserName = Entry(parnet_frame, bd = 3 )
    self.UserName.grid(row = 0, column = 1, sticky=E)
    self.PassWord = Entry(parnet_frame, show = "*", bd = 3 )
    self.PassWord.grid(row = 1, column = 1, sticky=E)

    self.StartBtn = Button(parnet_frame, text="開始", command = self.application_start).grid(row = 0, rowspan = 2, column = 2, sticky = NS)
    self.quitBtn  = Button(parnet_frame, text="離開", command = self.application_quit).grid(row = 0, rowspan = 2, column = 3, sticky = NS)

  def create_fbapp_setting_frame(self, parnet_frame):
    f1 = Frame(parnet_frame)
    Label(f1, text="每一篇文章間隔(秒)").pack(side = LEFT)
    self.each_article_delay_min = Entry(f1, width = 5, bd = 3 )
    self.each_article_delay_min.pack(side = LEFT)
    Label(f1, text=" ~ ").pack(side = LEFT)
    self.each_article_delay_max = Entry(f1, width = 5, bd = 3 )
    self.each_article_delay_max.pack(side = LEFT)
    f1.pack(fill = X)

    f2 = Frame(parnet_frame)
    Label(f2, text="每發").pack(side = LEFT)
    self.how_many_article_should_pause = Entry(f2, width = 5, bd = 3 )
    self.how_many_article_should_pause.pack(side = LEFT)
    Label(f2, text="篇文章，休息").pack(side = LEFT)
    self.fbapp_pause_sec_min = Entry(f2, width = 5, bd = 3 )
    self.fbapp_pause_sec_min.pack(side = LEFT)
    Label(f2, text = " ~ ").pack(side = LEFT)
    self.fbapp_pause_sec_max = Entry(f2, width = 5, bd = 3 )
    self.fbapp_pause_sec_max.pack(side = LEFT)
    Label(f2, text = "秒").pack(side = LEFT)
    f2.pack(fill = X)

    f3 = Frame(parnet_frame)
    Label(f3, text = "搜集社團最大數量:").pack(side = LEFT)
    self.max_collect_groups = Entry(f3, width = 5, bd = 3 )
    self.max_collect_groups.pack(side = LEFT)
    f3.pack(fill = X)

    f4 = Frame(parnet_frame)
    self.check_comment_after_post = IntVar()
    Checkbutton(f4, text="發完文是否要留言", variable=self.check_comment_after_post, anchor = W).grid(row = 3, sticky=E)
    f4.pack(fill = X)

    f5 = Frame(parnet_frame)
    self.browse_button = Button(f5, text="指定文案目錄", command=self.browse_file_directory, width=10, bd = 5)
    self.browse_button.pack(side = LEFT)
    self.dir_name = StringVar()
    self.browse_dir_name = Entry(f5, width = 40, bd = 3 , textvariable = self.dir_name)
    self.browse_dir_name.pack(side = LEFT)
    f5.pack(fill = X)


  def browse_file_directory(self):
    directory_name= filedialog.askdirectory()
    self.dir_name.set(directory_name)

  def application_start(self):
    username            = self.UserName.get()
    password            = self.PassWord.get()
    article_delay_min   = self.each_article_delay_min.get()
    article_delay_max   = self.each_article_delay_max.get()
    article_count_delay = self.how_many_article_should_pause.get()
    app_pause_min       = self.fbapp_pause_sec_min.get()
    app_pause_max       = self.fbapp_pause_sec_max.get()
    fb_max_groups_count = self.max_collect_groups.get()
    is_comment          = self.check_comment_after_post.get()

    # if(username == "") or (password == ""):
    #   messagebox.showwarning("錯誤", "請輸入帳號及密碼")
    #   return

    # if not ((article_delay_min.isdigit()) and (article_delay_max.isdigit()) and
    #        (article_count_delay.isdigit()) and
    #        (app_pause_min.isdigit()) and (app_pause_max.isdigit()) and
    #        (fb_max_groups_count.isdigit())):
    #   messagebox.showwarning("錯誤", "請輸入正確的數值")
    #   return
    

    self.start_button_thread.start()
    # self.start_button_thread.join()
  
    
  def application_quit(self):
    self.parent.destroy()

  def thread_start_button_function(self):
    username = self.UserName.get()
    password = self.PassWord.get()
    if fb.facebook_login(username,password) == "failed" :
      return

    self.group_list = fb.facebook_collect_groups_id(200)
    self.insert_group_info(self.group_list)

  def insert_group_info(self, group_list):
    # self.group_listbox.insert("" , "end", text=digit, values=(members, attrs))
    for group_info in group_list:
      g_name = group_info['g_name']
      g_id   = group_info['g_id']
      self.group_listbox.insert("", "end", text = g_name)


root = Tk()
# root.geometry("250x150+300+300")
# root.geometry("800x500")
app = FacebookApp(root)
root.mainloop()
