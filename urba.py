#!/usr/bin/env python
# -*- coding: utf-8 -*-
#from parserFirst import parser1
from functools import partial
from PIL import ImageTk, Image # $ pip install pillow
import webbrowser
#from parserSecond import parser2
from urllib.request import urlopen
import requests, html2text, bs4
try:
    # Tkinter for Python 2.xx
    import Tkinter as tk
except ImportError:
    # Tkinter for Python 3.xx
    import tkinter as tk

def siteOpen1(y):
    webbrowser.open_new('https://www.culture.ru/' + y)

def siteOpen2(y):
    webbrowser.open_new('https://gorodzovet.ru' + y)

def splitter(text):
    s = []
    k = ''
    p = ''
    for i in range(len(text)):
        k += text[i]
        if text[i] == ' ':
            iter =i
            p = k
        if i % 20 == 0 and i > 0:
            s.append(p)
            k = text[iter + 1:i + 1]
            p = ''
    s.append(k)
    return '\n'.join(s)
        
def parser1():
    buttons = []
    def listTitle():
        #print(s28)
        for i in range(0,len(title)):
            if title[i] != '':
                #print(title[i])
                buttons.append(title[i])
                #scrollbar.config( command = b1.yview )
    #scrollbar = Scrollbar(root)
    #scrollbar.pack( side = RIGHT, fill = Y )
    s = requests.get('https://www.culture.ru/afisha/izhevsk')
    b = bs4.BeautifulSoup(s.text, 'html.parser')
    t = b.select('.entity-card_title')
    images = b.select('.thumbnail')
    #print(images)
    #print(t)
    s = ''.join(list(map(str, t)))
    imagesList = ''.join(list(map(str, images)))
    siteList = []
    a = False
    for i in range(len(s)):
        if s[i:i+7] == 'events/':
            a = True
            k = ''
        if a:
            if s[i] == '"':
                siteList.append(k)
                a = False
            else:
                k += s[i]
    #print(siteList)
                
                
    #t = html2text.HTML2Text().handle(s.text)

    for i in range(len(t)):
        y = i
        title = t[i].getText().split('\n')
        listTitle()
    imagesList = ''.join(list(map(str, images)))
    a = False
    photos = []
    for i in range(len(imagesList)):
        if imagesList[i:i + 5] == 'src="':
            a = True
            k = ''
            count = 0
        if a:
            if imagesList[i] == '"':
                count += 1
            if count == 2:
                a = False
                photos.append(k[5:])
            else:
                k += imagesList[i]
    return list(splitter(i) for i in buttons), siteList, photos


def parser2():
    def listTitle():
        #print(s28)
        for i in range(0,len(title)):
            if title[i] != '':
                buttons.append(title[i])
                #scrollbar.config( command = b1.yview )

    #scrollbar = Scrollbar(root)
    #scrollbar.pack( side = RIGHT, fill = Y )
    buttons = []
    s = requests.get('https://gorodzovet.ru/izhevsk/')
    b = bs4.BeautifulSoup(s.text, 'html.parser')
    t = b.select('.eventBox__title')
    silka = b.select('.eventBox')
    s = ''.join(list(map(str, silka)))
    siteList = []
    photos=[]
    a = False
    phurl = False
    for i in range(len(s)):
        if s[i:i+2] == '//':
            phurl = True
            p= ''
        if phurl:
            if s[i] == '"':
                photos.append('https:' + p)
                phurl= False
            else:
                p += s[i]
        if s[i:i+9] == '/izhevsk/':
            a = True
            count = 0
            k = ''
        if a:
            if s[i] == '/':
                count += 1
                if count == 3:
                    a = False
                    continue
            if s[i] == '"':
                siteList.append(k)
                a = False
            else:
                k += s[i]
                
    #t = html2text.HTML2Text().handle(s.text)

    for i in range(len(t)):
        y = i
        title = t[i].getText().split('\n')
        listTitle()
    return list(splitter(i) for i in buttons), siteList, photos

APP_TITLE = "THE BEST PROGRAMM EVER OF AFISHA"
APP_XPOS = 0
APP_YPOS = 0
NUM_OF_BUTTONS = 20
a = parser1()
buttons1, site1, photos1 = a[0], a[1], a[2]
b = parser2()
buttons2, site2, photos2 = b[0], b[1], b[2]
#print(parser1()) 
class Application(tk.Frame):
    
    def __init__(self, master, **options):
        
        global X
        X = master.winfo_screenwidth()
        self.master = master
        self.master.protocol("WM_DELETE_WINDOW", self.close)
         
        tk.Frame.__init__(self, master, **options)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)     
        self.canvas = tk.Canvas(self, bg='steelblue', highlightthickness=0)
             
        self.canvas.grid(row=0, column=0, sticky='wesn')
         
        self.yscrollbar = tk.Scrollbar(self, orient="vertical",
            width=14, command=self.canvas.yview)
        self.yscrollbar.grid(row=0, column=1, sticky='ns')
 
        self.xscrollbar = tk.Scrollbar(self, orient="horizontal",
            width=14, command=self.canvas.xview)
        self.xscrollbar.grid(row=1, column=0, sticky='we')
         
        self.canvas.configure(
            xscrollcommand=self.xscrollbar.set,
            yscrollcommand=self.yscrollbar.set)
        
        self.button_frame = tk.Frame(self.canvas, bg=self.canvas['bg'])
        self.button_frame.pack()
        self.canvas.create_window((0,0), window=self.button_frame, anchor="nw")
        c = 0
        r = 1
        self.BUTTONS1 = []
        for button in buttons1 + buttons2:

            if button in buttons1:
                '''
                im = Image.open(urlopen(photos1[buttons1.index(button)]))
                im = im.resize((400, 160))
                im.save('Foto.png')
                image1 = ImageTk.PhotoImage(file='Foto.png')'''
                button = tk.Button(self.button_frame, text=button, 
                highlightthickness=0, bg='#6b6262', fg = '#ffde27', font = 'Verdana 15',width = round(X) // 60, padx=round(X) // 15, height = 7, command=lambda x = site1[buttons1.index(button)]: siteOpen1(x))
                self.BUTTONS1.append(button)
                # button.config(image=image1)
                button.grid(row = r,column= c)
                # button.image = image1
                self.bind_mouse_scroll(button, self.yscroll)
            else:
                '''
                im = Image.open(urlopen(photos2[buttons2.index(button)]))
                im = im.resize((400, 160))
                im.save('Foto.png')
                image1 = ImageTk.PhotoImage(file='Foto.png')'''
                button = tk.Button(self.button_frame, text=button, 
                highlightthickness=0, bg='#6b6262', fg = '#ffde27', font = 'Verdana 15',width = round(X) // 60, padx=round(X) // 15, height = 7, command=lambda x = site2[buttons2.index(button)]: siteOpen2(x))
                button.grid(row = r, column = c)
                # button.image=image1
                # button.bind("<Enter>", view)
                self.bind_mouse_scroll(button, self.yscroll)
            c+=1
            if c % 3 == 0:
                r +=1
                c=0
        
        self.canvas.bind('<Configure>', self.update)
        self.bind_mouse_scroll(self.canvas, self.yscroll)
        self.bind_mouse_scroll(self.xscrollbar, self.xscroll)
        self.bind_mouse_scroll(self.yscrollbar, self.yscroll)
        self.bind_mouse_scroll(self.button_frame, self.yscroll)
        #self.canvas.focus_set()
         
    def bind_mouse_scroll(self, parent, mode):
        #~~ Windows only
        parent.bind("<MouseWheel>", mode)
        #~~ Unix only        
        parent.bind("<Button-4>", mode)
        parent.bind("<Button-5>", mode)
 
    def yscroll(self, event):
        if event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "unit")
        elif event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "unit")
 
    def xscroll(self, event):
        if event.num == 5 or event.delta < 0:
            self.canvas.xview_scroll(1, "unit")
        elif event.num == 4 or event.delta > 0:
            self.canvas.xview_scroll(-1, "unit")
 
    def update(self, event):
        if self.canvas.bbox('all') != None:
            region = self.canvas.bbox('all')
            self.canvas.config(scrollregion=region)
             
    def button_callback(self, button):
        pass
        #print(button)
                       
    def close(self):
        #print("Application-Shutdown")
        self.master.destroy()
 
     
def main():
    
    app_win = tk.Tk()
    app_win.iconbitmap(r'C:\Users\Sasha\Desktop\hak\icona.ico')
    '''
    def start():
            app = Application(app_win)
            app.pack(fill='both', expand=True)
            bt1.destroy()
            fonLabel.destroy()
            '''
    X = app_win.winfo_screenwidth()
    Y = app_win.winfo_screenheight()
    app_win.title(APP_TITLE)
    app_win.geometry("+{}+{}".format(0, 0))
    app_win.geometry("{}x{}".format(round(X), round(Y)))
    '''
    fonbg = tk.PhotoImage(file='fon.gif')
    fonLabel = tk.Label(app_win, image=fonbg)
    fonLabel.pack()
    bt1 = tk.Button(app_win, text='Start', font='Verdana 18', command = start)
    bt1.pack()
    '''
    app = Application(app_win)
    app.pack(fill='both', expand=True)
    app_win.mainloop()
if __name__ == '__main__':
    main()      
