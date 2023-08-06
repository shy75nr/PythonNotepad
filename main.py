# -*- coding: UTF-8 -*-
import datetime
import getpass
import random
import subprocess
import traceback
import webbrowser
from tkinter import EventType, TclError
from tkinter.colorchooser import askcolor
from tkinter.filedialog import asksaveasfilename, askopenfilename, askopenfilenames, askdirectory
from typing import List

import chardet
import jieba
import windnd
from need.ttkbootstrap.scrolled import ScrolledText

from idlelib import zoomheight
from dialogs import *
from widgets import *

ICONDIR = "icon"


def wheel_event(event, widget=None):
    """Handle scrollwheel event.

    For wheel up, event.delta = 120*n on Windows, -1*n on darwin,
    where n can be > 1 if one scrolls fast.  Flicking the wheel
    generates up to maybe 20 events with n up to 10 or more 1.
    Macs use wheel down (delta = 1*n) to scroll up, so positive
    delta means to scroll up on both systems.

    X-11 sends Control-Button-4,5 events instead.

    The widget parameter is needed so browser label bindings can pass
    the underlying canvas.

    This function depends on widget.yview to not be overridden by
    a subclass.
    """
    up = {EventType.MouseWheel: event.delta > 0,
          EventType.ButtonPress: event.num == 4}
    lines = -5 if up[event.type] else 5
    widget = event.widget if widget is None else widget
    widget.yview(SCROLL, lines, 'units')
    return 'break'


class TreeNode:

    def __init__(self, canvas, parent, item, parents):
        self.canvas = canvas
        self.parent = parent
        self.parents = parents
        self.item = item
        self.state = 'collapsed'
        self.selected = False
        self.children = []
        self.x = self.y = None
        self.iconimages = {}  # cache of PhotoImage instances for icons

    def destroy(self):
        for c in self.children[:]:
            self.children.remove(c)
            c.destroy()
        self.parent = None

    def geticonimage(self, name):
        try:
            return self.iconimages[name]
        except KeyError:
            pass
        file, ext = os.path.splitext(name)
        ext = ext or ".gif"
        fullname = os.path.join(ICONDIR, file + ext)
        image = PhotoImage(master=self.canvas, file=fullname)
        self.iconimages[name] = image
        return image

    def select(self, event=None):
        if self.selected:
            return
        self.deselectall()
        self.selected = True
        self.canvas.delete(self.image_id)
        self.drawicon()
        self.drawtext()

    def deselect(self, event=None):
        if not self.selected:
            return
        self.selected = False
        self.canvas.delete(self.image_id)
        self.drawicon()
        self.drawtext()

    def deselectall(self):
        if self.parent:
            self.parent.deselectall()
        else:
            self.deselecttree()

    def deselecttree(self):
        if self.selected:
            self.deselect()
        for child in self.children:
            child.deselecttree()

    def flip(self, event=None):
        if os.path.isfile(self.item.path):
            self.parents.paths.append(self.item.path)
            encoding = self.parents.encoding
            try:
                self.parents.choose_encodings('gbk')
                self.parents.encoding = 'GBK'
            except UnicodeError:
                try:
                    self.parents.choose_encodings('gb2312')
                    self.parents.encoding = 'GB2312'
                except UnicodeError:
                    try:
                        self.parents.choose_encodings('utf-8')
                        self.parents.encoding = 'UTF-8'
                    except UnicodeError:
                        try:
                            self.parents.choose_encodings('ANSI')
                            self.parents.encoding = 'ANSI'
                        except UnicodeError:
                            try:
                                self.parents.encoding = '二进制'
                                self.parents.name.append(os.path.basename(self.parents.paths[-1]))
                                self.parents.frame.append(Frame(self.parents))
                                if os.path.basename(self.parents.paths[-1]).split('.')[-1].lower() in (
                                        'jpg', 'jpeg', 'png', 'gif', 'bmp', 'ico'):
                                    self.parents.text.append(
                                        PhotoEdit(self.parents.frame[-1], self.parents.paths[-1]))
                                elif os.path.basename(self.parents.paths[-1]).split('.')[-1].lower() in ('mp3', 'ogg'):
                                    self.parents.text.append(
                                        MediaPlayer(self.parents.frame[-1], self.parents.paths[-1])
                                    )
                                else:
                                    while True:
                                        if Messagebox.okcancel("文件被以错误的编码加载,\n是否以二进制读写?",
                                                               "编码错误") == "确定":
                                            self.parents.text.append(
                                                TextEdit(self.parents.frame[-1], font=self.parents.fontname, undo=True,
                                                         borderwidth=1))
                                            self.parents.text[-1].delete("1.0", END)
                                            with open(self.parents.paths[-1], 'rb') as fo:
                                                self.parents.text[-1].insert(END, hex(int.from_bytes(fo.read())))
                                            break
                                        else:
                                            try:
                                                self.parents.choose_encodings(askencoding())
                                                self.parents.saves(
                                                    self.parents.paths[
                                                        self.parents.note.index(self.parents.note.select())])
                                            except UnicodeError:
                                                pass
                                            else:
                                                break
                                            finally:
                                                pass
                                self.parents.text[-1].pack(fill=BOTH, expand=YES)
                                self.parents.text[-1].tag_configure("found", background="yellow")
                                self.parents.note.add(self.parents.frame[-1], text=self.parents.name[-1])
                                self.parents.note.select((self.parents.frame[-1]))
                                self.parents.binds(self.parents.text[-1])
                            except UnicodeError:
                                Messagebox.show_error("打开失败", "Error")
                                print(
                                    f"打开文件{self.parents.paths[self.parents.note.index(self.parents.note.select())]}失败")
                                self.parents.encoding = encoding
                            except TclError:
                                os.remove(f"C:/Users/{getpass.getuser()}/AppData/Local/Temp/python_notepad.tmp")
                                self.parents.show()
            self.parents.saves(self.item.path)
        print(self.parents.paths)
        if self.state == 'expanded':
            self.collapse()
        else:
            self.expand()
        self.item.OnDoubleClick()
        return "break"

    def expand(self, event=None):
        if not self.item._IsExpandable():
            return
        if self.state != 'expanded':
            self.state = 'expanded'
            self.update()
            self.view()

    def collapse(self, event=None):
        if self.state != 'collapsed':
            self.state = 'collapsed'
            self.update()

    def view(self):
        top = self.y - 2
        bottom = self.lastvisiblechild().y + 17
        height = bottom - top
        visible_top = self.canvas.canvasy(0)
        visible_height = self.canvas.winfo_height()
        visible_bottom = self.canvas.canvasy(visible_height)
        if visible_top <= top and bottom <= visible_bottom:
            return
        x0, y0, x1, y1 = self.canvas._getints(self.canvas['scrollregion'])
        if top >= visible_top and height <= visible_height:
            fraction = top + height - visible_height
        else:
            fraction = top
        fraction = float(fraction) / y1
        self.canvas.yview_moveto(fraction)

    def lastvisiblechild(self):
        if self.children and self.state == 'expanded':
            return self.children[-1].lastvisiblechild()
        else:
            return self

    def update(self):
        if self.parent:
            self.parent.update()
        else:
            oldcursor = self.canvas['cursor']
            self.canvas['cursor'] = "watch"
            self.canvas.update()
            self.canvas.delete(ALL)  # XXX could be more subtle
            self.draw(7, 2)
            x0, y0, x1, y1 = self.canvas.bbox(ALL)
            self.canvas.configure(scrollregion=(0, 0, x1, y1))
            self.canvas['cursor'] = oldcursor

    def draw(self, x, y):
        # XXX This hard-codes too many geometry constants!
        dy = 20
        self.x, self.y = x, y
        self.drawicon()
        self.drawtext()
        if self.state != 'expanded':
            return y + dy
        # draw children
        if not self.children:
            sublist = self.item._GetSubList()
            if not sublist:
                # _IsExpandable() was mistaken; that's allowed
                return y + 17
            for item in sublist:
                child = self.__class__(self.canvas, self, item, self.parents)
                self.children.append(child)
        cx = x + 20
        cy = y + dy
        cylast = 0
        for child in self.children:
            cylast = cy
            self.canvas.create_line(x + 9, cy + 7, cx, cy + 7, fill="gray50")
            cy = child.draw(cx, cy)
            if child.item._IsExpandable():
                if child.state == 'expanded':
                    iconname = "minusnode"
                    callback = child.collapse
                else:
                    iconname = "plusnode"
                    callback = child.expand
                image = self.geticonimage(iconname)
                id = self.canvas.create_image(x + 9, cylast + 7, image=image)
                # XXX This leaks bindings until canvas is deleted:
                self.canvas.tag_bind(id, "<1>", callback)
                self.canvas.tag_bind(id, "<Double-1>", lambda x: None)
        id = self.canvas.create_line(x + 9, y + 10, x + 9, cylast + 7,
                                     ##stipple="gray50",     # XXX Seems broken in Tk 8.0.x
                                     fill="gray50")
        self.canvas.tag_lower(id)  # XXX .lower(id) before Python 1.5.2
        return cy

    def drawicon(self):
        if self.selected:
            imagename = (self.item.GetSelectedIconName() or
                         self.item.GetIconName() or
                         "openfolder")
        else:
            imagename = self.item.GetIconName() or "folder"
        image = self.geticonimage(imagename)
        id = self.canvas.create_image(self.x, self.y, anchor="nw", image=image)
        self.image_id = id
        self.canvas.tag_bind(id, "<1>", self.select)
        self.canvas.tag_bind(id, "<Double-1>", self.flip)

    def drawtext(self):
        textx = self.x + 20 - 1
        texty = self.y - 4
        labeltext = self.item.GetLabelText()
        if labeltext:
            id = self.canvas.create_text(textx, texty, anchor="nw",
                                         text=labeltext)
            self.canvas.tag_bind(id, "<1>", self.select)
            self.canvas.tag_bind(id, "<Double-1>", self.flip)
            x0, y0, x1, y1 = self.canvas.bbox(id)
            textx = max(x1, 200) + 10
        text = self.item.GetText() or "<no text>"
        try:
            self.entry
        except AttributeError:
            pass
        else:
            self.edit_finish()
        try:
            self.label
        except AttributeError:
            # padding carefully selected (on Windows) to match Entry widget:
            self.label = Label(self.canvas, text=text)
        theme = idleConf.CurrentTheme()
        if self.selected:
            self.label.configure(idleConf.GetHighlight(theme, 'hilite'))
        else:
            self.label.configure(idleConf.GetHighlight(theme, 'normal'))
        id = self.canvas.create_window(textx, texty,
                                       anchor="nw", window=self.label)
        self.label.bind("<1>", self.select_or_edit)
        self.label.bind("<Double-1>", self.flip)
        self.label.bind("<MouseWheel>", lambda e: wheel_event(e, self.canvas))
        self.label.bind("<Button-4>", lambda e: wheel_event(e, self.canvas))
        self.label.bind("<Button-5>", lambda e: wheel_event(e, self.canvas))
        self.text_id = id

    def select_or_edit(self, event=None):
        # if self.selected and self.item.IsEditable():
        #     self.edit(event)
        # else:
        #     self.select(event)
        self.select(event)

    def edit(self, event=None):
        self.entry = Entry(self.label, width=0)
        self.entry.insert(0, self.label['text'])
        self.entry.selection_range(0, END)
        self.entry.pack(ipadx=5)
        self.entry.focus_set()
        self.entry.bind("<Return>", self.edit_finish)
        self.entry.bind("<Escape>", self.edit_cancel)

    def edit_finish(self, event=None):
        try:
            entry = self.entry
            del self.entry
        except AttributeError:
            return
        text = entry.get()
        entry.destroy()
        if text and text != self.item.GetText():
            self.item.SetText(text)
        text = self.item.GetText()
        self.label['text'] = text
        self.drawtext()
        self.canvas.focus_set()

    def edit_cancel(self, event=None):
        try:
            entry = self.entry
            del self.entry
        except AttributeError:
            return
        entry.destroy()
        self.drawtext()
        self.canvas.focus_set()


class TreeItem:
    """Abstract class representing tree items.

    Methods should typically be overridden, otherwise a default action
    is used.

    """

    def __init__(self):
        """Constructor.  Do whatever you need to do."""

    def GetText(self):
        """Return text string to display."""

    def GetLabelText(self):
        """Return label text string to display in front of text (if any)."""

    expandable = None

    def _IsExpandable(self):
        """Do not override!  Called by TreeNode."""
        if self.expandable is None:
            self.expandable = self.IsExpandable()
        return self.expandable

    def IsExpandable(self):
        """Return whether there are subitems."""
        return 1

    def _GetSubList(self):
        """Do not override!  Called by TreeNode."""
        if not self.IsExpandable():
            return []
        sublist = self.GetSubList()
        if not sublist:
            self.expandable = 0
        return sublist

    def IsEditable(self):
        """Return whether the item's text may be edited."""

    def SetText(self, text):
        """Change the item's text (if it is editable)."""

    def GetIconName(self):
        """Return name of icon to be displayed normally."""

    def GetSelectedIconName(self):
        """Return name of icon to be displayed when selected."""

    def GetSubList(self):
        """Return list of items forming sublist."""

    def OnDoubleClick(self):
        """Called on a double-click on the item."""


# Example application

class FileTreeItem(TreeItem):
    """Example TreeItem subclass -- browse the file system."""

    def __init__(self, path):
        self.path = path

    def GetText(self):
        return os.path.basename(self.path) or self.path

    def IsEditable(self):
        return os.path.basename(self.path) != ""

    def SetText(self, text):
        newpath = os.path.dirname(self.path)
        newpath = os.path.join(newpath, text)
        if os.path.dirname(newpath) != os.path.dirname(self.path):
            return
        try:
            os.rename(self.path, newpath)
            self.path = newpath
        except OSError:
            pass

    def GetIconName(self):
        if not self.IsExpandable():
            return "python"  # XXX wish there was a "file" icon

    def IsExpandable(self):
        return os.path.isdir(self.path)

    def GetSubList(self):
        try:
            names = os.listdir(self.path)
        except OSError:
            return []
        names.sort(key=os.path.normcase)
        dir = []
        base = []
        for i in names:
            if os.path.isdir(os.path.join(self.path, i)):
                dir.append(i)
            else:
                base.append(i)
        names = dir + base
        sublist = []
        for name in names:
            item = FileTreeItem(os.path.join(self.path, name))
            sublist.append(item)
        return sublist


# A canvas widget with scroll bars and some useful bindings

class ScrolledCanvas:

    def __init__(self, master, **opts):
        if 'yscrollincrement' not in opts:
            opts['yscrollincrement'] = 17
        self.master = master
        self.frame = Frame(master, width=150)
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)
        self.canvas = Canvas(self.frame, width=140, **opts)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.vbar = Scrollbar(self.frame, name="vbar")
        self.vbar.grid(row=0, column=1, sticky="nse")
        self.hbar = Scrollbar(self.frame, name="hbar", orient="horizontal")
        self.hbar.grid(row=1, column=0, sticky="ews")
        self.canvas['yscrollcommand'] = self.vbar.set
        self.vbar['command'] = self.canvas.yview
        self.canvas['xscrollcommand'] = self.hbar.set
        self.hbar['command'] = self.canvas.xview
        self.canvas.bind("<Key-Prior>", self.page_up)
        self.canvas.bind("<Key-Next>", self.page_down)
        self.canvas.bind("<Key-Up>", self.unit_up)
        self.canvas.bind("<Key-Down>", self.unit_down)
        self.canvas.bind("<MouseWheel>", wheel_event)
        self.canvas.bind("<Button-4>", wheel_event)
        self.canvas.bind("<Button-5>", wheel_event)
        # if isinstance(master, Toplevel) or isinstance(master, Tk):
        self.canvas.bind("<Alt-Key-2>", self.zoom_height)
        self.canvas.focus_set()

    def page_up(self, event):
        self.canvas.yview_scroll(-1, "page")
        return "break"

    def page_down(self, event):
        self.canvas.yview_scroll(1, "page")
        return "break"

    def unit_up(self, event):
        self.canvas.yview_scroll(-1, "unit")
        return "break"

    def unit_down(self, event):
        self.canvas.yview_scroll(1, "unit")
        return "break"

    def zoom_height(self, event):
        zoomheight.zoom_height(self.master)
        return "break"


def gettime(): return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


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
        root.geometry('640x400+620+250')
        root.title(title)
        # root.resizable(False, False)
        root.iconbitmap(os.path.join(os.path.dirname(sys.argv[0]), '.\\icon\\notepad.ico'))
        text = ScrolledText(root, background="white", relief=FLAT, bootstyle=ROUND)
        text.pack(fill=BOTH, expand=YES)
        text.insert(1.0, string)
        # text.configure(state='disabled')
        root.wait_window()

    @staticmethod
    def show_file(path, length, gets):
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
                ("文本长度:", length),
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
                                while True:
                                    if Messagebox.okcancel("文件被以错误的编码加载,\n是否以二进制读写?",
                                                           "编码错误") == "确定":
                                        self.text.append(
                                            TextEdit(self.frame[-1], font=self.fontname, undo=True, borderwidth=1))
                                        self.text[-1].delete("1.0", END)
                                        with open(self.paths[-1], 'rb') as fo:
                                            self.text[-1].insert(END, hex(int.from_bytes(fo.read())))
                                        break
                                    else:
                                        try:
                                            self.choose_encodings(askencoding())
                                            self.saves(self.paths[self.note.index(self.note.select())])
                                        except UnicodeError:
                                            pass
                                        else:
                                            break
                                        finally:
                                            pass
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

    def open_dir(self):
        # self.dir = ScrolledCanvas(self)
        path = askdirectory()
        if path != '':
            self.item = FileTreeItem(path)
            self.node = TreeNode(self.dir.canvas, None, self.item, self)
            self.node.expand()

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
            i.linenumbers.update_colors(self.choosecolor()[1])

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
        # self.dir.frame.config(height=self.winfo_height()-44-self.files.winfo_height())
        try:
            # print(len(text))
            # self.dir.frame.config(height=self.winfo_height()-44-self.files.winfo_height())
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
        cd8.add_command(
            label="更多编码",
            command=lambda: self.opens(
                "rt",
                askencoding()))
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
        cd.add_command(label="词频统计", command=lambda: threading.Thread(target=self.lcut).start())
        cd.add_command(label="文件信息",
                       command=lambda: self.show_file(self.paths[self.note.index(self.note.select())], len(
                           self.text[self.note.index(self.note.select())].get("1.0", END)),
                                                      self.text[
                                                          self.note.index(self.note.select())].get(
                                                          "1.0", END)))
        cd.add_command(label="文件列表", command=self.post_input_list)
        cd.add_separator()
        cd.add_command(label="打开(O)            Ctrl+O", command=self.choose)
        cd.add_command(label="打开文件夹", command=self.open_dir)
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
        # cd12.add_command(label="运行python F5", command=self.run_module)
        # cd12.add_command(label="运行pyw Ctrl+B", command=self.pyw)
        # cd12.add_command(
        #     label="python shell",
        #     command=lambda: subprocess.Popen("shell"))
        # cd12.add_command(
        #     label="运行C语言",
        #     command=lambda: self.gcc("gcc.exe", self.paths[self.note.index(self.note.select())]))
        # cd12.add_command(
        #     label="运行C++",
        #     command=lambda: self.gcc("g++.exe", self.paths[self.note.index(self.note.select())]))
        # cd12.add_command(
        #     label="运行.vbs .js",
        #     command=lambda: self.run_modules(f"wscript {self.paths[self.note.index(self.note.select())]}"))
        # cd12.add_command(label="运行.html", command=lambda: self.run_modules(
        #     f'"C:\\Program Files\\Internet Explorer\\iexplore.exe" {self.paths[self.note.index(self.note.select())]}'))
        # cd9.add_cascade(label="运行", menu=cd12)
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
        self.files = ScrolledFrame(self, width=150)
        self.dir = ScrolledCanvas(self)
        self.item = FileTreeItem(os.path.dirname(self.paths[0]))
        self.node = TreeNode(self.dir.canvas, None, self.item, self)
        self.node.expand()
        Label(self, text="打开的文件", font=("Microsoft YaHei UI", 10, "bold")).pack(anchor=W, side=TOP, fill=Y)
        self.files.pack(side=TOP, fill=Y, anchor=W)
        Label(self, text="打开的文件夹", font=("Microsoft YaHei UI", 10, "bold")).pack(side=TOP, fill=Y, anchor=W)
        self.dir.frame.pack(side=TOP, fill=Y, anchor=W)

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
        Style(theme="sandstone")
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
