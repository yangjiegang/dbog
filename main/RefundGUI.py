import os, sys, threading, time
from Tools import tool
from MultiListBox import MultiListbox
from MTree import MTree
import RequestWorker
import Vars as mVars
from Validator import Validator

try:
    from tkinter import *
except ImportError:  # Python 2.x
    PythonVersion = 2
    from Tkinter import *
    from tkFont import Font
    from ttk import *
    from tkMessageBox import *
else:  # Python 3.x
    PythonVersion = 3
    from tkinter.font import Font
    from tkinter.ttk import *
    from tkinter.messagebox import *
    from tkinter.simpledialog import askstring, askinteger, askfloat

class Application_ui(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
#         frame = Frame(master,height=467,width=358,background="#000000").pack(expand=YES,fill=BOTH)
        self.master.title('操作窗口')
        self.master.geometry('467x358')
#         self.master.background("#FFFFFF")
        self.createWidgets()

    def createWidgets(self):
        self.top = self.winfo_toplevel()
        self.style = Style()
 
#         frame = Frame(height=467,width=358,bg="#000000").pack(expand=YES,fill=BOTH)
        canvas = Canvas(self.top,width = 467, height = 358, bg = '#000000')
        canvas.pack(expand = YES, fill = BOTH)
        
        self.style.configure('background_label.TLabel',anchor='w', font=('宋体',9))
        background_label = Label(canvas, style='background_label.TLabel')
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
 
        self.m_tree = MTree(canvas, ['col00', 'col01'])
        self.m_tree.place(relx=0.02, rely=0.046, relwidth=0.959, relheight=0.802)

        self.gapTxtVar = StringVar(value='30')
        self.style.configure('gapTxt.TEntry')
        self.gapTxt = Entry(canvas, text='30', textvariable=self.gapTxtVar, font=('宋体',9), style='gapTxt.TEntry')
        self.gapTxt.place(relx=0.137, rely=0.882, relwidth=0.105, relheight=0.05)
 
        self.style.configure('queryCntLbl.TLabel',anchor='w', font=('宋体',9))
        self.queryCntLbl = Label(canvas, text='秒', style='queryCntLbl.TLabel')
        self.queryCntLbl.place(relx=0.257, rely=0.882, relwidth=0.088, relheight=0.047)
 
        self.style.configure('recordCntLbl.TLabel',anchor='w', font=('宋体',9))
        self.recordCntLbl = Label(canvas, text='间隔', style='recordCntLbl.TLabel')
        self.recordCntLbl.place(relx=0.051, rely=0.882, relwidth=0.088, relheight=0.047)
 
        self.style.configure('Command1.TLabel', font=('宋体',9))
#         self.launchBtn = Button(canvas, text='启动', command=self.launchBtn_Cmd, style='Command1.TLabel')
        self.launchBtn = Label(canvas, text='启动', style='Command1.TLabel')
        self.launchBtn.place(relx=0.565, rely=0.872, relwidth=0.071, relheight=0.07)
        self.launchBtn.bind('<Button-1>',self.launchBtn_Cmd)
 
        self.style.configure('Command2.TLabel',font=('宋体',9))
        self.stopBtn = Button(canvas, text='停止', command=self.pauseBtn_Cmd, style='Command2.TLabel')
#         self.launchBtn = Label(self.top, text='启动', style='Command2.TLabel')
        self.stopBtn.place(relx=0.688, rely=0.872, relwidth=0.071, relheight=0.07)

        self.style.configure('Command3.TLabel',font=('宋体',9))
        self.stopBtn = Button(canvas, text='修改密码', command=self.chgPwd_Cmd, style='Command3.TLabel')
#         self.launchBtn = Label(self.top, text='启动', style='Command2.TLabel')
        self.stopBtn.place(relx=0.818, rely=0.872, relwidth=0.110, relheight=0.07)

    def launchBtn_Cmd(self, event=None):
        print("info: program has been launched at %s" % str(time.ctime()))
        if tool.isEmpty(self.gapTxtVar.get()):
            qGap = 30
        else:
            qGap = float(self.gapTxtVar.get())
        self.launchBtn['state'] = DISABLED
        self.master.title('  请稍等：正在工作中...')
        widgetDict = {"gapTxt":self.gapTxt, "m_tree":self.m_tree, "queryCntLbl":self.queryCntLbl, "recordCntLbl":self.recordCntLbl}
        self.reqSpider = RequestWorker.RequestWoker(widgetDict)
        td = threading.Thread(target=self.reqSpider.run, args=(qGap,))
        td.setDaemon(True)
        td.start()
    def pauseBtn_Cmd(self):
        mVars.queryThreadIsRunningFlg = False
        # 如果没启动浏览器
        if hasattr(self, "reqSpider"):
            self.reqSpider.quit()
        try:
            # 退出之前强制终止所有火狐进程
            os.system("taskkill -f -im firefox.exe")
        except Exception as e:
            tool.logger.exception(e)
        sys.exit()
        # showinfo('提示', '本功能还未开发')
    def chgPwd_Cmd(self):
        lock_pwd = askstring("密保", "请输入密码")
        if lock_pwd == mVars.lock_pwd:                
            userInfo = askstring("修改密码", "用户名,密码")
            res = tool.setAccounts(userInfo)
            if res:
                messagebox.showinfo(title='修改结果', message='修改成功')
            else:
                messagebox.showinfo(title='修改结果', message='修改失败')
        else:
            messagebox.showinfo(title='警告', message='密码错误')
class Application(Application_ui):
    def __init__(self, master=None):
        Application_ui.__init__(self, master)
        self.app_ui = Application_ui()

# Launch program
def main():
    top = Tk()
    validator = Validator()
    if validator.judgeLegal():
        try:
            Application(top).mainloop()
            top.destroy()
        except Exception as e:
            tool.logger.exception(e)
main()