import time
import win32clipboard
from tkinter import ttk, Tk

import multiprocessing
from multiprocessing import Manager


class MTree(ttk.Treeview):

    # def __int__(self):
    #     self.width_arr = list()
    #     self.def_index = 2

    def init(self, master, treeChsHeadTup, scroll_bar=None):
        self.width_arr = list()
        self.def_index = 2
        # 初始化
        ttk.Style().configure("Treeview", font=('宋体', 8))
        # self.__init__(master, show="headings", columns=treeChsHeadTup, style='Treeview',
        #               yscrollcommand=scroll_bar)
        self.__init__(master, show="headings", columns=treeChsHeadTup, style='Treeview')
        for i in range(len(treeChsHeadTup)):
            if i == 0:
                widthNum = 20
            else:
                widthNum = 50
            # 记录各列宽
            self.width_arr.append(widthNum)
            self.column(treeChsHeadTup[i], width=widthNum, anchor='center')
        for i in range(len(treeChsHeadTup)):
            self.heading(treeChsHeadTup[i], text=treeChsHeadTup[i])
        self.bind("<Double-1>", self.onDBClick)

    def show(self, cols):
        # ttk.Style().configure("Treeview", font=('宋体', 8))
        # self.tableTree = ttk.Treeview(master, show="headings", columns=cols, style='Treeview')
        # for col_txt in cols:
        for i in range(len(cols)):
            col_txt = cols[i]
            if i == 0:
                widthNum = 20
            else:
                widthNum = 150
            self.heading('col_%s' % i, text='%s' % col_txt)
            self.column('col_%s' % i, width=widthNum, anchor='center')
            # self.tableTree.heading(cols[1], text='%s' % cols[1])
            # self.tableTree.column(cols[1], width=100, anchor='center')
        self.bind("<Double-1>", self.onDBClick)

    # 设置每列表头标题文本
    def set_headings(self, treeChsHeadTup):
        for i in range(len(treeChsHeadTup)):
            self.heading(treeChsHeadTup[i], text=treeChsHeadTup[i])

    def onDBClick(self, event):
        # if the area be clicked is not empty
        if self.selection():
            # print(event.x)
            x_index = self.judge_click_area(event.x) if (event and event.x) else self.def_index
            item = self.selection()[0]
            # print(x_index)
            # print("you clicked on %s" % item)
            # comp_name = self.item(item, "values")[2]
            comp_name = self.item(item, "values")[x_index]
            self.send_to_clipboard(comp_name)

    # @staticmethod
    def judge_click_area(self, _x):
        # _x -= 50
        fix_width_arr = [118, 266, 416, 562]
        # from Tools import tool
        if _x != None and _x > 0:
            # _x_sum_col = 0
            i = -1
            # _x_sum_col = self.width_arr.index(_x)
            for _x_col in fix_width_arr:
                i += 1
                # _x_sum_col += _x_col
                if _x_col >= _x:
                    return i
            return self.def_index

    # def place(self, **kvs):
    #     self.tableTree.place(**kvs)

    # def insert(self, *args, **kvs):
    #     self.tableTree.insert(*args, **kvs)

    def send_to_clipboard(self, content):
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_UNICODETEXT, str(content))
        win32clipboard.CloseClipboard()

    # def test(self):
    #     for i in range(0, 110):
    #         self.insert('', 0, values=(i, i, i))
    # def yscrollcommand(self):
    #     return self.tableTree['yscrollcommand']
    #
    # def yview(self):
    #     return self.tableTree.yview()


# def test():
#     tk = Tk()
#     # Tab_VScroll = Scrollbar(tk, orient='vertical')
#     # Tab_VScroll.place(relx=0.965, rely=0.030, relwidth=0.030, relheight=0.800)
#     Tab_MTree = MTree()
#     # Tab_MTree.init(tk, ('aaa', 'bbb', 'ccc'), Tab_VScroll)
#     Tab_MTree.init(tk, ('aaa', 'bbb', 'ccc'), None)
#     Tab_MTree.place(relx=0.010, rely=0.010, relwidth=0.950, relheight=0.800)
#     # 下面的这句是关键：指定Scrollbar的command的回调函数是Listbar的yview
#     # Tab_VScroll.config(command=Tab_MTree.yview)
#     # Tab_MTree.config(yscroll=Tab_VScroll.set)  # y滚动条关联
#     tk.mainloop()
#     # time.sleep(3)
#     Tab_MTree.insert('', 0, values=('aaaa', 'bbbb', 'cccc'))
#     Tab_MTree.insert('', 0, values=(1111, 2222, 3333))
#     Tab_MTree.onDBClick({'x': 40})
# import Vars as mVars
# if __name__ == '__main__':
#     multiprocessing.freeze_support()
#     vars_manager = Manager()
#     m_dict = vars_manager.dict()
#     valid_attr_dict = {}
#     i = 0
#     for attr in dir(mVars):
#         # print(attr)
#         # print(type(attr))
#         if "_" not in attr:
#             i += 1
#             attr_val = getattr(mVars, attr)
#             valid_attr_dict[attr] = attr_val
#             try:
#                 m_dict[attr] = attr_val
#                 # print(m_dict)
#             except Exception as e:
#                 print(e)
#     print(len(valid_attr_dict))
#     print(len(m_dict))
#     # print(i)
#     # print(dir(mVars))
#     for key in valid_attr_dict.keys():
#         # for key in m_dict.keys():
#         if key not in m_dict.keys():
#             print(key)