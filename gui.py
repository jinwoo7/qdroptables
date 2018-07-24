import threading
import json
from tkinter import *
from PIL import Image, ImageTk

window = Tk()

def gui():
    pass

def window(filepath, data):
    # parse data

    # set up image
    img = Image.open(filepath)
    w, h = img.size

    # set up window
    window.title("Testing")
    window.configure(background='black')
    window.geometry("%dx%d" % (w+200, h+200))
    
    # set up image to be displayed
    img_tk = ImageTk.PhotoImage(img)
    
    # draw rectangle
    canvas = Canvas(window, width=w, height=h)
    canvas.pack()
    canvas.config(borderwidth=0, background='black', highlightcolor='black')
    canvas.create_image(0, 0, anchor=NW, image=img_tk)

    outlines = ['white', 'yellow', 'red', 'green', 'blue']
    canvas.create_rectangle(50, 50, 100, 100, width=1.5, outline='blue')

    # open window
    window.mainloop()

with open('../Downloads/data.txt') as json_file:
    data = json.load(json_file)
    window("./index.jpeg", data)
