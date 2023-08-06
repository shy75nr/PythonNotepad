from need.ttkbootstrap import *
import threading
import os
import time
from need.ttkbootstrap.icons import Emoji
from tkinter import EventType
from pathlib import Path
import pygame.mixer as music
from mutagen.mp3 import MP3
from sidebar import *
from idlelib.idle_test.test_sidebar import *
from need.ttkbootstrap.dialogs import Messagebox


def validate_number(x) -> bool:
    """Validates that the input is a number"""
    if x.isdigit():
        return True
    elif x == "":
        return True
    else:
        return False
def wheel_event(event, widget=None, linenumbers=None):
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
    linenumbers.yview(SCROLL,lines,'units')
    return 'break'

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
        self.TerminalText = Text(self, cnf, **kw)
        self.stp = Scrollbar(self, command=self.scroll, bootstyle=ROUND)
        self.TerminalText.config(yscrollcommand=self.stp.set)
        self.stp.pack(side=RIGHT, fill=Y)
        self.TerminalText.pack(fill=BOTH, expand=YES, side=RIGHT)
        self.TerminalText.configure(yscrollcommand=self.stp.set)
        editwin = Dummy_editwin(self.TerminalText)
        editwin.vbar = self.stp
        self.linenumbers = LineNumbers(editwin)
        self.linenumbers.sidebar_text.config(yscrollcommand=self.stp.set)
        self.linenumbers.sidebar_text.pack(fill=Y, expand=YES)
        self.txt = ''
        self.TerminalText.bind("<Return>", self.enter)
        self.TerminalText.bind("<MouseWheel>", lambda event:wheel_event(event,self.TerminalText,self.linenumbers.main_widget))
        self.TerminalText.bind("<[>", lambda e: threading.Thread(target=self.printer, args=(']',)).start())
        self.TerminalText.bind("<(>", lambda e: threading.Thread(target=self.printer, args=(')',)).start())
        self.TerminalText.bind("<{>", lambda e: threading.Thread(target=self.printer, args=('}',)).start())
        self.TerminalText.bind("<'>", lambda e: threading.Thread(target=self.printer, args=('\'',)).start())
        self.TerminalText.bind("<\">", lambda e: threading.Thread(target=self.printer, args=('"',)).start())
        threading.Thread(target=self.set_func).start()

    def scroll(self, *xy):
        self.TerminalText.yview(*xy)
        self.linenumbers.sidebar_text.yview(*xy)
        return 'break'
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
        self.linenumbers.update_font(font)

    def enter(self, *args):
        if self.parents.master.is_coding.get():
            a = float(self.TerminalText.index('insert'))
            b = self.TerminalText.get(float(int(a)), a).replace('\n', '')
            c = b
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
        return self.TerminalText.see(index)

    def bind(self, sue, func, add=None):
        self.TerminalText.bind(sue, func, add)
