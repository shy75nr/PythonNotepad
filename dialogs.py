from need.ttkbootstrap import *
from need.ttkbootstrap.scrolled import ScrolledFrame
from need.ttkbootstrap.dialogs import Messagebox
import pyperclip
from tkinter.font import Font
import os
import sys


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


class EncodingDialog(Toplevel):
    def __init__(self):
        super().__init__()
        self.geometry("230x300")
        self.resizable(False, False)
        self.title("选择编码")
        self.result = 'gbk'
        Label(self, text='选择编码').pack(anchor=W, side=TOP)
        self.frm = ScrolledFrame(self)
        self.frm.pack(fill=BOTH, expand=YES)
        # coding = ['ASCII', 'ANSI', 'CESU-8', 'GB18030', 'GB2312', 'GBK', 'ISO-8859-1', 'ISO-8859-13', 'ISO-8859-15',
        #           'ISO-8859-16', 'Latin-1', 'Unicode', 'US-ASCII', 'UTF-8', 'UTF-8BE',
        #           'UTF-8LE', 'UTF-16', 'UTF-16BE', 'UTF-16LE', 'UTF-32', 'UTF-32BE', 'UTF-32LE']
        coding = ['ascii', 'big5', 'big5hkscs', 'charmap', 'cp037', 'cp1006', 'cp1026', 'cp1125', 'cp1140', 'cp1250',
                  'cp1251', 'cp1252', 'cp1253', 'cp1254', 'cp1255', 'cp1256', 'cp1257', 'cp1258', 'cp273', 'cp424',
                  'cp437', 'cp500', 'cp720', 'cp737', 'cp775', 'cp850', 'cp852', 'cp855', 'cp856', 'cp857', 'cp858',
                  'cp860', 'cp861', 'cp862', 'cp863', 'cp864', 'cp865', 'cp866', 'cp869', 'cp874', 'cp875', 'cp932',
                  'cp949', 'cp950', 'euc_jis_2004', 'euc_jisx0213', 'euc_jp', 'euc_kr', 'gb18030', 'gb2312', 'gbk',
                  'hp_roman8', 'hz', 'idna', 'iso2022_jp', 'iso2022_jp_1', 'iso2022_jp_2', 'iso2022_jp_2004',
                  'iso2022_jp_3', 'iso2022_jp_ext', 'iso2022_kr', 'iso8859_1', 'iso8859_10', 'iso8859_11', 'iso8859_13',
                  'iso8859_14', 'iso8859_15', 'iso8859_16', 'iso8859_2', 'iso8859_3', 'iso8859_4', 'iso8859_5',
                  'iso8859_6', 'iso8859_7', 'iso8859_8', 'iso8859_9', 'johab', 'koi8_r', 'koi8_t', 'koi8_u', 'kz1048',
                  'latin_1', 'mac_arabic', 'mac_croatian', 'mac_cyrillic', 'mac_farsi', 'mac_greek', 'mac_iceland',
                  'mac_latin2', 'mac_roman', 'mac_romanian', 'mac_turkish', 'mbcs', 'oem', 'palmos', 'ptcp154',
                  'punycode', 'raw_unicode_escape', 'shift_jis', 'shift_jis_2004', 'shift_jisx0213', 'tis_620',
                  'unicode_escape', 'utf_16', 'utf_16_be', 'utf_16_le', 'utf_32', 'utf_32_be', 'utf_32_le', 'utf_7',
                  'utf_8', 'utf_8_sig']
        self.sv = StringVar()
        for i in range(len(coding)):
            Radiobutton(self.frm, variable=self.sv, value=coding[i], text=coding[i], bootstyle=SECONDARY).pack(side=TOP,
                                                                                                               anchor=W)
        self.sv.set('gbk')
        Button(self, text="确定", command=self.ok).pack(anchor=E, side=TOP)
        self.wait_window()

    def ok(self):
        self.result = self.sv.get()
        self.destroy()


def askencoding():
    window = EncodingDialog()
    return window.result


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
    Button(tk, text=1, command=lambda: jia(1)).place(width=60, height=60, relx=0, rely=0.17)
    Button(tk, text=2, command=lambda: jia(2)).place(width=60, height=60, relx=0.16, rely=0.17)
    Button(tk, text=3, command=lambda: jia(3)).place(width=60, height=60, relx=0.32, rely=0.17)
    Button(tk, text='+', command=lambda: jia('+'), bootstyle='secondary').place(width=60, height=60, relx=0.48,
                                                                                rely=0.17)
    Button(tk, text='-', command=lambda: jia('-'), bootstyle='secondary').place(width=60, height=60, relx=0.48,
                                                                                rely=0.29)
    Button(tk, text='×', command=lambda: jia('x'), bootstyle='secondary').place(width=60, height=60, relx=0.48,
                                                                                rely=0.41)
    Button(tk, text='÷', command=lambda: jia('÷'), bootstyle='secondary').place(width=60, height=60, relx=0.48,
                                                                                rely=0.53)
    Button(tk, text='√(', command=lambda: jia('math.sqrt('), bootstyle='secondary').place(width=60, height=60,
                                                                                          relx=0.64, rely=0.17)
    Button(tk, text='sin', command=lambda: jia('math.sin('), bootstyle='secondary').place(width=60, height=60, relx=0.8,
                                                                                          rely=0.29)
    Button(tk, text='tan', command=lambda: jia('math.tan('), bootstyle='secondary').place(width=60, height=60, relx=0.8,
                                                                                          rely=0.41)
    Button(tk, text='cos', command=lambda: jia('math.cos('), bootstyle='secondary').place(width=60, height=60, relx=0.8,
                                                                                          rely=0.53)
    Button(tk, text='清除', command=clean, bootstyle='secondary').place(width=60, height=60, relx=0.80, rely=0.17)
    Button(tk, text='^2', command=lambda: jia('^2'), bootstyle='secondary').place(width=60, height=60, relx=0.64,
                                                                                  rely=0.29)
    Button(tk, text='^', command=lambda: jia('^'), bootstyle='secondary').place(width=60, height=60, relx=0.64,
                                                                                rely=0.41)
    Button(tk, text='=', command=run, bootstyle='	success').place(width=60, height=60, relx=0.64, rely=0.53)
    Button(tk, text=4, command=lambda: jia(4)).place(width=60, height=60, relx=0, rely=0.29)
    Button(tk, text=5, command=lambda: jia(5)).place(width=60, height=60, relx=0.16, rely=0.29)
    Button(tk, text=6, command=lambda: jia(6)).place(width=60, height=60, relx=0.32, rely=0.29)
    Button(tk, text=7, command=lambda: jia(7)).place(width=60, height=60, relx=0, rely=0.41)
    Button(tk, text=8, command=lambda: jia(8)).place(width=60, height=60, relx=0.16, rely=0.41)
    Button(tk, text=9, command=lambda: jia(9)).place(width=60, height=60, relx=0.32, rely=0.41)
    Button(tk, text='(', bootstyle='secondary', command=lambda: jia('(')).place(width=60, height=60, relx=0, rely=0.53)
    Button(tk, text=0, command=lambda: jia(0)).place(width=60, height=60, relx=0.16, rely=0.53)
    Button(tk, text=')', bootstyle='secondary', command=lambda: jia(')')).place(width=60, height=60, relx=0.32,
                                                                                rely=0.53)
    Button(tk, text='DEL', bootstyle='secondary', command=delete).place(width=60, height=60, relx=0, rely=0.65)
    Button(tk, text='%', bootstyle='secondary', command=lambda: jia('%')).place(width=60, height=60, relx=0.16,
                                                                                rely=0.65)
    Button(tk, text='mod', bootstyle='secondary', command=lambda: jia('mod')).place(width=60, height=60, relx=0.32,
                                                                                    rely=0.65)
    Button(tk, text='.', bootstyle='secondary', command=lambda: jia('.')).place(width=60, height=60, relx=0.48,
                                                                                rely=0.65)
    Button(tk, text='1/x', bootstyle='secondary', command=jiax).place(width=60, height=60, relx=0.64, rely=0.65)
    Button(tk, text='八进制', bootstyle='secondary', command=lambda: jinzhi(8)).place(width=60, height=60, relx=0,
                                                                                      rely=0.77)
    Button(tk, text='十进制', bootstyle='secondary', command=lambda: jinzhi(10)).place(width=60, height=60, relx=0.16,
                                                                                       rely=0.77)
    Button(tk, text='十六进制', bootstyle='secondary', command=lambda: jinzhi(16)).place(width=60, height=60, relx=0.32,
                                                                                         rely=0.77)
    Button(tk, text='m+', bootstyle='secondary', command=mplus).place(width=60, height=60, relx=0.48, rely=0.77)
    Button(tk, text='m-', bootstyle='secondary', command=muplus).place(width=60, height=60, relx=0.64, rely=0.77)
    Button(tk, text='mr', bootstyle='secondary', command=lambda: en1.insert(END, mr)).place(width=60, height=60,
                                                                                            relx=0.80, rely=0.77)
    Button(tk, text='mc', bootstyle='secondary', command=mc).place(width=60, height=60, relx=0.8, rely=0.65)
    Button(tk, text='计算日\n期之差', bootstyle='secondary', command=date).place(width=60, height=60, relx=0, rely=0.89)
    Button(tk, text='sinh', bootstyle='secondary', command=lambda: jia('math.sinh(')).place(width=60, height=60,
                                                                                            relx=0.16, rely=0.89)
    Button(tk, text='cosh', bootstyle='secondary', command=lambda: jia('math.cosh(')).place(width=60, height=60,
                                                                                            relx=0.32, rely=0.89)
    Button(tk, text='tanh', bootstyle='secondary', command=lambda: jia('math.tanh')).place(width=60, height=60,
                                                                                           relx=0.48, rely=0.89)
    Button(tk, text='10^', bootstyle='secondary', command=lambda: jia('10^')).place(width=60, height=60, relx=0.64,
                                                                                    rely=0.89)
    Button(tk, text='π', bootstyle='secondary', command=lambda: jia('π')).place(width=60, height=60, relx=0.8,
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
