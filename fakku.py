#!/usr/bin/env python3

"""
Python Fakku Downloader

"""

import urllib.request
import os.path
import os
import re
import sys
from tkinter import *

re_pages = re.compile(r'<b>([0-9]+)</b> pages')
re_url = re.compile(r"return '(.+?)' \+ x \+ '\.jpg';")
imgname = '{:03}.jpg'

def get_html(url):
    conn = urllib.request.urlopen(url)
    data = conn.read()
    conn.close()
    data = data.decode('UTF-8')
    return data


def save(url, path):
    conn = urllib.request.urlopen(url)
    data = conn.read()
    conn.close()
    if os.path.exists(path):
        raise IOError('File exists.')
    with open(path, 'wb') as f:
        f.write(data)


def get_loc(url):
    """Get image location url"""
    page1 = url + '/read#page=1'
    html = get_html(page1)
    match = re_url.search(html)
    if not match:
        raise ParsingError(html)
    return match.group(1)


def get_pages(url):
    """Get number of pages"""
    html = get_html(url)
    match = re_pages.search(html)
    if not match:
        raise ParsingError(html)
    return int(match.group(1))


def dl(url, dir):
    print("Save: " + url)
    print("Here: " + dir)
    loc = get_loc(url)
    npages = get_pages(url)
    if os.path.exists(dir):
        raise IOError('File exists.')
    os.mkdir(dir)
    for i in range(1, npages + 1):
        save(loc + imgname.format(i), os.path.join(dir, imgname.format(i)))
        print('downloaded {}'.format(i))
    print('done.')


class Display(Text):

    def write(self, text):
        self.insert(END, text)
        self.see(END)
        self.update_idletasks()

    def flush(self):
        pass


class App:

    def __init__(self):
        self.root = Tk()
        self.root.wm_title("Fakku Downloader")
        self.root.bind_class("Text","<Control-a>", self.display_selectall)
        self.root.bind_class("Entry","<Control-a>", self.entry_selectall)

        row1 = Frame(self.root)
        row1.pack(side=TOP)
        row2 = Frame(self.root)
        row2.pack(side=TOP)
        row3 = Frame(self.root)
        row3.pack(side=TOP)
        row4 = Frame(self.root)
        row4.pack(side=TOP)

        self.url_label = Label(row1, text='URL')
        self.url_label.pack(side=LEFT)
        self.url = Entry(row1)
        self.url.pack(side=LEFT)

        self.name_label = Label(row2, text='Name')
        self.name_label.pack(side=LEFT)
        self.name = Entry(row2)
        self.name.bind('<Return>', self.dl)
        self.name.pack(side=LEFT)

        self.button = Button(row3, text="Download", command=self.dl)
        self.button.pack()

        self.output = Display(row4)
        self.output.pack()
        sys.stdout = self.output
        #sys.stderr = self.output

    def entry_selectall(self, event):
        event.widget.select_range(0, END)

    def display_selectall(self, event):
        event.widget.tag_add(SEL, '1.0', END)

    def mainloop(self):
        self.root.mainloop()

    def quit(self):
        self.root.quit()

    def dl(self, *args):
        dl(self.url.get(), self.name.get())        


class ParsingError(Exception):
    pass


def main(*args):

    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-g', dest='gui', action='store_true', default=False)
    parser.add_argument('url', nargs='?')
    parser.add_argument('name', nargs='?')
    args = parser.parse_args(args)
    
    if args.gui:
        app = App()
        app.mainloop()
    else:
        try:
            dl(args.url, args.name)
        except NameError as e:
            raise e


if __name__ == "__main__":
    import sys
    main(*sys.argv[1:])