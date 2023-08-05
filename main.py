# -*- coding: UTF-8 -*-
import datetime
import getpass
import multiprocessing
import os
import random
import subprocess
import sys
import threading
import time
import traceback
import webbrowser
from tkinter.colorchooser import *
from tkinter.filedialog import asksaveasfilename, askopenfilename, askopenfilenames
from tkinter.font import *
from typing import List

import chardet
# import ctypes
import jieba
import pyperclip
import windnd
from PIL import Image, ImageTk
# from tkinter import *
from _tkinter import TclError
from need.ttkbootstrap import *
from need.ttkbootstrap.scrolled import ScrolledFrame
from need.ttkbootstrap.dialogs import Messagebox, Querybox
from need.ttkbootstrap.icons import Emoji
from pathlib import Path
import pygame.mixer as music
from mutagen.mp3 import MP3


def gettime(): return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def runcalc():
    def date():
        begin = Querybox.get_date(title='选择开始日期')
        end = Querybox.get_date(title='选择截止日期')
        days = str((end - begin).days)
        if Messagebox.okcancel(f'日期之差为:{days}点击复制,点X取消', '计算结果'):
            pyperclip.copy(days)

    def run():
        global need, jin
        s = en1.get()
        s = s.replace('%', '/100')
        s = s.replace('mod', '%')
        s = s.replace('^', '**')
        s = s.replace('π', str(math.pi))
        s = s.replace('x', '*')
        s = s.replace('÷', '/')
        try:
            a = eval(s)
        except Exception:
            a = '计算错误'
        finally:
            jin = 10
            en2.delete(0, END)
            en2.insert(END, a)

    def jia(a):
        global need
        need.append(a)
        en1.insert(END, a)

    def clean():
        global need
        need.clear()
        en1.delete(0, END)

    def delete():
        en1.delete(len(en1.get()) - 1, END)

    def jiax():
        en1.insert(0, '1÷(')
        en1.insert(END, ')')

    def jinzhi(num):
        global jin
        s = en1.get()
        s = s.replace('%', '/100')
        s = s.replace('mod', '%')
        s = s.replace('^', '**')
        s = s.replace('π', str(math.pi))
        s = s.replace('x', '*')
        s = s.replace('÷', '/')
        en2.delete(0, END)
        try:
            if num == 10:
                en2.insert(0, str(int(str(eval(s)), jin))[2:])
                jin = 10
            elif num == 8:
                en2.insert(0, str(oct(int(str(eval(s)), jin)))[2:])
                jin = 8
            elif num == 16:
                en2.insert(0, str(hex(int(str(eval(s)), jin)))[2:])
                jin = 16
        except Exception:
            en2.delete(0, END)
            en2.insert(0, '计算错误')

    def mplus():
        global mr
        try:
            mr = eval(en1.get())
        except Exception:
            en2.delete(0, END)
            en2.insert(0, 'm+错误')

    def muplus():
        global mr
        try:
            mr = eval(en1.get()) * -1
        except Exception:
            en2.delete(0, END)
            en2.insert(0, 'm-错误')

    def mc():
        global mr
        mr = ''

    need = []
    jin = 10
    mr = 0
    # tk = Window(title=f'python记事本-计算器',
    #             themename="sandstone",
    #             size=(400, 550),
    #             position=(500, 200),
    #             resizable=(False, False),
    #             )
    tk = Toplevel()
    tk.title('python记事本 - 计算器')
    tk.geometry('400x550+500+200')
    tk.resizable(False, False)
    tk.iconbitmap(os.path.join(os.path.dirname(sys.argv[0]), '.\\icon\\calc.ico'))
    tk.configure(bg='white')
    en1 = Entry(tk)
    en1.place(width=400, height=40, rely=0.01)
    en2 = Entry(tk)
    en2.place(width=400, rely=0.09, height=40)
    Button(
        tk,
        text=1,
        command=lambda: jia(1)).place(
        width=60,
        height=60,
        relx=0,
        rely=0.17)
    Button(
        tk,
        text=2,
        command=lambda: jia(2)).place(
        width=60,
        height=60,
        relx=0.16,
        rely=0.17)
    Button(
        tk,
        text=3,
        command=lambda: jia(3)).place(
        width=60,
        height=60,
        relx=0.32,
        rely=0.17)
    Button(
        tk,
        text='+',
        command=lambda: jia('+'),
        bootstyle='secondary').place(
        width=60,
        height=60,
        relx=0.48,
        rely=0.17)
    Button(
        tk,
        text='-',
        command=lambda: jia('-'),
        bootstyle='secondary').place(
        width=60,
        height=60,
        relx=0.48,
        rely=0.29)
    Button(
        tk,
        text='×',
        command=lambda: jia('x'),
        bootstyle='secondary').place(
        width=60,
        height=60,
        relx=0.48,
        rely=0.41)
    Button(
        tk,
        text='÷',
        command=lambda: jia('÷'),
        bootstyle='secondary').place(
        width=60,
        height=60,
        relx=0.48,
        rely=0.53)
    Button(
        tk,
        text='√(',
        command=lambda: jia('math.sqrt('),
        bootstyle='secondary').place(
        width=60,
        height=60,
        relx=0.64,
        rely=0.17)
    Button(
        tk,
        text='sin',
        command=lambda: jia('math.sin('),
        bootstyle='secondary').place(
        width=60,
        height=60,
        relx=0.8,
        rely=0.29)
    Button(
        tk,
        text='tan',
        command=lambda: jia('math.tan('),
        bootstyle='secondary').place(
        width=60,
        height=60,
        relx=0.8,
        rely=0.41)
    Button(
        tk,
        text='cos',
        command=lambda: jia('math.cos('),
        bootstyle='secondary').place(
        width=60,
        height=60,
        relx=0.8,
        rely=0.53)
    Button(
        tk,
        text='清除',
        command=clean,
        bootstyle='secondary').place(
        width=60,
        height=60,
        relx=0.80,
        rely=0.17)
    Button(
        tk,
        text='^2',
        command=lambda: jia('^2'),
        bootstyle='secondary').place(
        width=60,
        height=60,
        relx=0.64,
        rely=0.29)
    Button(
        tk,
        text='^',
        command=lambda: jia('^'),
        bootstyle='secondary').place(
        width=60,
        height=60,
        relx=0.64,
        rely=0.41)
    Button(
        tk,
        text='=',
        command=run,
        bootstyle='	success').place(
        width=60,
        height=60,
        relx=0.64,
        rely=0.53)
    Button(
        tk,
        text=4,
        command=lambda: jia(4)).place(
        width=60,
        height=60,
        relx=0,
        rely=0.29)
    Button(
        tk,
        text=5,
        command=lambda: jia(5)).place(
        width=60,
        height=60,
        relx=0.16,
        rely=0.29)
    Button(
        tk,
        text=6,
        command=lambda: jia(6)).place(
        width=60,
        height=60,
        relx=0.32,
        rely=0.29)
    Button(
        tk,
        text=7,
        command=lambda: jia(7)).place(
        width=60,
        height=60,
        relx=0,
        rely=0.41)
    Button(
        tk,
        text=8,
        command=lambda: jia(8)).place(
        width=60,
        height=60,
        relx=0.16,
        rely=0.41)
    Button(
        tk,
        text=9,
        command=lambda: jia(9)).place(
        width=60,
        height=60,
        relx=0.32,
        rely=0.41)
    Button(
        tk,
        text='(',
        bootstyle='secondary',
        command=lambda: jia('(')).place(
        width=60,
        height=60,
        relx=0,
        rely=0.53)
    Button(
        tk,
        text=0,
        command=lambda: jia(0)).place(
        width=60,
        height=60,
        relx=0.16,
        rely=0.53)
    Button(tk, text=')',
           bootstyle='secondary',
           command=lambda: jia(')')).place(
        width=60, height=60, relx=0.32, rely=0.53)
    Button(
        tk,
        text='DEL',
        bootstyle='secondary',
        command=delete).place(
        width=60,
        height=60,
        relx=0,
        rely=0.65)
    Button(
        tk,
        text='%',
        bootstyle='secondary',
        command=lambda: jia('%')).place(
        width=60,
        height=60,
        relx=0.16,
        rely=0.65)
    Button(
        tk,
        text='mod',
        bootstyle='secondary',
        command=lambda: jia('mod')).place(
        width=60,
        height=60,
        relx=0.32,
        rely=0.65)
    Button(
        tk,
        text='.',
        bootstyle='secondary',
        command=lambda: jia('.')).place(
        width=60,
        height=60,
        relx=0.48,
        rely=0.65)
    Button(
        tk,
        text='1/x',
        bootstyle='secondary',
        command=jiax).place(
        width=60,
        height=60,
        relx=0.64,
        rely=0.65)
    Button(
        tk,
        text='八进制',
        bootstyle='secondary',
        command=lambda: jinzhi(8)).place(
        width=60,
        height=60,
        relx=0,
        rely=0.77)
    Button(
        tk,
        text='十进制',
        bootstyle='secondary',
        command=lambda: jinzhi(10)).place(
        width=60,
        height=60,
        relx=0.16,
        rely=0.77)
    Button(
        tk,
        text='十六进制',
        bootstyle='secondary',
        command=lambda: jinzhi(16)).place(
        width=60,
        height=60,
        relx=0.32,
        rely=0.77)
    Button(
        tk,
        text='m+',
        bootstyle='secondary',
        command=mplus).place(
        width=60,
        height=60,
        relx=0.48,
        rely=0.77)
    Button(
        tk,
        text='m-',
        bootstyle='secondary',
        command=muplus).place(
        width=60,
        height=60,
        relx=0.64,
        rely=0.77)
    Button(
        tk,
        text='mr',
        bootstyle='secondary',
        command=lambda: en1.insert(END, mr)).place(
        width=60,
        height=60,
        relx=0.80,
        rely=0.77)
    Button(
        tk,
        text='mc',
        bootstyle='secondary',
        command=mc).place(
        width=60,
        height=60,
        relx=0.8,
        rely=0.65)
    Button(
        tk,
        text='计算日\n期之差',
        bootstyle='secondary',
        command=date).place(
        width=60,
        height=60,
        relx=0,
        rely=0.89)
    Button(
        tk,
        text='sinh',
        bootstyle='secondary',
        command=lambda: jia('math.sinh(')).place(
        width=60,
        height=60,
        relx=0.16,
        rely=0.89)
    Button(
        tk,
        text='cosh',
        bootstyle='secondary',
        command=lambda: jia('math.cosh(')).place(
        width=60,
        height=60,
        relx=0.32,
        rely=0.89)
    Button(
        tk,
        text='tanh',
        bootstyle='secondary',
        command=lambda: jia('math.tanh')).place(
        width=60,
        height=60,
        relx=0.48,
        rely=0.89)
    Button(
        tk,
        text='10^',
        bootstyle='secondary',
        command=lambda: jia('10^')).place(
        width=60,
        height=60,
        relx=0.64,
        rely=0.89)
    Button(
        tk,
        text='π',
        bootstyle='secondary',
        command=lambda: jia('π')).place(
        width=60,
        height=60,
        relx=0.8,
        rely=0.89)
    tk.mainloop()


def show_log():
    tk = Toplevel()
    tk.title("python记事本 - 更新日志")
    tk.geometry('500x550')
    tk.iconbitmap(os.path.join(os.path.dirname(sys.argv[0]), '.\\icon\\notepad.ico'))
    tk.resizable(False, False)
    s = ScrolledFrame(tk)
    s.pack(fill=BOTH, expand=YES)
    Label(s, text="python快乐记事本 更新日志", font=("Microsoft YaHei UI", 15, "bold")).pack(anchor=W)
    Label(s, text='''版本号    日期         更新天数    内容    
0.9.0    2022.10.10  1    开始写第一行代码 
1.0.0    2022.10.12    1    创建框架                                                                                                                                                
1.0.5    2022.10.13    2    创建按钮                                                                                                                                                
1.1.0    2022.10.14    1    按钮变菜单                                                                                                                                                
1.2.0    2022.10.16    2    增加撤销功能                                                                                                                                                
2.0.0    2022.10.17    1    窗口美化            
2.3.0    2022.11.1    4    增加查找替换功能    
2.4.0    2022.11.3    3    支持切换字体                                                                                                                                                
2.4.1    2022.11.4    1    修复已知bug                                                                                                                                                
2.4.2    2022.11.5    1    更新帮助文档    
2.6.0    2022.11.8    1    增加主题切换        
2.7.0    2022.11.10    2    自由设定前景背景色
3.0.0    2022.11.15    5    代码重组                                                                                                                                                
3.0.1    2022.11.16    1    提高启动速度                                                                                                                                                
3.1.0    2022.11.19    3    增加透明度调节    
3.2.0    2022.11.23    4    增加查找对话框
3.4.5    2022.12.1         修复已知bug
3.5.0    2022.12.3    2    菜单重组                                                                                                                                                
3.6.0    2022.12.5    3    计算器代码重写
3.7.0    2022.12.8    3    卸载程序代码重写    
3.8.0    2022.12.25    2    重写帮助文档
3.9.0    2022.12.30    1    更新快捷键                                                                                                                                                
3.10.0   2023.1.2    2    帮助文档改版                                                                                                                                                
3.10.2   2023.1.3    1    代码优化，提高启动速度
3.10.5   2023.1.4    1    修复已知bug                                                                                                                                                
3.11.0   2023.1.7    3    增加二进制文件打开功能
3.11.1   2023.1.9    2    增加美化功能    
4.0.0    2023.7.25    6    增加多选项卡
4.1.0    2023.7.31    2    增加"选择的文件"
4.2.0    2023.8.3     3    增加行显示
4.3.0                 3    增加大量功能:
大小写转换
行处理
全部保存
切换文件
更多主题颜色
4.4.0                 1    增加行数颜色设置,文件列表,复制文件
4.5.0                      增加音频播放  ''').pack(fill=BOTH, expand=YES)
    tk.mainloop()


def about():
    s = (
        ("Ctrl+c复制", 0),
        ("Ctrl+v粘贴", 1),
        ("Ctrl+A全选", 2),
        ("Ctrl+x剪切", 3),
        ("Ctrl+s保存", 4),
        ("Ctrl+n新建", 4),
        ("Alt+F4退出", 5),
        ("F1帮助", 5),
        ("Ctrl+o打开", 5),
        ("Ctrl+w直接退出", 4)
    )
    s2 = (
        ("F5运行py", 0),
        ("F12打开网页", 0),
        ("Ctrl+b运行pyw", 1),
        ("Ctrl+L文本长度", 2),
        ("Ctrl+]增加缩进", 3),
        ("Ctrl+[减少缩进", 4)
    )
    themes = (
        "暗色主题",
        "亮色主题",
        "紫色主题",
        "蓝色主题",
        "灰色主题"
    )
    tk = Toplevel()
    '''(title="python记事本 - 关于",
                    themename="sandstone",
                    size=(450, 480),
                    position=(500, 200),
                    resizable=(False, False)
                    )'''
    tk.title("python记事本 - 关于")
    tk.geometry("450x480+500+200")
    tk.resizable(False, False)
    # tk=Toplevel()
    # tk.title("python记事本 - 帮助")
    # tk.geometry('450x500+500+200')
    # tk.resizable(False,False)
    # Style(theme="sandstone")
    # lbf=LabelFrame(tk)
    # lbf.place(relwidth=1,relheight=0.2)
    tk.iconbitmap(os.path.join(os.path.dirname(sys.argv[0]), '.\\icon\\help.ico'))
    img = PhotoImage(file=os.path.join(os.path.dirname(sys.argv[0]), '.\\icon\\notepad.gif'))
    Label(tk, image=img).place(relx=0.1, rely=0, relheight=0.2, relwidth=0.2)
    Label(tk, text='python快乐记事本\n版本号3.11.5,更新时间2023.1.28').place(relx=0.3, rely=0.06)
    Separator(tk).place(rely=0.2, relwidth=1, relheight=0.01)
    # Label(tk,text='快捷键大全:\n'
    #                    '  通用快捷键:\n'
    #                    '     Ctrl+c复制,Ctrl+v粘贴,Ctrl+A全选,Ctrl+x剪切').place(rely=0.22,relx=0.01)
    tw = Treeview(tk)
    tw.place(rely=0.22, relx=0.01, relwidth=0.98, relheight=0.77)
    tw1 = tw.insert("", 0, text="快捷键大全", values="1")
    tw2 = tw.insert(tw1, 0, text="通用快捷键", values="1_1")
    for i, index in s:
        tw.insert(tw2, index, text=i)
    tw3 = tw.insert(tw1, 1, text="此程序快捷键")
    for i, index in s2:
        tw.insert(tw3, index, text=i)
    tw_h = tw.insert("", END, text="程序开发")
    tw.insert(tw_h, END, text="python版本:3.11")
    tw.insert(tw_h, END, text="词频统计:jieba")
    tw.insert(tw_h, END, text="代码高亮:idlelib")
    tw.insert(tw_h, END, text="GUI:tkinter")
    twh2 = tw.insert("", END, text="使用说明")
    twh22 = tw.insert(twh2, END, text="主题")
    for x in themes:
        tw.insert(twh22, END, text=x)
    tw.insert(twh2, END, text="搜索引擎:bing")
    tw.insert(twh2, END, text="运行python需配置解释器")
    tw.insert(twh2, END, text="运行c,c++需配置mingw")
    tw5 = tw.insert("", END, text="其他")
    tw4 = tw.insert(tw5, END, text="不小心选择超大文件导致之后打开时卡死")
    tw.insert(tw4, 0, text=f"请删除%USERNAME%/AppData/Local/Temp/python_notepad.tmp")

    def open_children(parent):
        tw.item(parent, open=True)
        for child in tw.get_children(parent):
            open_children(child)

    open_children(tw.focus())
    # tw.bind('<<TreeviewOpen>>', handleOpenEvent)
    # Label(tk,text="信息").place(rely=0.25,relx=0.04)
    tk.mainloop()


def validate_number(x) -> bool:
    """Validates that the input is a number"""
    if x.isdigit():
        return True
    elif x == "":
        return True
    else:
        return False


class Scales:
    """a class to get scales"""

    def __init__(self):
        self.scale = 0
        self.s = {"get": 0}
        self.root = Toplevel()
        self.root.title("python记事本 - 透明度")
        self.root.geometry('330x90+600+300')
        self.root.resizable(False, False)
        self.root.iconbitmap(os.path.join(os.path.dirname(sys.argv[0]), './icon/notepad.ico'))
        self.sca = Scale(self.root, bootstyle=INFO, from_=0, to=100)
        self.fontname = Font(family="Microsoft YaHei UI", size=10)

    def returns(self):
        get = self.sca.get()
        self.scale = get
        self.s["get"] = int(get)
        self.root.destroy()
        return self.s

    def fefreshes(self, tk, *args):
        get = int(self.sca.get())
        tk.attributes("-alpha", (100 - get) / 100)
        self.root.title(f"python记事本 - 透明度-{get}")

    def show(self, windows):
        self.sca.place(relwidth=1, height=30, rely=0.15)
        Label(self.root, text="选择透明度").place(rely=0, relx=0)
        Button(self.root, text="确定", command=self.returns).place(relx=0.42, rely=0.6)
        self.sca.bind("<Button-1>", lambda event: self.fefreshes(windows))
        self.sca.bind("<ButtonRelease>", lambda event: self.fefreshes(windows))
        self.root.wait_window()


class Replace:
    def __init__(self, text, parents):
        self.parents = parents
        self.parents.text[self.parents.note.index(self.parents.note.select())] = text
        self.root = Toplevel()
        self.root.title('python记事本 - 替换')
        self.root.geometry('320x80+600+300')
        self.root.resizable(False, False)
        self.root.iconbitmap(os.path.join(os.path.dirname(sys.argv[0]), './icon/notepad.ico'))
        Label(self.root, text='查找').grid(row=0, column=1, sticky=W, padx=5, pady=5)
        Label(self.root, text='替换').grid(row=1, column=1)
        self.ent = Entry(self.root)
        self.ent.grid(row=0, column=2, sticky=W, padx=3, pady=3)
        self.ent2 = Entry(self.root)
        self.ent2.grid(row=1, column=2, sticky=W, padx=3, pady=3)
        self.ent.bind("<Key>", self.mysearch)
        self.ent2.bind("<Return>", self.replace)
        Button(self.root, text='查找', command=self.mysearch).grid(row=0, column=3, sticky=W, padx=3, pady=3)
        Button(self.root, text='退出', command=self.kill).grid(row=0, column=4, sticky=W, padx=3, pady=3)
        Button(self.root, text='替换', command=self.replace).grid(row=1, column=3, sticky=W, padx=3, pady=3)
        Button(self.root, text='全部', command=lambda: self.replace(all_=True)).grid(row=1, column=4, sticky=W, padx=3,
                                                                                     pady=3)
        self.root.wait_window()

    def mysearch(self, *args):
        self.parents.text[self.parents.note.index(self.parents.note.select())].tag_remove("found", "1.0", END)
        start = "1.0"
        try:
            key = self.parents.text[self.parents.note.index(self.parents.note.select())].get(SEL_FIRST, SEL_LAST)
        except TclError:
            key = self.ent.get()
        if len(key.strip()) == 0:
            return
        while True:
            pos = self.parents.text[self.parents.note.index(self.parents.note.select())].search(key, start, END)
            # print("pos= ",pos) # pos=  3.0  pos=  4.0  pos=
            if pos == "":
                break
            self.parents.text[self.parents.note.index(self.parents.note.select())].tag_add("found", pos,
                                                                                           "%s+%dc" % (pos, len(key)))
            start = "%s+%dc" % (pos, len(key))

    def replace(self, all_=False):
        text = self.parents.text[self.parents.note.index(self.parents.note.select())].get(1.0, END)
        self.parents.text[self.parents.note.index(self.parents.note.select())].delete(1.0, END)
        if all_:
            self.parents.text[self.parents.note.index(self.parents.note.select())].insert(END,
                                                                                          text.replace(self.ent.get(),
                                                                                                       self.ent2.get()))
        else:
            self.parents.text[self.parents.note.index(self.parents.note.select())].insert(END,
                                                                                          text.replace(self.ent.get(),
                                                                                                       self.ent2.get(),
                                                                                                       1))

    def kill(self):
        self.parents.text[self.parents.note.index(self.parents.note.select())].tag_remove("found", "1.0", END)
        self.root.destroy()


class Find:
    def __init__(self, text, parents):
        self.parents = parents
        self.parents.text[self.parents.note.index(self.parents.note.select())] = text
        self.root = Toplevel()
        self.root.title('python记事本 - 查找')
        self.root.geometry('300x40+600+300')
        self.root.resizable(False, False)
        self.root.iconbitmap(os.path.join(os.path.dirname(sys.argv[0]), './icon/notepad.ico'))
        Label(self.root, text='查找').grid(row=0, column=1)
        self.ent = Entry(self.root)
        self.ent.grid(row=0, column=2)
        Button(self.root, text='查找', command=self.mysearch).place(x=190)
        Button(self.root, text='退出', command=self.kill).place(x=245)
        self.ent.bind("<Key>", self.mysearch)
        self.root.wait_window()

    def mysearch(self, *args):
        self.parents.text[self.parents.note.index(self.parents.note.select())].tag_remove("found", "1.0", END)
        start = "1.0"
        try:
            key = self.parents.text[self.parents.note.index(self.parents.note.select())].get(SEL_FIRST, SEL_LAST)
        except TclError:
            key = self.ent.get()
        if len(key.strip()) == 0:
            return
        while True:
            pos = self.parents.text[self.parents.note.index(self.parents.note.select())].search(key, start, END)
            # print("pos= ",pos) # pos=  3.0  pos=  4.0  pos=
            if pos == "":
                break
            self.parents.text[self.parents.note.index(self.parents.note.select())].tag_add("found", pos,
                                                                                           "%s+%dc" % (pos, len(key)))
            start = "%s+%dc" % (pos, len(key))

    def kill(self):
        self.parents.text[self.parents.note.index(self.parents.note.select())].tag_remove("found", "1.0", END)
        self.root.destroy()


class MediaPlayer(Frame):
    def __init__(self, master: Window, path):
        super().__init__(master)
        self.path = path
        self.flag = 0
        self.parents = master
        self.sound = 0.5
        music.init()
        music.music.load(path)
        music.music.set_volume(self.sound)
        self.audio = MP3(self.path)
        self.pack(fill=BOTH, expand=YES)
        self.hdr_var = StringVar()
        self.elapsed_var = DoubleVar(value=0)
        self.remain_var = DoubleVar(value=190)
        self.is_change = False

        self.create_header()
        self.create_media_window()
        self.create_progress_meter()
        self.create_buttonbox()

    def create_header(self):
        """The application header to display user messages"""
        Label(self, text=self.path).grid(sticky=W, row=0)
        Label(self, text=f'文件名: {os.path.basename(self.path)}').grid(sticky=W, row=1)
        Label(self, text=f'文件类型: {self.path.split(".")[-1]}').grid(sticky=W, row=2)
        Separator(self).grid(sticky=W, row=3)
        Label(self, text=f'音频类型: {self.path.split(".")[-1]}音频').grid(sticky=W, row=4)
        Label(self, text=f'音频长度: {int(self.audio.info.length // 60)}分{int(self.audio.info.length % 60)}秒').grid(
            sticky=W, row=5)

    def create_media_window(self):
        """Create frame to contain media"""
        img_path = Path(__file__).parent / 'assets/mp_background.png'
        # self.demo_media = PhotoImage(file=img_path)
        # self.media = Label(self, image=self.demo_media)
        # self.media = Label(self)
        # self.media.pack(fill=BOTH, expand=YES)

    def create_progress_meter(self):
        """Create frame with progress meter with labels"""
        pass
        # container = Frame(self)
        # container.pack(fill=X, expand=YES, pady=10)

        # self.elapse = Label(container, text='00:00')
        # self.elapse.pack(side=LEFT, padx=10)
        # self.audio = MP3(self.path)
        # self.scale = Scale(
        #     master=container,
        #     command=self.on_progress,
        #     bootstyle=SECONDARY
        # )
        # self.scale.bind("<Button-1>",self.start_change)
        # self.scale.bind("<ButtonRelease-1>",self.stop_change)
        # self.scale.pack(side=LEFT, fill=X, expand=YES)
        # times = self.audio.info.length
        # x = int(times // 60)
        # if x < 10: x = f'0{x}'
        # times = f'{x}:{int(times % 60)}'
        # self.remain = Label(container, text=times)
        # self.remain.pack(side=LEFT, fill=X, padx=10)

    def set_sound(self, add):
        self.sound += add
        if self.sound < 0:
            self.sound = 0
        elif self.sound > 1:
            self.sound = 1
        music.music.set_volume(self.sound)

    def start_change(self, event=None):
        self.is_change = True

    def stop_change(self, event=None):
        self.is_change = False

    def play(self):
        # music.music.play()
        music.music.unload()
        music.music.load(self.path)
        threading.Thread(target=music.music.play).start()
        # multiprocessing.Process(target=self.play_).start()
        # threading.Thread(target=self.set_scale).start()
        while self.winfo_exists: pass
        music.music.stop()

    # def set_scale(self):
    #     x=1/self.audio.info.length
    #     while True:
    #         if not self.is_change:
    #             threading.Thread(target=lambda: self.scale.set(self.scale.get()+x)).start()
    #             # self.scale.set(self.scale.get()+x)
    #             time.sleep(1)
    def create_buttonbox(self):
        """Create buttonbox with media controls"""
        digit_func = self.register(validate_number)
        container = Frame(self)
        void = Frame(self)
        void.grid(sticky=W, row=6)
        container.grid(sticky=W, row=7)
        # Style().configure('TButton', font="-size 20")
        rev_btn = Button(
            master=void,
            text=Emoji.get('SPEAKER WITH THREE SOUND WAVES'),
            padding=10,
            command=lambda: self.set_sound(0.1),
            bootstyle=SECONDARY,
            width=5
        )
        rev_btn.pack(side=LEFT, expand=YES, fill=X)

        play_btn = Button(
            master=container,
            text=Emoji.get('black right-pointing triangle'),
            padding=10,
            command=lambda: threading.Thread(target=self.play).start(),
            width=5
        )

        fwd_btn = Button(
            master=void,
            text=Emoji.get('SPEAKER WITH ONE SOUND WAVE'),
            padding=10,
            command=lambda: self.set_sound(-0.1),
            bootstyle=SECONDARY,
            width=5
        )
        play_btn.pack(side=LEFT, fill=X, expand=YES)
        fwd_btn.pack(side=LEFT, fill=X, expand=YES)

        pause_btn = Button(
            master=container,
            text=Emoji.get('double vertical bar'),
            padding=10,
            command=music.music.pause,
            width=5
        )
        pause_btn.pack(side=LEFT, fill=X, expand=YES)

        stop_btn = Button(
            master=container,
            text=Emoji.get('black square for stop'),
            padding=10,
            command=music.music.unpause,
            width=5
        )
        stop_btn.pack(side=LEFT, fill=X, expand=YES)
        Label(self, text='跳转').grid(row=7, column=1, sticky=W)
        self.ent = Spinbox(self, width=5, from_=0, to=10000, validate="focus", validatecommand=(digit_func, '%P'))
        self.ent.set(0)
        self.ent.grid(row=7, column=2)
        Label(self, text='分').grid(row=7, column=3)
        self.ent2 = Spinbox(self, width=5, from_=0, to=59, validate="focus", validatecommand=(digit_func, '%P'))
        self.ent2.grid(row=7, column=4)
        self.ent2.set(0)
        Label(self, text='秒').grid(row=7, column=5)
        self.img = ImageTk.PhotoImage(Image.open('.\\icon\\flush.gif').resize((20, 20)))
        Button(self, image=self.img, bootstyle=SUCCESS, command=self.run).grid(row=7, column=6)

    def run(self):
        try:
            music.music.set_pos(int(self.ent.get()) * 60 + int(self.ent2.get()))
        except ValueError:
            Messagebox.show_error('无法转换输入!', '错误')

    def insert(self, *args, **kwargs):
        pass

    def get(self, *args, **kwargs):
        return ''

    def index(self, *args, **kwargs):
        return '1.0'

    def delete(self, *args, **kwargs):
        pass

    def edit_undo(self):
        pass

    def edit_redo(self):
        pass

    def tag_configure(self, *args, **kwargs):
        pass

    def bind(self, *args, **kwargs):
        pass


class PhotoEdit(Frame):
    def __init__(self, parents, path):
        super().__init__(parents)
        self.parents = parents
        # global img
        self.x = Image.open(path)
        h = 485
        w = 1000
        Label(self, text=os.path.basename(path)).pack(anchor=NW)
        Label(self,
              text=f'图片尺寸: {self.x.width}x{self.x.height}    图片格式: .{os.path.basename(path).split(".")[-1]}').pack(
            anchor=NW)
        self.x = self.x.resize((w, int(self.x.height * (w / self.x.width))))
        if self.x.height > h:
            self.x = self.x.resize((int(self.x.width * (h / self.x.height)), h))
        self.img = ImageTk.PhotoImage(self.x)
        self.lb = Label(self, image=self.img)
        self.lb.pack(fill=BOTH, expand=YES)
        # super().bind("<Control-o>", lambda: self.parents.master.choose())
        self.tag_config = self.tag_configure

    def insert(self, *args, **kwargs):
        pass

    def get(self, *args, **kwargs):
        return ''

    def index(self, *args, **kwargs):
        return '1.0'

    def delete(self, *args, **kwargs):
        pass

    def edit_undo(self): pass

    def edit_redo(self): pass

    def tag_configure(self, *args, **kwargs):
        pass

    def bind(self, *args, **kwargs):
        pass


class TextEdit(Frame):
    def __init__(self, parents, cnf={}, **kw):
        super().__init__(parents)
        self.parents = parents
        self.LineText = Text(self, width=5, bd=0, font=("consolas", 10), takefocus=0,
                             state="disabled", cursor="arrow", relief='flat', borderwidth=1, spacing1=4)
        self.LineText.pack(side="left", expand=NO, fill=Y)
        self.TerminalText = Text(self, cnf, **kw)
        self.stp = Scrollbar(self, command=self.scroll, bootstyle=ROUND)
        self.TerminalText.pack(fill=BOTH, expand=YES, side=LEFT)
        self.thread_lock = threading.Lock()
        self.TerminalText.config(yscrollcommand=self.stp.set)
        self.LineText.config(yscrollcommand=self.stp.set)
        self.LineText.bind("<MouseWheel>", self.wheel)
        self.TerminalText.bind("<MouseWheel>", self.wheel)
        self.TerminalText.bind("<Key>", lambda e: self.get_txt_thread())
        self.TerminalText.configure(yscrollcommand=self.stp.set)
        self.LineText.configure(yscrollcommand=self.stp.set)
        self.stp.pack(side=RIGHT, fill=Y)
        self.txt = ''
        self.LineText.tag_config('SteelBlue', foreground='SteelBlue')
        self.TerminalText.bind("<Return>", self.enter)
        self.TerminalText.bind("<[>", lambda e: threading.Thread(target=self.printer, args=(']',)).start())
        self.TerminalText.bind("<(>", lambda e: threading.Thread(target=self.printer, args=(')',)).start())
        self.TerminalText.bind("<{>", lambda e: threading.Thread(target=self.printer, args=('}',)).start())
        self.TerminalText.bind("<'>", lambda e: threading.Thread(target=self.printer, args=('\'',)).start())
        self.TerminalText.bind("<\">", lambda e: threading.Thread(target=self.printer, args=('"',)).start())
        threading.Thread(target=self.set_func).start()
        self.get_txt_thread()
        # self.TerminalText.see(1.0)

    def set_func(self):
        self.tag_config = self.tag_configure
        self.config = self.TerminalText.config
        self.configure = self.TerminalText.configure
        self.tag_raise = self.TerminalText.tag_raise
        self.tag_add = self.TerminalText.tag_add
        self.tag_ranges = self.TerminalText.tag_ranges
        self.tag_remove = self.TerminalText.tag_remove
        self.tag_names = self.TerminalText.tag_names
        self.tag_delete = self.TerminalText.tag_delete
        self.tag_nextrange = self.TerminalText.tag_nextrange
        self.tag_prevrange = self.TerminalText.tag_prevrange

    def printer(self, v):
        if self.parents.master.is_coding.get():
            time.sleep(0.01)
            if v == '"':
                if self.TerminalText.get(1.0, float(self.TerminalText.index(INSERT))).count('"') % 2 == 1:
                    self.TerminalText.insert(float(self.TerminalText.index(INSERT)), v)
                    self.TerminalText.mark_set("insert", "insert-1c")
            elif v == "'":
                if self.TerminalText.get(1.0, float(self.TerminalText.index(INSERT))).count("'") % 2 == 1:
                    self.TerminalText.insert(float(self.TerminalText.index(INSERT)), v)
                    self.TerminalText.mark_set("insert", "insert-1c")
            else:
                self.TerminalText.insert(float(self.TerminalText.index(INSERT)), v)
                self.TerminalText.mark_set("insert", "insert-1c")

    def set_font(self, font: Font):
        self.TerminalText.config(font=font)
        self.LineText.config(font=Font(family="consolas", size=int(font.cget('size'))))

    def enter(self, *args):
        if self.parents.master.is_coding.get():
            a = float(self.TerminalText.index('insert'))
            b = self.TerminalText.get(float(int(a)), a).replace('\n', '')
            c = b
            # if b[-1:] == ':':
            #      i = 1
            # else:
            #      i = 0
            i = 1 if b[-1:] == ':' else 0
            while True:
                if b[:4] == '     ':
                    b = b[4:]
                    i += 1
                else:
                    break
            if c.strip() == 'break' or c.strip() == 'return' or c.strip() == 'pass' or c.strip() == 'continue':
                i -= 1
            self.TerminalText.insert('insert', '\n')
            self.TerminalText.insert('insert', '     ' * i)
            self.TerminalText.mark_set("insert", "insert-1c")
            # return 'break'

    def tag_configure(self, tag, background='#000000', foreground='#000000'):
        self.TerminalText.tag_configure(tag, background=background, foreground=foreground)

    def index(self, index):
        return self.TerminalText.index(index)

    def insert(self, index, text):
        return self.TerminalText.insert(index, text)

    def delete(self, index1, index2):
        return self.TerminalText.delete(index1, index2)

    def get(self, index1, index2):
        return self.TerminalText.get(index1, index2)

    def edit_undo(self):
        self.TerminalText.edit_undo()

    def edit_redo(self):
        self.TerminalText.edit_redo()

    def see(self, index):
        self.LineText.see(index)
        return self.TerminalText.see(index)

    def bind(self, sue, func, add=None):
        self.TerminalText.bind(sue, func, add)

    def wheel(self, event):
        self.LineText.yview_scroll(int(-1 * (event.delta / 120)), "units")
        self.TerminalText.yview_scroll(int(-1 * (event.delta / 120)), "units")
        return "break"

    def scroll(self, *xy):
        self.LineText.yview(*xy)
        self.TerminalText.yview(*xy)

    def get_txt_thread(self):
        threading.Thread(target=self.get_txt).start()

    def get_txt(self):
        self.thread_lock.acquire()
        if self.txt != self.TerminalText.get("1.0", "end")[:-1]:
            self.txt = self.TerminalText.get("1.0", "end")[:-1]
            self.show_line()
        else:
            self.thread_lock.release()
        self.update()
        # self.TerminalText.see(1.0)
        # self.LineText.see(1.0)
        # self.LineText.see(1.0)

    def show_line(self):
        sb_pos = self.stp.get()
        self.LineText.configure(state="normal")
        self.LineText.delete("1.0", "end")
        txt_arr = self.txt.split("\n")
        if len(txt_arr) == 1:
            self.LineText.insert("1.1", " 1")
        else:
            for i in range(1, len(txt_arr) + 1):
                if i < 10:
                    self.LineText.insert("end", f'  {i} ', 'SteelBlue')
                elif i < 100:
                    self.LineText.insert("end", f' {i} ', 'SteelBlue')
                elif i < 1000:
                    self.LineText.insert("end", f'{i} ', 'SteelBlue')
                else:
                    self.LineText.insert("end", f'{i}', 'SteelBlue')
                if i != len(txt_arr):
                    self.LineText.insert("end", "\n")
        if len(sb_pos) == 4:
            self.LineText.yview_moveto(0.0)
        elif len(sb_pos) == 2:
            self.LineText.yview_moveto(sb_pos[0])
            self.TerminalText.yview_moveto(sb_pos[0])
        self.LineText.configure(state="disabled")
        try:
            self.thread_lock.release()
        except RuntimeError:
            pass


class MainWindow(Window):
    text: List[TextEdit]

    def __init__(self):
        self.txt = ""
        super().__init__(size=(1171, 600), position=(375, 240))
        self.iconbitmap(os.path.join(os.path.dirname(sys.argv[0]), '.\\icon\\notepad.ico'))
        got_path = self.get_path()
        self.name = [got_path[1]]
        self.paths = [got_path[0]]
        self.title(f"python记事本 - {self.name[0]}")
        self.fontname = Font(family="Microsoft YaHei UI", size=10)
        self.Status = BooleanVar()
        self.Status2 = IntVar()
        self.Status3 = BooleanVar()
        self.is_highlighter = BooleanVar()
        self.is_coding = BooleanVar()
        self.is_coding.set(False)
        self.encoding = ""
        self.theme = 'sandstone'
        self.theme_chinese = {'sandstone': '亮色主题', 'darkly': '暗色主题', 'vapor': '紫色主题', 'solar': '蓝色主题',
                              'superhero': '灰色主题'}
        self.show()

        # def tags(keys):
        #      start = "1.0"
        #      if keys is not None:
        #            for key in keys:
        #                 if len(key.strip()) == 0:
        #                      return
        #                 while True:
        #                      pos = self.text[self.note.index(self.note.select())].search(key, start, END)
        #                      # print("pos= ",pos) # pos=  3.0  pos=  4.0  pos=
        #                      if pos == "":
        #                            break
        #                      self.text[self.note.index(self.note.select())].tag_add("web", pos, "%s+%dc" % (pos, len(key)))
        #                      start = "%s+%dc" % (pos, len(key))
        #
        # a = re.compile('http(s?)://(?:[-\w.]|(?:%[\da-fA-F]{2}))+')
        # tags(a.findall(self.text[self.note.index(self.note.select())].get(1.0, END)))

    def get_scale(self):
        app = Scales()
        app.show(self)
        print(app.s["get"])
        return int(app.s["get"])

    help31 = lambda event=None, get=None: Messagebox.show_info(f"python快乐记事本\n\
Ctrl+s保存,Ctrl+B运行pyw,F5运行py,Ctrl+w退出\nCtrl+L文本长度\
Ctrl+o打开,Alt+C代码高亮\nCtrl+/注释,Ctrl+]增加缩进,Ctrl+[取消缩进\n\
Ctrl+Alt+u增加行,Ctrl+Alt+p删除行\n\
如遇不小心选择超大文件导致之后打开时卡死,\n\
请删除C:/Users/{getpass.getuser()}/AppData/Local/Temp/\npython_notepad.tmp\n\
目前不支持m4a播放,pdf显示", "帮助")

    def lcut(self):
        threading.Thread(
            target=lambda: Messagebox.show_info("正在统计,可能需要一些时间,\n请耐心等待数秒钟", "build")).start()

        def cut():
            a = jieba.lcut(self.text[self.note.index(self.note.select())].get(1.0, END))
            counts = {}
            for word in a:
                if len(word) == 1:
                    continue
                else:
                    rword = word
                counts[rword] = counts.get(rword, 0) + 1
            items = list(counts.items())
            items.sort(key=lambda x: x[1], reverse=True)
            x = ""
            i = 0
            while True:
                try:
                    word, count = items[i]
                    x += "{0:<10}{1:>5}\n".format(word, count)
                except IndexError:
                    break
                i += 1
            print(x)
            self.show_info(x, '词频统计')
            # with open(f"C:/Users/{getpass.getuser()}"
            #           "/AppData/Local/Temp/python_notepad_chinese_words_for_15.python_notepad",
            #           "wt") as fo:
            #     fo.write(x)
            #     fo.close()
            # subprocess.Popen(
            #     f"main.exe C:/Users/{getpass.getuser()}/AppData/Local/Temp/python_notepad_chinese_words_for_15.python_notepad")

        threading.Thread(target=cut).start()

    @staticmethod
    def choosecolor():
        return askcolor(title="颜色选择器")

    def big_small(self, low=True):
        try:
            if low:
                get = str(self.text[self.note.index(self.note.select())].get(SEL_FIRST, SEL_LAST))
                self.text[self.note.index(self.note.select())].delete(SEL_FIRST, SEL_LAST)
                self.text[self.note.index(self.note.select())].insert(INSERT, get.lower())
            elif low is None:
                get = str(self.text[self.note.index(self.note.select())].get(SEL_FIRST, SEL_LAST))
                self.text[self.note.index(self.note.select())].delete(SEL_FIRST, SEL_LAST)
                for i in get:
                    if 65 <= ord(i) <= 90:
                        self.text[self.note.index(self.note.select())].insert(INSERT, i.lower())
                    else:
                        self.text[self.note.index(self.note.select())].insert(INSERT, i.upper())
            elif low == '':
                get = str(self.text[self.note.index(self.note.select())].get(SEL_FIRST, SEL_LAST))
                self.text[self.note.index(self.note.select())].delete(SEL_FIRST, SEL_LAST)
                self.text[self.note.index(self.note.select())].insert(INSERT, get[0].upper())
                self.text[self.note.index(self.note.select())].insert(INSERT, get[1:])
            else:
                get = str(self.text[self.note.index(self.note.select())].get(SEL_FIRST, SEL_LAST))
                self.text[self.note.index(self.note.select())].delete(SEL_FIRST, SEL_LAST)
                self.text[self.note.index(self.note.select())].insert(INSERT, get.upper())
        except TclError:
            Messagebox.show_error("您未选择任何内容!", "大小写转换")

    def textcolor(self):
        for i in self.text:
            i.config(highlightbackground=self.choosecolor()[1])

    def _insert(self, get):
        self.text[self.note.index(self.note.select())].delete(1.0, END)
        self.text[self.note.index(self.note.select())].insert(END, "\n".join(get))
        self.text[self.note.index(self.note.select())].delete(1.0, 1.0)

    def sort(self, reverse=False):
        get = self.text[self.note.index(self.note.select())].get(1.0, END).split("\n")
        get.sort()
        if reverse:
            get = get[::-1]
        self._insert(get)

    def reverse(self):
        get = self.text[self.note.index(self.note.select())].get(1.0, END).split("\n")[::-1]
        self._insert(get)

    def shuffle(self):
        get = self.text[self.note.index(self.note.select())].get(1.0, END).split("\n")
        random.shuffle(get)
        self._insert(get)

    def deduplication(self):
        get = self.text[self.note.index(self.note.select())].get(1.0, END).split("\n")
        get = list(dict.fromkeys(get))
        self._insert(get)

    @staticmethod
    def show_info(string, title):
        # root = Window(title=title, size=(570, 400), position=(620, 250), resizable=(False, False))
        root = Toplevel()
        root.title(title)
        root.geometry('570x400+620+250')
        root.resizable(False, False)
        root.iconbitmap(os.path.join(os.path.dirname(sys.argv[0]), '.\\icon\\notepad.ico'))
        text = ScrolledText(root, background="white", relief=FLAT)
        text.pack()
        text.insert(1.0, string)
        text.configure(state='disabled')
        root.mainloop()

    @staticmethod
    def show_file(path, lengh, gets):
        root = Window(title="文件信息", size=(300, 200), position=(620, 250))
        root.iconbitmap(os.path.join(os.path.dirname(sys.argv[0]), '.\\icon\\notepad.ico'))
        try:
            get = os.stat(path)
        except FileNotFoundError:
            root.destroy()
            Messagebox.show_error('系统找不到指定的路径', '错误')
        else:
            m = os.path.getsize(path)

            s = (
                ("文件大小:", f"{round(m / 1024, 1)}KB,{round(m / 1024 / 1024, 1)}MB"),
                ("访问日期:", datetime.fromtimestamp(get.st_atime)),
                ("修改日期:", datetime.fromtimestamp(get.st_mtime)),
                ("创建日期:", datetime.fromtimestamp(get.st_ctime)),
                ("文本长度:", lengh),
                ("文本行数:", gets.count("\n"))
            )
            y = 0
            for i, x in s:
                Label(root, text=f"{i}{x}", background="white").grid(row=y, pady=5, padx=10)
                y += 1
            root.mainloop()

    def color(self):
        r = self.choosecolor()[1]
        self.text[self.note.index(self.note.select())].config(background=r)

    def colors(self):
        r = self.choosecolor()[1]
        self.text[self.note.index(self.note.select())].config(foreground=r)

    @staticmethod
    def date():
        begin = Querybox.get_date(title="选择开始日期")
        end = Querybox.get_date(title="选择截止日期")
        days = str((end - begin).days)
        if Messagebox.okcancel(f"日期之差为:{days}点击复制,点X取消", "计算结果"):
            pyperclip.copy(days)

    # @staticmethod
    # def date():
    #      # begin = Querybox.get_date(title="选择开始日期")
    #      # end = Querybox.get_date(title="选择截止日期")
    #      # days = str((end - begin).days)
    #      time_dll=ctypes.windll.LoadLibrary(os.path.join(os.path.abspath(os.curdir),"api-ms-win-time-calculation.dll"))
    #      days=time_dll.dayDis(2023,1,1,2023,1,1)
    #      if Messagebox.okcancel(f"日期之差为:{days}点击复制,点X取消", "计算结果"):
    #            pyperclip.copy(days)
    @staticmethod
    def sqrt_wrong(a):
        if a != "":
            Messagebox.show_error("类型无效", "错误")
            return True
        else:
            return False

    def sqrt(self):
        keep_going = True
        while keep_going:
            a = Querybox.get_string("要开方数", "开方")
            try:
                a = eval(a)
                keep_going = False
            except NameError:
                keep_going = self.sqrt_wrong(a)
            except SyntaxError:
                keep_going = self.sqrt_wrong(a)
        try:
            if Messagebox.okcancel(
                    f"计算结果是:{str(round(pow(a, 0.5), 5))}点击复制,点X取消",
                    "计算结果"):
                pyperclip.copy(a)
        except TypeError:
            pass

    @staticmethod
    def open_path(r):
        with open(f"C:/Users/{getpass.getuser()}/AppData/Local/Temp/python_notepad.tmp", "wt") as fo:
            fo.write(r)
            fo.close()

    def two(self, path):
        with open(path, "wb") as fo:
            hes = self.text[self.note.index(self.note.select())].get("1.0", END).strip()
            hes = bytes.fromhex(
                str(hes).replace(
                    "\t",
                    "").replace(
                    "\n",
                    "").replace(
                    " ",
                    ""))
            fo.write(hes)
            fo.close()

    def to_save(self):
        if not isinstance(self.text[self.note.index(self.note.select())], PhotoEdit):
            if self.two_open_or_not:
                self.two(self.paths[self.note.index(self.note.select())])
            else:
                if "." not in self.paths[self.note.index(self.note.select())] and self.paths[
                    self.note.index(self.note.select())] != "":
                    if str(
                            Messagebox.okcancel(
                                "您未输入文件名，即将转换成txt格式",
                                "格式转换")).strip() == "确定":
                        self.paths[self.note.index(self.note.select())] += ".txt"
                try:
                    self.two(self.paths[self.note.index(self.note.select())])
                except ValueError:
                    try:
                        with open(self.paths[self.note.index(self.note.select())], "wt", encoding="GB2312") as fo:
                            fo.write(self.text[self.note.index(self.note.select())].get("1.0", END))
                            fo.close()
                    except UnicodeError:
                        try:
                            with open(self.paths[self.note.index(self.note.select())], "wt", encoding="UTF-8") as fo:
                                fo.write(self.text[self.note.index(self.note.select())].get("1.0", END))
                                fo.close()
                        except UnicodeError:
                            try:
                                with open(self.paths[self.note.index(self.note.select())], "wt", encoding="GBK") as fo:
                                    fo.write(self.text[self.note.index(self.note.select())].get("1.0", END))
                                    fo.close()
                            except UnicodeError:
                                with open(self.paths[self.note.index(self.note.select())], "wt", encoding="ANSI") as fo:
                                    fo.write(self.text[self.note.index(self.note.select())].get("1.0", END))
                                    fo.close()
            self.name[self.note.index(self.note.select())] = os.path.basename(
                self.paths[self.note.index(self.note.select())])
            print(f"保存文件{self.paths[self.note.index(self.note.select())]}")
            self.title("python记事本 - " + self.name[self.note.index(self.note.select())])
            if os.path.isfile(self.paths[self.note.index(self.note.select())]):
                with open(f"C:/Users/{getpass.getuser()}/AppData/Local/Temp/python_notepad.tmp", "wt") as fo:
                    fo.write(self.paths[self.note.index(self.note.select())])
                    fo.close()
        return self.paths[self.note.index(self.note.select())]

    def save(self, event=None):
        if not isinstance(self.note.index(self.note.select()), PhotoEdit) and not isinstance(
                self.note.index(self.note.select()), MediaPlayer):
            if self.paths[self.note.index(self.note.select())] == "":
                self.paths[self.note.index(self.note.select())] = str(asksaveasfilename(initialfile="新建文本文档.txt",
                                                                                        title="python记事本 - 另存为...",
                                                                                        filetypes=[("文本文档", ".txt"),
                                                                                                   (
                                                                                                       "二维数组/Excel",
                                                                                                       ".csv"),
                                                                                                   ("系统配置", ".ini"),
                                                                                                   (
                                                                                                       "windows批处理文件",
                                                                                                       ".bat .cmd"),
                                                                                                   ("Windows VBScript",
                                                                                                    ".vbs"),
                                                                                                   ("python文件",
                                                                                                    ".py .pyw"),
                                                                                                   (
                                                                                                       "html文件",
                                                                                                       ".html"),
                                                                                                   ("C语言源码", ".c"),
                                                                                                   ("C++源码", ".cpp"),
                                                                                                   (
                                                                                                       "C/C++头文件",
                                                                                                       ".h"),
                                                                                                   ("日志文件", ".log"),
                                                                                                   (
                                                                                                       "HTML文件",
                                                                                                       ".html"),
                                                                                                   (
                                                                                                       "JSON文件",
                                                                                                       ".json"),
                                                                                                   ("所有文件", ".*")]))
            if os.path.isfile(self.paths[self.note.index(self.note.select())]):
                self.paths[self.note.index(self.note.select())] = self.to_save()

    def save_as(self):
        if not isinstance(self.note.index(self.note.select()), PhotoEdit) and not isinstance(
                self.note.index(self.note.select()), MediaPlayer):
            self.paths[self.note.index(self.note.select())] = str(asksaveasfilename(initialfile="新建文本文档.txt",
                                                                                    title="python记事本 - 另存为...",
                                                                                    filetypes=[("文本文档", ".txt"),
                                                                                               ("二维数组/Excel",
                                                                                                ".csv"),
                                                                                               ("系统配置", ".ini"), (
                                                                                                   "windows批处理",
                                                                                                   ".bat",
                                                                                                   ".cmd"),
                                                                                               ("windows VBScript",
                                                                                                ".vbs"),
                                                                                               (
                                                                                                   "python文件", ".py",
                                                                                                   ".pyw"),
                                                                                               ("html文件", ".html"),
                                                                                               ("C语言源码", ".c"),
                                                                                               ("C++源码", ".cpp"),
                                                                                               ("日志文件", ".log"),
                                                                                               ("所有文件", ".*")]))
            self.paths[self.note.index(self.note.select())] = self.to_save()

    def save_all(self):
        if not isinstance(self.note.index(self.note.select()), PhotoEdit) and not isinstance(
                self.note.index(self.note.select()), MediaPlayer):
            for i in range(len(self.paths)):
                if os.path.isfile(self.paths[i]):
                    end = END if eval(self.text[i].index(END)) <= 10.0 else 10.0
                    encoding = chardet.detect(self.text[i].get(1.0, end).encode())['encoding']
                    with open(self.paths[i], 'wt', encoding=encoding) as fo:
                        fo.write(self.text[i].get(1.0, END))

    def len_of_text(self, event=None):
        gets = str(self.text[self.note.index(self.note.select())].get(1.0, END))
        for i in [' ', '\n', '\\', '\t', '/', '?', '!', '>', '<', ',', '=', '+', '_', '@', '#']:
            gets = gets.replace(i, '')
        if Messagebox.okcancel(
                f"文本长度为:{str(len(gets))},点击复制,点X取消\n注:该统计不包含空格、换行、符号\n下方信息栏统计包含所有字符",
                "长度"):
            pyperclip.copy(str(len(gets)))

    def len_of_english_text(self, event=None):
        gets = str(self.text[self.note.index(self.note.select())].get(1.0, END)).replace(".", "").replace("\n",
                                                                                                          "").replace(
            ",", "").replace("?",
                             "").replace(
            "!", "")
        word = gets.split(" ")
        print(word)
        for i in word:
            if i == "" or i == "":
                del word[word.index(i)]
        print(f"\n\n\n\n\n\n{word}")
        if Messagebox.okcancel(f"文本词数为:{str(len(word))},点击复制,点X取消", "长度"):
            pyperclip.copy(str(len(gets)))

    def time_insert(self):
        times = gettime()
        self.text[self.note.index(self.note.select())].insert(
            self.text[self.note.index(self.note.select())].index(INSERT), times)

    def choose_encodings(self, encoding):
        path = self.paths[-1]
        encodings = self.encoding
        try:
            with open(path, "rt", encoding=encoding) as fo:
                read = fo.readlines()
                fo.close()
            self.encoding = encoding
        except FileNotFoundError:
            self.paths[self.note.index(self.note.select())] = path
            self.encoding = encodings
            self.new()
        else:
            self.name.append(os.path.basename(path))
            self.frame.append(Frame(self))
            if os.path.basename(path).split('.')[-1].lower() in (
            'jpg', 'jpeg', 'png', 'gif', 'bmp', 'ico', 'webp', 'ppm', 'sgl', 'tiff'):
                self.text.append(
                    PhotoEdit(self.frame[-1], path))
            elif os.path.basename(path).split('.')[-1].lower() in ('mp3', 'ogg'):
                self.text.append(
                    MediaPlayer(self.frame[-1], path)
                )
            else:
                self.text.append(
                    TextEdit(self.frame[-1], font=self.fontname, undo=True, borderwidth=1))
                self.text[-1].delete("1.0", END)
                for i in read:
                    self.text[-1].insert(END, i)
            self.text[-1].pack(fill=BOTH, expand=YES)
            self.text[-1].tag_configure("found", background="yellow")
            self.note.add(self.frame[-1], text=self.name[-1])
            self.note.select((self.frame[-1]))
            self.binds(self.text[-1])
            # self.up(self.note.index(self.note.select()) + 1)
        print(f"打开文件{self.paths[self.note.index(self.note.select())]}")
        self.label3['text'] = f'|    {self.encoding}    |'
        self.label2['text'] = f'|    共{len(self.text[self.note.index(self.note.select())].get(1.0, END))}个字符'

    @staticmethod
    def saves(string):
        if string != f"C:/Users/{getpass.getuser()}/AppData/Local/Temp/python_notepad_run_c_error.error" \
                and string != "" \
                and string != f"C:/Users/{getpass.getuser()}/AppData/Local/Temp/python_notepad_chinese_words_for_15.python_notepad":
            with open(f"C:/Users/{getpass.getuser()}/AppData/Local/Temp/python_notepad.tmp", "wt") as fo:
                fo.write(string)
                fo.close()

    def chooses(self):
        encoding = self.encoding
        try:
            self.choose_encodings("GBK")
            self.saves(self.paths[self.note.index(self.note.select())])
            self.encoding = 'GBK'
        except UnicodeError:
            try:
                self.choose_encodings("GB2312")
                self.saves(self.paths[self.note.index(self.note.select())])
                self.encoding = 'GB2312'
            except UnicodeError:
                try:
                    self.choose_encodings("UTF-8")
                    self.saves(self.paths[self.note.index(self.note.select())])
                    self.encoding = 'UTF-8'
                except UnicodeError:
                    try:
                        self.choose_encodings("ANSI")
                        self.saves(self.paths[self.note.index(self.note.select())])
                        self.encoding = 'ANSI'
                    except UnicodeError:
                        # try:
                        #    self.choose_encodings("unicode_escape")
                        #    self.saves(self.paths[self.note.index(self.note.select())])
                        # except UnicodeError:
                        try:
                            self.encoding = '二进制'
                            self.name.append(os.path.basename(self.paths[-1]))
                            self.frame.append(Frame(self))
                            if os.path.basename(self.paths[-1]).split('.')[-1].lower() in (
                                    'jpg', 'jpeg', 'png', 'gif', 'bmp', 'ico'):
                                self.text.append(
                                    PhotoEdit(self.frame[-1], self.paths[-1]))
                            elif os.path.basename(self.paths[-1]).split('.')[-1].lower() in ('mp3', 'ogg'):
                                self.text.append(
                                    MediaPlayer(self.frame[-1], self.paths[-1])
                                )
                            else:
                                self.text.append(
                                    TextEdit(self.frame[-1], font=self.fontname, undo=True, borderwidth=1))
                                self.text[-1].delete("1.0", END)
                                with open(self.paths[-1], 'rb') as fo:
                                    self.text[-1].insert(END, hex(int.from_bytes(fo.read())))
                            self.text[-1].pack(fill=BOTH, expand=YES)
                            self.text[-1].tag_configure("found", background="yellow")
                            self.note.add(self.frame[-1], text=self.name[-1])
                            self.note.select((self.frame[-1]))
                            self.binds(self.text[-1])
                        except UnicodeError:
                            Messagebox.show_error("打开失败", "Error")
                            print(f"打开文件{self.paths[self.note.index(self.note.select())]}失败")
                            self.encoding = encoding
                        except TclError:
                            os.remove(f"C:/Users/{getpass.getuser()}/AppData/Local/Temp/python_notepad.tmp")
                            self.show()
        self.update_file()
        self.two_open_or_not = False
        self.name[self.note.index(self.note.select())] = os.path.basename(
            self.paths[self.note.index(self.note.select())])
        self.title("python记事本 - " + self.name[self.note.index(self.note.select())])
        self.label3['text'] = f'|    {self.encoding}    |'
        self.label2['text'] = f'    共{len(self.text[self.note.index(self.note.select())].get(1.0, END))}个字符'
        self.label4['text'] = self.paths[self.note.index(self.note.select())]

    def choose(self, event=None):
        # pathes = str(askopenfilename())
        for pathes in askopenfilenames():
            if pathes != "":
                self.paths.append(pathes)
                self.chooses()
                self.saves(self.paths[self.note.index(self.note.select())])

    def opens(self, mode, encoding):
        encodings = self.encoding
        try:
            self.paths.append(str(askopenfilename()))
            with open(self.paths[-1], mode, encoding=encoding) as fo:
                hel = fo.read()
                fo.close()
            self.name[self.note.index(self.note.select())] = os.path.basename(
                self.paths[self.note.index(self.note.select())])
            self.title("python记事本 - " + self.name[self.note.index(self.note.select())])
            with open(f"C:/Users/{getpass.getuser()}/AppData/Local/Temp/python_notepad.tmp", "wt") as fo:
                fo.write(self.paths[-1])
                fo.close()
            self.encoding = encoding
        except UnicodeError:
            Messagebox.show_error("打开失败", "Error")
            self.encoding = encodings
        else:
            self.name.append(os.path.basename(self.paths[-1]))
            self.frame.append(Frame(self))
            self.text.append(
                TextEdit(self.frame[-1], font=self.fontname, undo=True, borderwidth=1))
            self.text[-1].pack(fill=BOTH, expand=YES)
            self.text[-1].tag_configure("found", background="yellow")
            self.note.add(self.frame[-1], text=self.name[-1])
            self.text[-1].delete("1.0", END)
            self.text[-1].insert(1.0, hel)
            self.note.select()(self.frame[-1])
            self.binds(self.text[-1])
        self.label3['text'] = f'|    {self.encoding}    |'
        self.two_open_or_not = False

    def open_two(self):
        try:
            self.paths.append(str(askopenfilename()))
            with open(self.paths[self.note.index(self.note.select())], "rb") as fo:
                self.two_open_or_not = True
                hes = "".join(["%02x" % b for b in fo.read()])
                hel = ""
                for i in range(len(hes)):
                    hel += hes[i]
                    if (i + 1) % 4 == 0:
                        hel += "\t"
                    if (i + 1) % 60 == 0:
                        hel += "\n"
                fo.close()
            self.name[self.note.index(self.note.select())] = os.path.basename(
                self.paths[-1])
            self.title("python记事本 - " + self.name[self.note.index(self.note.select())])
            with open(f"C:/Users/{getpass.getuser()}/AppData/Local/Temp/python_notepad.tmp", "wt") as fo:
                fo.write(self.paths[self.note.index(self.note.select())])
                fo.close()
        except UnicodeError:
            Messagebox.show_error("打开失败", "Error")
            self.name[self.note.index(self.note.select())] = "无标题"
            self.title("python记事本 - " + self.name[self.note.index(self.note.select())])
        else:
            self.name.append(os.path.basename(self.paths[-1]))
            self.frame.append(Frame(self))
            self.text.append(
                TextEdit(self.frame[-1], font=self.fontname, undo=True, borderwidth=1))
            self.text[-1].pack(fill=BOTH, expand=YES)
            self.text[-1].tag_configure("found", background="yellow")
            self.note.add(self.frame[-1], text=self.name[-1])
            self.text[-1].delete("1.0", END)
            self.text[-1].insert(1.0, hel)
            self.note.select(self.frame[-1])
            self.binds(self.text[-1])

    def copy_get(self):
        try:
            pyperclip.copy(self.text[self.note.index(self.note.select())].get(SEL_FIRST, SEL_LAST))
        except TclError:
            pass

    def copy_cut(self):
        pyperclip.copy(self.text[self.note.index(self.note.select())].get(SEL_FIRST, SEL_LAST))
        self.text[self.note.index(self.note.select())].delete(SEL_FIRST, SEL_LAST)

    def tk_quit(self):
        save_or_not = None
        try:
            save_or_not = str(
                Messagebox.okcancel(
                    "你需要保存吗?\n如果不保存,您可能丢失信息",
                    "保存")).strip()
            if save_or_not == "确定":
                self.save_all()
            if not (save_or_not == "") and not (save_or_not is None):
                self.quit()
                sys.exit()
        except UnicodeDecodeError:
            if not (save_or_not is None):
                sys.exit()

    def Styles(self, theme):
        Style(theme=theme)
        self.theme = theme
        self.label_theme['text'] = f'|    {self.theme_chinese[self.theme]}'
        # cdg = idc.ColorDelegator()
        # cdg.prog = re.compile(rf'\b(?P<MYGROUP>tkinter)\b|{idc.make_pat()}', re.S)
        # cdg.idprog = re.compile(r'\s+(\w+)', re.S)
        #
        # cdg.tagdefs['MYGROUP'] = {'foreground': '#7F7F7F', 'background': '#FFFFFF'}
        #
        # # These five lines are optional. If omitted, default colours are used.
        # cdg.tagdefs['COMMENT'] = {'foreground': '#FF0000', 'background': '#FFFFFF'}
        # cdg.tagdefs['KEYWORD'] = {'foreground': '#007F00', 'background': '#FFFFFF'}
        # cdg.tagdefs['BUILTIN'] = {'foreground': '#7F7F00', 'background': '#FFFFFF'}
        # cdg.tagdefs['STRING'] = {'foreground': '#7F3F00', 'background': '#FFFFFF'}
        # cdg.tagdefs['DEFINITION'] = {'foreground': '#007F7F', 'background': '#FFFFFF'}
        #
        # idp.Percolator(self.text[self.note.index(self.note.select())]).insertfilter(cdg)

    # self.text[self.note.index(self.note.select())].tag_configure("True", foreground="red")
    # self.text[self.note.index(self.note.select())].tag_configure("False", foreground="red")

    def open_web(self, event=None):
        try:
            a = self.text[self.note.index(self.note.select())].get(SEL_FIRST, SEL_LAST)
        except TclError:
            a = Querybox.get_string("请输入要打开的网页", "打开网页")
        if a != "" and a is not None:
            webbrowser.open(a)

    def run_module(self, event=None):
        self.save()
        try:
            os.system(
                f"start python {self.paths[self.note.index(self.note.select())]}")
            # exec(open(self.paths[self.note.index(self.note.select())]).read())
        except Exception as ex:
            Messagebox.show_error(traceback.format_exc(), "错误")

    def pyw(self, event=None):
        self.save()
        try:
            os.system(
                f"start pythonw {self.paths[self.note.index(self.note.select())]}")
            # exec(open(self.paths[self.note.index(self.note.select())]).read())
        except Exception as ex:
            Messagebox.show_error(traceback.format_exc(), "错误")

    def undo(self):
        try:
            self.text[self.note.index(self.note.select())].edit_undo()
        except TclError:
            pass

    def redo(self):
        try:
            self.text[self.note.index(self.note.select())].edit_redo()
        except TclError:
            pass

    def deletes(self):
        try:
            self.text[self.note.index(self.note.select())].delete(SEL_FIRST, SEL_LAST)
        except TclError:
            pass

    def new(self, event=None):
        self.name.append('无标题')
        self.frame.append(Frame(self))
        self.text.append(
            TextEdit(self.frame[-1], font=self.fontname, undo=True, borderwidth=1))
        self.text[-1].pack(fill=BOTH, expand=YES)
        self.text[-1].tag_configure("found", background="yellow")
        self.note.add(self.frame[-1], text=self.name[-1])
        self.text[-1].delete("1.0", END)
        self.paths.append('')
        self.paths[self.note.index(self.note.select())] = ''
        # self.title("python记事本 - 无标题")
        self.name[-1] = "无标题"
        self.text[-1].delete(1.0, END)
        self.saves(self.paths[self.note.index(self.note.select())])
        self.binds(self.text[-1])
        self.up(self.note.index(self.note.select()) + 1)

    @staticmethod
    def get_path():
        try:
            a = sys.argv[1]
        except IndexError:
            a = None
        if a is None:
            try:
                with open(f"C:/Users/{getpass.getuser()}/AppData/Local/Temp/python_notepad.tmp", "rt") as fo:
                    pathes = fo.read()
                    fo.close()
            except FileNotFoundError:
                with open(f"C:/Users/{getpass.getuser()}/AppData/Local/Temp/python_notepad.tmp", "wt") as fo:
                    pathes = ""
                    fo.close()
            if not (os.path.isfile(pathes)):
                pathes = ""
        else:
            pathes = a
        nams = os.path.basename(pathes)
        if nams == "" or nams is None:
            nams = "无标题"
        return pathes, nams

    def row_column(self, *args):
        if self.is_see_rows:
            try:
                index = str(self.text[self.note.index(self.note.select())].index(INSERT)).split(".")
            except TclError:
                index = ('0', '0')
            text = f'第{index[0]}行  第{int(index[1]) + 1}列'
            # print(len(text))
            if len(text) >= 12:
                self.label.config(text=text)  # 750 14
                self.label.place(x=740, y=self.lb.winfo_y())
            else:
                self.label.config(text=text)
                self.label.place(x=750, y=self.lb.winfo_y())
        else:
            self.label.config(text='')
            self.label.place(x=750, y=self.lb.winfo_y())

    def rows(self, *args):
        self.is_see_rows = self.Status3.get()
        self.label.config(text='')

    def add(self, tab):
        index = self.text[self.note.index(self.note.select())].index(INSERT).split(".")
        string = str(index[0]) + ".0"
        if self.text[self.note.index(self.note.select())].get(string) != tab:
            self.text[self.note.index(self.note.select())].insert(string, tab)
        else:
            a = self.text[self.note.index(self.note.select())].get(1.0, string)
            string = str(index[0]) + ".1"
            b = self.text[self.note.index(self.note.select())].get(string, END)
            self.text[self.note.index(self.note.select())].delete(1.0, END)
            self.text[self.note.index(self.note.select())].insert(END, a)
            self.text[self.note.index(self.note.select())].insert(END, b)

    def add_tabs(self, *args):
        index = self.text[self.note.index(self.note.select())].index(INSERT).split(".")
        string = str(index[0]) + ".0"
        self.text[self.note.index(self.note.select())].insert(string, "\t")

    def adds(self, *args):
        index = self.text[self.note.index(self.note.select())].index(INSERT).split(".")
        string = str(index[0]) + ".0"
        if self.text[self.note.index(self.note.select())].get(string) == "\t":
            a = self.text[self.note.index(self.note.select())].get(1.0, string)
            string = str(index[0]) + ".1"
            b = self.text[self.note.index(self.note.select())].get(string, END)
            self.text[self.note.index(self.note.select())].delete(1.0, END)
            self.text[self.note.index(self.note.select())].insert(END, a)
            self.text[self.note.index(self.note.select())].insert(END, b)

    def addn(self, *args):
        self.text[self.note.index(self.note.select())].insert(
            self.text[self.note.index(self.note.select())].index(INSERT), "\n")

    def delete(self, *args):
        index = str(self.text[self.note.index(self.note.select())].index(INSERT)).split(".")[0]
        self.text[self.note.index(self.note.select())].delete((index + ".0"), (index + ".end"))

    # print("start= ",start) # start=  3.0+3c  start=  4.0+3c

    def large(self, event=None):
        if not self.larges:
            self.state("zoomed")
            self.larges = True
        else:
            self.state("normal")
            self.larges = False

    def run_modules(self, string):
        if Messagebox.okcancel("你要保存并运行吗?", "运行").strip() == "确定":
            self.save()
            subprocess.Popen(string)

    @staticmethod
    def gcc(order, paths):
        gets = subprocess.getoutput(f"{order} {paths}")
        if gets == "" or gets is None:
            Messagebox.show_info("编译成功", "运行")
            subprocess.Popen("a.exe")
        else:
            with open(f"C:/Users/{getpass.getuser()}/AppData/Local/Temp/python_notepad_run_c_error.error", "wt") as fo:
                fo.write(gets)
                fo.close()
            subprocess.Popen(f"main C:/Users/{getpass.getuser()}/AppData/Local/Temp/python_notepad_run_c_error.error")

    def enters(self):
        get = self.Status.get()
        if get:
            self.text[self.note.index(self.note.select())].configure(wrap="word")
        else:
            self.text[self.note.index(self.note.select())].configure(wrap="none")

    def search_web(self):
        try:
            webbrowser.open(
                f'https://cn.bing.com/search?q={self.text[self.note.index(self.note.select())].get(SEL_FIRST, SEL_LAST)}')
        except TclError:
            get = Querybox.get_string("关键词", "搜索")
            print(get)
            if get is not None:
                webbrowser.open(f'https://cn.bing.com/search?q={get}')

    def file_info(self):
        try:
            self.show_file(self.paths[self.note.index(self.note.select())], len(
                self.text[self.note.index(self.note.select())].get("1.0", END)),
                           self.text[self.note.index(self.note.select())].get("1.0", END))
        except TclError:
            pass

    def linecolor(self):
        for i in self.text:
            i.LineText.tag_configure("SteelBlue", foreground=self.choosecolor()[1])

    def copy_file(self):
        path = asksaveasfilename(filetypes=(('文本文档', '.txt'), ('所有文件', '.*')))
        if path != '':
            with open(path, 'wt') as fo:
                fo.write(self.text[self.note.index(self.note.select())].get("1.0", END))
            self.paths.append(path)
            self.chooses()

    def set_font(self):
        font_, ok = Querybox.get_font()
        # if font[1]:
        if ok:
            self.fontname = font_
            for i in self.text:
                i.set_font(font=font_)
        # self.label.config(font=font)
        # self.label2.config(font=font)
        # self.label3.config(font=font)
        # self.label4.config(font=font)

    def config_font(self, mode='+'):
        size = int(self.fontname.cget('size')) + (1 if mode == '+' else -1)
        if size < 5:
            size = 5
        self.fontname.config(size=size)
        for i in self.text:
            i.set_font(self.fontname)

    def recover_font(self):
        self.fontname.config(size=10)
        for i in self.text:
            i.set_font(self.fontname)

    def dragged_files(self, file):
        self.paths[self.note.index(self.note.select())] = file[0].decode(encoding='UTF-8')
        print(self.paths[self.note.index(self.note.select())])
        if os.path.isfile(self.paths[self.note.index(self.note.select())]):
            self.name[self.note.index(self.note.select())] = os.path.basename(
                self.paths[self.note.index(self.note.select())])
            self.title(f'python记事本 - {self.name[self.note.index(self.note.select())]}')
            print(file)
            print(len(file))
            print(self.paths[self.note.index(self.note.select())])
            self.chooses()
        else:
            Messagebox.show_error('你选择的文件不存在或者你选择了文件夹', '错误')

    def post_input_list(self):
        def setit(set_message):
            posting.destroy()

        posting = Toplevel(self, bg='#ffffff')
        posting.iconbitmap(os.path.join(os.path.dirname(sys.argv[0]), '.\\icon\\notepad.ico'))
        posting.title('文件列表')
        posting.geometry('400x300')
        posting.transient(self)
        command_list = Listbox(posting, fg='#800080', selectforeground='white', selectbackground='#800080',
                               font=('Microsoft YaHei UI', 11))
        command_list.bind('<Return>', lambda v=None: setit(command_list.get(command_list.curselection())))
        command_list.bind('<Double-Button-1>', lambda v=None: setit(command_list.get(command_list.curselection())))
        command_list.bind('<Right>', lambda v=None: setit(command_list.get(command_list.curselection())))
        command_list.bind('<Left>', lambda v=None: setit(command_list.get(command_list.curselection())))
        command_list.pack(fill='both', expand=1)
        for temp in self.paths:
            command_list.insert(END, f'{temp}')

    def _Configuration_labels(self, ww, ly, index_):
        index = str(self.text[self.note.index(self.note.select())].index(INSERT)).split(".")
        text = f'第{index[0]}行  第{index[1]}列'
        if len(text) >= 12:  # 1011,550
            self.label.place(x=ww - 331, y=ly)
        else:
            self.label.place(x=ww - 321, y=ly)
        self.label2.place(x=ww - 111, y=ly)
        self.label3.place(x=ww - 166, y=ly)
        self.label4.place(x=0, y=ly)
        self.label_theme.place(x=ww - 231, y=ly)
        self.label2['text'] = f'     共{len(self.text[index_].get(1.0, END))}个字符'
        self.label3['text'] = f'|    {self.encoding}    |'
        try:
            self.label4['text'] = self.paths[index_]
        except IndexError:
            self.label4['text'] = '无标题'

    def _Configuration_frames(self, ww, wh, ly, index_):
        self.files.place(width=150, height=wh - 44, y=22)
        try:
            # print(len(text))
            self.note.place(width=ww - 150, height=wh - 18)
            for i in self.text:
                # i.place(width=ww - 153, height=self.frame[0].winfo_height())
                i.pack(fill=BOTH, expand=YES)
            # try:
            #      self.label_theme['text'] = f'|    {self.theme_chinese[self.theme]}'
            # except KeyError:
            #      self.label_theme['text'] = f'|    {self.theme}'
            self.new_btn.place(x=ww - 71)
            self.cls_btn.place(x=ww - 36)
        except TclError:
            pass

    def Configuration(self):
        ww = self.winfo_width()
        wh = self.winfo_height()
        index_ = self.note.index(self.note.select())
        self.lb.pack(side=BOTTOM, fill=X)
        ly = self.lb.winfo_y()
        threading.Thread(target=lambda: self._Configuration_frames(ww, wh, ly, index_)).start()
        threading.Thread(target=lambda: self._Configuration_labels(ww, ly, index_)).start()

    def binds(self, i):
        def a():
            i.bind("<Control-Alt-p>", self.delete)
            i.bind("<Control-f>", lambda event: Find(
                i, self))
            i.bind("<Control-h>", lambda event: Replace(
                i, self))
            i.bind("<Button-3>", lambda event: self.cd3.post(event.x_root, event.y_root))
            i.bind("<F5>", self.run_module)
            i.bind("<F12>", self.open_web)
            i.bind("<Control-g>", lambda event: self.text[self.note.index(self.note.select())].see(
                f'{Querybox.get_string("请输入需要跳到的行数:", title="跳到行")}.0'))
            i.bind("<Control-p>", lambda event: sys.exit(0))
            i.bind("<Control-[>", self.adds)
            i.bind("<Control-Alt-u>", self.addn)

        def b():
            i.bind("<Button-1>", self.row_column)
            i.bind("<Control-b>", self.pyw)
            i.bind("<F1>", self.help31)
            i.bind("<Control-s>", self.save)
            i.bind("<Control-n>", self.new)
            i.bind("<Control-l>", self.len_of_text)
            i.bind("<Control-o>", self.choose)
            i.bind("<Control-w>", self.close)
            i.bind("<Control-/>", lambda event: self.add("#"))
            i.bind("<Control-]>", self.add_tabs)

        threading.Thread(target=a).start()
        threading.Thread(target=b).start()

    def no_thown(self, function, Error=TclError):
        try:
            function()
        except Error:
            pass

    def close(self, event=None):
        index = self.note.index(self.note.select())
        self.note.forget(self.note.select())
        try:
            self.frame[index].destroy()
            del self.frame[index]
            del self.text[index]
            del self.name[index]
            del self.paths[index]
        except TclError:
            pass
        if len(self.note.tabs()) <= 0:
            self.new()
        self.note.select(self.note.tabs()[0])
        try:
            self.text[index].place(width=1000, height=480)
        except TclError:
            self.text[-1].place(width=1000, height=480)
        self.label['text'] = f'第1行  第1列'
        self.label2['text'] = f'     未创建文件'
        self.label3['text'] = f'|    {self.encoding}    |'
        self.label4['text'] = ''
        self.Configuration()
        self.update_file()

    def up(self, index):
        try:
            self.note.select(self.note.tabs()[index])
        except (TclError, IndexError):
            pass

    def set_menu(self):
        cd = Menu(self, tearoff=False)
        cd8 = Menu(self, tearoff=False)
        cd9 = Menu(self, tearoff=False)
        cd20 = Menu(self, tearoff=False)
        cd7 = Menu(self, tearoff=False)
        cd1 = Menu(self, tearoff=False)
        cd5 = Menu(self, tearoff=False)
        cd10 = Menu(self, tearoff=False)
        cd2 = Menu(self, tearoff=False)
        cd12 = Menu(self, tearoff=False)
        cd14 = Menu(self, tearoff=False)
        cd15 = Menu(self, tearoff=False)
        cd16 = Menu(self, tearoff=False)
        cd17 = Menu(self, tearoff=False)
        cd18 = Menu(self, tearoff=False)
        cd19 = Menu(self, tearoff=False)
        cd16.add_command(label="转换成大写", command=lambda: self.big_small(low=False))
        cd16.add_command(label="转换成小写", command=self.big_small)
        cd16.add_command(label="首字母大写", command=lambda: self.big_small(low=''))
        cd16.add_command(label="反向处理", command=lambda: self.big_small(low=None))
        cd15.add_command(label="上一个文件        Tab",
                         command=lambda: self.up(self.note.index(self.note.select()) - 1))
        cd15.add_command(label="下一个文件        Shift+Tab",
                         command=lambda: self.up(self.note.index(self.note.select()) + 1))
        cd15.add_command(label="第一个文件        Home", command=lambda: self.up(0))
        cd15.add_command(label="最后一个文件    End", command=lambda: self.up(-1))
        self.cd3 = Menu(self, tearoff=False)
        cd8.add_command(label="用二进制打开", command=self.open_two)
        cd8.add_command(label="用GBK打开", command=lambda: self.opens("rt", "GBK"))
        cd8.add_command(
            label="用GB2312打开",
            command=lambda: self.opens(
                "rt",
                "GB2312"))
        cd8.add_command(
            label="用UTF-8打开",
            command=lambda: self.opens(
                "rt",
                "UTF-8"))
        cd20.add_command(label="打开cmd", command=lambda: subprocess.Popen("cmd"))
        cd20.add_command(label="打开终端", command=lambda: subprocess.Popen("powershell"))
        cd8.add_command(label="用ANSI打开", command=lambda: self.opens("rt", "ANSI"))
        cd.add_command(label="新建文件(N)    Ctrl+N", command=self.new)
        # cd.add_command(label="新建窗口", command=lambda: MainWindow())
        cd.add_command(label="新建窗口", command=lambda: subprocess.Popen("main"))
        cd.add_command(label="保存(S)             Ctrl+S", command=self.save)
        cd.add_command(label="另存为", command=self.save_as)
        cd.add_command(label="全部保存", command=self.save_all)
        cd.add_command(label="复制文件", command=self.copy_file)
        cd.add_separator()
        cd.add_command(label="文本长度(L)     Ctrl+L", command=self.len_of_text)
        cd.add_command(label="英文文本词数", command=self.len_of_english_text)
        cd.add_command(label="词频统计", command=lambda:threading.Thread(target=self.lcut).start())
        cd.add_command(label="文件信息",
                       command=lambda: self.show_file(self.paths[self.note.index(self.note.select())], len(
                           self.text[self.note.index(self.note.select())].get("1.0", END)),
                                                      self.text[
                                                          self.note.index(self.note.select())].get(
                                                          "1.0", END)))
        cd.add_command(label="文件列表", command=self.post_input_list)
        cd.add_separator()
        cd.add_command(label="打开(O)            Ctrl+O", command=self.choose)
        cd.add_command(label="重新打开", command=self.chooses)
        cd.add_cascade(label="用...打开", menu=cd8)

        cd18.add_command(
            label="打开文件路径",
            command=lambda: subprocess.Popen(
                "explorer {}".format(
                    (self.paths[self.note.index(self.note.select())].replace("/", "\\")).replace(
                        "\\{}".format(os.path.basename(self.paths[self.note.index(self.note.select())])), ""))))
        cd18.add_command(label="复制文件名", command=lambda: pyperclip.copy(
            os.path.basename(self.paths[self.note.index(self.note.select())])))
        cd18.add_command(label="复制文件路径", command=lambda: pyperclip.copy(
            os.path.dirname(self.paths[self.note.index(self.note.select())])))
        cd18.add_command(label="复制文件名与路径",
                         command=lambda: pyperclip.copy(self.paths[self.note.index(self.note.select())]))
        cd.add_cascade(label="文件...", menu=cd18)
        cd.add_cascade(label="打开...", menu=cd20)
        cd.add_command(label="关闭文件(W)    Ctrl+W", command=self.close)
        cd.add_separator()
        cd.add_command(label="退出                    Alt+F4", command=self.tk_quit)
        cd.add_command(label="直接退出(P)      Ctrl+P", command=sys.exit)
        for text, command, status, value in (("暗色主题", lambda: self.Styles(theme="darkly"), self.Status2, 1),
                                             ("亮色主题", lambda: self.Styles(theme="sandstone"), self.Status2, 2),
                                             ("紫色主题", lambda: self.Styles(theme="vapor"), self.Status2, 3),
                                             ("蓝色主题", lambda: self.Styles(theme="solar"), self.Status2, 4),
                                             ("灰色主题", lambda: self.Styles(theme="superhero"), self.Status2, 5)):
            cd7.add_radiobutton(label=text, command=command, variable=status,
                                value=value)
        for text, value, command in (("cosmo", 6, lambda: self.Styles(theme="cosmo")),
                                     ("flatly", 7, lambda: self.Styles(theme="flatly")),
                                     ("litera", 8, lambda: self.Styles(theme="litera")),
                                     ("minty", 9, lambda: self.Styles(theme="minty")),
                                     ("lumen", 10, lambda: self.Styles(theme="lumen")),
                                     ("sandstone", 11, lambda: self.Styles(theme="sandstone")),
                                     ("yeti", 12, lambda: self.Styles(theme="yeti")),
                                     ("pulse", 13, lambda: self.Styles(theme="pulse")),
                                     ("united", 14, lambda: self.Styles(theme="united")),
                                     ("morph", 15, lambda: self.Styles(theme="morph")),
                                     ("journal", 16, lambda: self.Styles(theme="journal")),
                                     ("darkly", 17, lambda: self.Styles(theme="darkly")),
                                     ("superhero", 18, lambda: self.Styles(theme="superhero")),
                                     ("solar", 19, lambda: self.Styles(theme="solar")),
                                     ("cyborg", 20, lambda: self.Styles(theme="cyborg")),
                                     ("vapor", 21, lambda: self.Styles(theme="vapor")),
                                     ("simplex", 22, lambda: self.Styles(theme="simplex")),
                                     ("cerculean", 23, lambda: self.Styles(theme="cerculean"))):
            cd17.add_radiobutton(label=text, variable=self.Status2, value=value,
                                 command=command)
        cd7.add_cascade(label="更多主题", menu=cd17)
        cd14.add_command(label="字体", command=self.set_font)
        self.Status.set(True)
        self.Status2.set(2)
        self.Status3.set(True)
        cd19.add_command(label="增大", command=self.config_font)
        cd19.add_command(label="减小", command=lambda: self.config_font('-'))
        cd19.add_command(label="恢复", command=self.recover_font)
        cd14.add_checkbutton(label="自动换行", variable=self.Status, command=self.enters)
        cd14.add_checkbutton(label="显示行列", variable=self.Status3, command=self.rows)
        cd14.add_checkbutton(label="代码模式", variable=self.is_coding)
        cd14.add_cascade(label="缩放", menu=cd19)
        cd14.add_separator()
        # cd5.add_command(label="导入字体", command=newfont)
        cd5.add_command(label="服务", command=lambda: subprocess.Popen('service'))
        cd14.add_cascade(label="主题颜色", menu=cd7)
        self.is_highlighter.set(False)
        cd14.add_command(label="背景色", command=lambda: threading.Thread(target=self.color).start())
        cd14.add_command(label="前景色", command=lambda: threading.Thread(target=self.colors).start())
        cd14.add_command(label="边框色", command=lambda: threading.Thread(target=self.textcolor).start())
        cd14.add_command(label="行数色", command=lambda: threading.Thread(target=self.linecolor).start())
        cd14.add_command(label="透明度",
                         command=lambda: self.attributes("-alpha", (100 - self.get_scale()) / 100))
        cd14.add_separator()
        cd14.add_cascade(menu=cd15, label="切换文件")
        cd14.add_separator()
        cd14.add_command(label="跳到行      Ctrl+G", command=lambda: self.text[self.note.index(self.note.select())].see(
            f'{Querybox.get_string("请输入需要跳到的行数:", title="跳到行")}.0'))
        cd14.add_command(label="跳到开头  Home",
                         command=lambda: self.text[self.note.index(self.note.select())].see(1.0))
        cd14.add_command(label="跳到最后  End", command=lambda: self.text[self.note.index(self.note.select())].see(END))
        # command=lambda: self.attributes("-alpha", (1 - Querybox.get_float("透明度,0-100", "透明") / 100)))
        cd2.add_cascade(label="设置", menu=cd5)
        cd2.add_separator()
        cd2.add_command(label="帮助    F1", command=self.help31)
        # cd2.add_command(label="文档",command=file)
        cd2.add_command(label="关于...", command=about)
        cd2.add_command(label="更新日志", command=show_log)
        cd2.add_separator()
        cd2.add_command(label="GUI", command=lambda: self.show_info("tkinter — Python interface to Tcl/Tk\n\n\
Source code: Lib/tkinter/__init__.py\n\n\
The tkinter package (“Tk interface”) is the standard Python interface to the Tcl/Tk GUI toolkit.\
Both Tk and tkinter are available on most Unix platforms, including macOS, as well as on Windows systems.\n\n\
Tkinter supports a range of Tcl/Tk versions, built either with or without thread support.\
The official Python binary release bundles Tcl/Tk 8.6 threaded.\
See the source code for the _tkinter module for more information about supported versions.\n\n\
ttkbootstrap\n\
A supercharged theme extension for tkinter that enables on-demand modern flat style themes inspired by Bootstrap.\n\
📦 Features\n\
✔️ Built-in Themes\n\
Over a dozen curated dark and light themes\n\
✔️ Pre-defined self.self.Styles:\n\
Loads of beautiful pre-defined widget self.self.Styles such as outline and round toggle buttons.\n\
✔️ Simple keyword API:\n\
Apply colors and types using simple keywords such as primary and striped instead of the legacy approach of primary.\
Striped.Horizontal.TProgressbar. If you\"ve used Bootstrap for web development, you are already familiar with this\
 approach using css classes.\n\
✔️ Lots of new Widgets:\n\
ttkbootstrap comes with several new beautifully designed widgets such as Meter, DateEntry, and Floodgauge. \
Additionally, dialogs are now themed and fully customizable.\n\
✔️ Built-in Theme Creator:\n\
Want to create your own theme? Easy! ttkbootstrap includes a built-in theme creator that enables you to easily build, \
load, expore, and apply your own custom themes.\n\
Breaking changes in 1.0\n\
Version 1.0 is a complete rebuild of the library. If you are using version 0.5 you may run into issues trying to import\
themes with the themes.json as this has been removed from 1.0. You can now import and save themes directly using the \
ttkcreator.", "关于-tkinter"))
        cd12.add_command(label="运行python F5", command=self.run_module)
        cd12.add_command(label="运行pyw Ctrl+B", command=self.pyw)
        cd12.add_command(
            label="python shell",
            command=lambda: subprocess.Popen("shell"))
        cd12.add_command(
            label="运行C语言",
            command=lambda: self.gcc("gcc.exe", self.paths[self.note.index(self.note.select())]))
        cd12.add_command(
            label="运行C++",
            command=lambda: self.gcc("g++.exe", self.paths[self.note.index(self.note.select())]))
        cd12.add_command(
            label="运行.vbs .js",
            command=lambda: self.run_modules(f"wscript {self.paths[self.note.index(self.note.select())]}"))
        cd12.add_command(label="运行.html", command=lambda: self.run_modules(
            f'"C:\\Program Files\\Internet Explorer\\iexplore.exe" {self.paths[self.note.index(self.note.select())]}'))
        cd9.add_cascade(label="运行", menu=cd12)
        cd9.add_cascade(label="计算", menu=cd10)
        cd10.add_command(label="计算日期之差", command=self.date)
        cd10.add_command(label="开方", command=self.sqrt)
        cd9.add_command(label="打开网页     F12", command=self.open_web)
        cd9.add_command(label="计算器", command=lambda: subprocess.Popen("runcalc"))
        cd9.add_command(label="终端", command=lambda: subprocess.Popen("powershell"))
        '''i.bind("<Control-]>", self.add_tabs)
        i.bind("<Control-[>", self.adds)'''
        self.cd3.add_cascade(label="大小写转换", menu=cd16)
        self.cd3.add_separator()
        for text, command in (("当前时间", self.time_insert),
                              ('web上搜索', self.search_web)):
            self.cd3.add_command(label=text, command=command)
        self.cd3.add_separator()
        for text, command in (("增加缩进         Ctrl+]", self.add_tabs),
                              ("减少缩进         Ctrl+[", self.adds)):
            self.cd3.add_command(label=text, command=command)
        self.cd3.add_separator()
        cd17 = Menu(self, tearoff=False)
        for text, command in (("增加行", self.addn),
                              ("删除行", self.delete),
                              ("行排序(升序)", self.sort),
                              ("行排序(降序)", lambda: self.sort(reverse=True)),
                              ("行逆序", self.reverse),
                              ("行打乱", self.shuffle),
                              ("行去重", self.deduplication)):
            cd17.add_command(label=text, command=command)
        self.cd3.add_cascade(label="行(L)", menu=cd17)
        self.cd3.add_separator()
        for text, command in (
                ("全部复制", lambda: pyperclip.copy(self.text[self.note.index(self.note.select())].get("1.0", END))),
                ("清空", lambda: self.text[self.note.index(self.note.select())].delete("1.0", END)),
                ("复制                 Ctrl+C", self.copy_get),
                ("剪切                 Ctrl+X", self.copy_cut),
                ("粘贴                 Ctrl+V", lambda: self.text[self.note.index(self.note.select())].insert(
                    eval(self.text[self.note.index(self.note.select())].index(INSERT)),
                    pyperclip.paste())),
                ("查找                 Ctrl+F",
                 lambda: Find(self.text[self.note.index(self.note.select())], self)),
                ("替换                 Ctrl+H",
                 lambda: Replace(self.text[self.note.index(self.note.select())], self)),
                ("撤销                 Ctrl+Z", self.undo),
                ("重做                 Ctrl+Y", self.redo),
                ("删除                 Del", self.deletes)):
            self.cd3.add_command(label=text, command=command)
        for text, menu in (("文件(F)", cd),
                           ("编辑(E)", self.cd3),
                           ("查看(V)", cd14),
                           ("应用(A)", cd9),
                           ("帮助(H)", cd2)):
            cd1.add_cascade(label=text, menu=menu)
        cd10.add_command(label="计算器", command=lambda: subprocess.Popen("runcalc"))
        self.config(menu=cd1)

    def set_label(self):
        if self.paths[0] != "":
            self.chooses()
        else:
            self.frame.append(Frame(self))
            self.text.append(
                TextEdit(self.frame[0], font=self.fontname, undo=True, borderwidth=1))
            self.text[-1].pack(fill=BOTH, expand=YES)
            self.text[-1].tag_configure("found", background="yellow")
            self.note.add(self.frame[0], text=self.name[0])
        self.note.place(width=1011, height=527, x=150)
        self.text[self.note.index(self.note.select())].place(width=1000, height=480)
        self.label['text'] = f'第1行  第1列'
        self.label2['text'] = f'     共{len(self.text[self.note.index(self.note.select())].get(1.0, END))}个字符'
        self.label3['text'] = f'|    {self.encoding}    |'
        self.label4['text'] = self.paths[self.note.index(self.note.select())]
        self.label_theme['text'] = f'|    {self.theme_chinese[self.theme]}'
        self.configure(bg="white")
        Style(theme="sandstone")
        # self.iconbitmap("C:/Windows/notepad.exe")
        # noinspection PyArgumentList
        self.text[self.note.index(self.note.select())].tag_configure("found", background="yellow")
        self.text[self.note.index(self.note.select())].tag_configure("web", foreground="blue")

        # self.Statusbar = Label(self, text="第1行,第1列", relief=SUNKEN, anchor=W)
        # self.Statusbar.pack(side=BOTTOM, fill=X)
        def bind():
            for i in self.text:
                self.binds(i)

        threading.Thread(target=bind).start()
        self.bind("<Configure>", lambda event: threading.Thread(target=self.Configuration).start())
        self.bind("<Double-Button-2>", self.large)
        # self.note.bind("<Configure>", self.Configuration)

    def set_file(self):
        self.files = ScrolledFrame(self)
        self.files.place(width=150, height=self.winfo_height() - 44, y=22)
        Label(self, text="打开的文件", font=("Microsoft YaHei UI", 10, "bold")).place(x=1, y=2)

    def update_file(self):
        for widget in self.files.winfo_children():
            widget.destroy()
        # commands = [lambda: self.note.select(self.frame[i]) for i in range(len(self.paths)) if print(i) is None]
        commands = [self.note.tabs()[i] for i in range(len(self.paths))]
        row = [i for i in range(len(self.paths))]
        for i in range(len(self.paths)):
            try:
                # Label(self.files, text=os.path.basename(self.paths[i])).pack(anchor=W)#place(x=3, y=(i + 1) * 25)
                Button(self.files, text=os.path.basename(self.paths[i]),
                       command=lambda f=commands[i]: self.note.select(f), bootstyle='link').grid(row=row[i], sticky=W,
                                                                                                 column=1, padx=0)
            except IndexError:
                pass

    def show(self):
        windnd.hook_dropfiles(self, func=self.dragged_files)
        self.protocol('WM_DELETE_WINDOW', self.tk_quit)
        self.note = Notebook(self)
        self.frame = []
        self.note.enable_traversal()
        self.lb = Label(self)
        self.lb.place(x=0, y=self.winfo_height() - 39)
        self.label = Label(self, font=Font(family='Microsoft YaHei UI', size=8))
        # self.label.place(x=750, y=self.winfo_height() - 39)
        self.label2 = Label(self, font=Font(family='Microsoft YaHei UI', size=8))
        # self.label2.place(x=900, y=self.winfo_height() - 39)
        self.label3 = Label(self, font=Font(family='Microsoft YaHei UI', size=8))
        # self.label3.place(x=845, y=self.winfo_height() - 39)
        self.label4 = Label(self, font=Font(family='Microsoft YaHei UI', size=8))
        # self.label4.place(x=0, y=self.winfo_height() - 39)
        # self.label4.pack(anchor=SW,side=BOTTOM)
        self.label_theme = Label(self, font=Font(family='Microsoft YaHei UI', size=8))
        # self.label_theme.place(x=800, y=self.winfo_height() - 39)
        self.new_btn = Button(self.note, command=self.new, text='+', bootstyle='outline-secondary')
        # self.new_btn.pack(side=RIGHT)
        # self.new_btn.place(x=940, y=0)
        self.cls_btn = Button(self.note, command=self.close, text='x', bootstyle='outline-secondary')
        # self.cls_btn.pack(side=RIGHT)
        # self.cls_btn.place(x=975, y=0)
        self.text = []
        self.set_file()
        self.set_label()
        self.set_menu()
        self.Configuration()
        cd_note = Menu(self, tearoff=True)
        cd_note.add_command(label="文件信息",
                            command=self.file_info)
        cd_note.add_command(label="关闭文件", command=self.close)
        '''
        cd15.add_command(label="上一个文件", command=lambda: self.up(self.note.index(self.note.select()) - 1))
        cd15.add_command(label="下一个文件", command=lambda: self.up(self.note.index(self.note.select()) + 1))
        cd15.add_command(label="第一个文件", command=lambda: self.up(0))
        cd15.add_command(label="最后一个文件", command=lambda: self.up(-1))'''
        self.note.bind("<Tab>", lambda event: self.up(self.note.index(self.note.select()) + 1))
        self.note.bind("<Shift-Tab>", lambda event: self.up(self.note.index(self.note.select()) - 1))
        self.files.bind("<Tab>", lambda event: self.up(self.note.index(self.note.select()) + 1))
        self.files.bind("<Shift-Tab>", lambda event: self.up(self.note.index(self.note.select()) - 1))
        self.note.bind("<Button-3>", lambda event: cd_note.post(event.x_root, event.y_root))
        self.note.bind("<Home>", lambda event: self.up(0))
        self.note.bind("<End>", lambda event: self.up(-1))
        self.files.bind("<Home>", lambda event: self.up(0))
        self.files.bind("<End>", lambda event: self.up(-1))
        # self.note.bind("<Button-1>",
        #                     lambda event: self.title("python记事本 - " + self.name[self.note.index(self.note.select())]))
        # self.note.bind("<Button-2>",
        #                     lambda event: self.title("python记事本 - " + self.name[self.note.index(self.note.select())]))
        # self.note.bind("<Key>",
        #                     lambda event: self.title("python记事本 - " + self.name[self.note.index(self.note.select())]))
        # self.text[self.note.index(self.note.select())].tag_bind("web","<F4>",webbrowser.open)
        self.is_see_rows = True
        self.two_open_or_not = False
        self.larges = False
        self.mainloop()


if __name__ == '__main__':
    window = MainWindow()
