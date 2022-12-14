import random
from math import sin, cos, pi, log
import tkinter as tk
import time
from playsound import playsound
from pathlib import Path
from threading import Thread
import threading
import os
import sys

IMAGE_ENLARGE = 11
HEART_COLOR = "#FF0000"
CHOOSE_POINT = 5000


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
 
def heart_function(t, shrink_ratio: float = IMAGE_ENLARGE):
   
    x = 16 * (sin(t) ** 3)
    y = - (13 * cos(t) - 5 * cos(2 * t) - 2 *cos(3 * t) - cos(3 * t))
 
 
    x *= shrink_ratio
    y *= shrink_ratio
 
    x += CANVAS_CENTER_X
    y += CANVAS_CENTER_Y
    return int(x), int(y)
 
def scatter_inside(x, y, benta=0.15):
    ratio_x = - benta * log(random.random())
    ratio_y = - benta * log(random.random())
    dx = ratio_x * (x - CANVAS_CENTER_X)
    dy = ratio_y * (y - CANVAS_CENTER_Y)
    return x - dx, y - dy
    
def shrink(x, y, ratio):
    force = -1 / (((x - CANVAS_CENTER_X) ** 2 + (y - CANVAS_CENTER_Y) ** 2) ** 0.6)
    dx = ratio * force * (x - CANVAS_CENTER_X)
    dy = ratio * force * (y - CANVAS_CENTER_Y)
    return x - dx, y - dy

def curve(p):
    return 2 * (2 * sin(4 * p)) / (2 * pi)

class Heart:
    def __init__(self, generate_frame = 20):
        self._points = set()
        self._edge_diffusion_points = set()
        self._center_diffusion_points = set()
        self.all_points = {}
        self.build(CHOOSE_POINT)
        self.generate_frame = generate_frame
        for frame in range(generate_frame):
            self.calc(frame)
 
    def build(self, number):
        for _ in range(number):
            t = random.uniform(0, 2 * pi)
            x, y = heart_function(t)
            self._points.add((x, y))
 
        for _x, _y in list(self._points):
            for _ in range(3):
                x, y = scatter_inside(_x, _y, 0.3)
                self._edge_diffusion_points.add((x, y))
 
        point_list = list (self._points)
        for _ in range(2500):
            x, y = random.choice(point_list)
            x, y = scatter_inside (x, y, 0.2)
            self._center_diffusion_points.add((x, y))
            
    @staticmethod
    def calc_position(x, y, ratio):
        force = 1 / (((x - CANVAS_CENTER_X) ** 2 +
                      (y - CANVAS_CENTER_Y) ** 2) ** 0.520)
        dx = ratio * force * (x - CANVAS_CENTER_X)
        dy = ratio * force * (y - CANVAS_CENTER_Y)
        return x - dx, y - dy

    def calc(self, generate_frame):
        ratio = 10 * curve(generate_frame / 10 * pi)
        halo_radius = int(4 * 6 * (1 + curve(generate_frame / 10 * pi)))
        halo_number = 25
        all_points = []
        heart_halo_points = set()
        for _ in range (halo_number):
            t = random.uniform(0, 2 * pi)
            x, y = heart_function(t, shrink_ratio=11.5)
            x, y = shrink(x, y, halo_radius)
            if (x, y) not in heart_halo_points:
                heart_halo_points.add((x, y))
                x += random.randint(-70, 70)
                y += random.randint(-70, 70)
                size = random.choice((1, 2, 3, 4))
                all_points.append((x, y, size))
        for x, y in self._edge_diffusion_points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1,2)
            all_points.append((x, y, size))
        for x, y in self._center_diffusion_points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1,2)
            all_points.append((x, y, size))
        self.all_points[generate_frame] = all_points

    def render(self, render_canvas, render_frame):
        for x, y, size in self.all_points[render_frame % self.generate_frame]:
            render_canvas.create_rectangle(x, y, x + size, y + size, width = 0, fill = HEART_COLOR)
        render_tree(render_canvas)
        render_snow(render_canvas)

def draw(root: tk.Tk, render_canvas: tk.Canvas, render_heart:Heart, render_frame = 0):
    render_canvas.delete('all')
    render_heart.render(render_canvas, render_frame)
    root.after(160, draw, root, render_canvas, render_heart, render_frame +1)

def render_tree(render_canvas: tk.Canvas):
    draw_tree_fixed(render_canvas, 70, 830)
    draw_tree_fixed(render_canvas, 142, 810)
    draw_tree_fixed(render_canvas, 250, 820)
    draw_tree_fixed(render_canvas, 329, 840)
    draw_tree_fixed(render_canvas, 402, 830)
    draw_tree_fixed(render_canvas, 475, 810)
    draw_tree_fixed(render_canvas, 595, 840)
    draw_tree_fixed(render_canvas, 675, 810)
    draw_tree_fixed(render_canvas, 783, 840)
    draw_tree_fixed(render_canvas, 847, 820)
    draw_tree_fixed(render_canvas, 925, 840)
    draw_tree_fixed(render_canvas, 1047, 830)
    draw_tree_fixed(render_canvas, 1119, 810)
    draw_tree_fixed(render_canvas, 1204, 840)
    draw_tree_fixed(render_canvas, 1269, 820)
    draw_tree_fixed(render_canvas, 1339, 840)
    draw_tree_fixed(render_canvas, 1458, 830)
    draw_tree_fixed(render_canvas, 1514, 810)
    draw_tree_fixed(render_canvas, 1644, 830)
    draw_tree_fixed(render_canvas, 1785, 820)
    draw_tree_fixed(render_canvas, 1859, 820)
    for i in range(len(Tree)):
        draw_tree(render_canvas, Tree[i])

def draw_tree(render_canvas: tk.Canvas, Tree):
    x = Tree[0]
    y = Tree[1]
    points = [x,y, x-30,y+80, x+30,y+80]
    render_canvas.create_polygon(points, fill='green')
    points = [x,y+40, x-30,y+120, x+30,y+120]
    render_canvas.create_polygon(points, fill='green')
    points = [x,y+80, x-30,y+160, x+30,y+160]
    render_canvas.create_polygon(points, fill='green')

def draw_tree_fixed(render_canvas: tk.Canvas, x, y):
    points = [x,y, x-30,y+80, x+30,y+80]
    render_canvas.create_polygon(points, fill='green')
    points = [x,y+40, x-30,y+120, x+30,y+120]
    render_canvas.create_polygon(points, fill='green')
    points = [x,y+80, x-30,y+160, x+30,y+160]
    render_canvas.create_polygon(points, fill='green')

def render_snow(render_canvas: tk.Canvas):
    for i in range(len(snowFall)):
        draw_snow(render_canvas, snowFall[i])
 
        snowFall[i][1] += snowFall[i][3]
        if snowFall[i][1] > CANVAS_HEIGHT:
            y = random.randrange(-50, -10)
            snowFall[i][1] = y
        
            x = random.randrange(0, CANVAS_WIDTH)
            snowFall[i][0] = x

def draw_snow(render_canvas: tk.Canvas, snowFall):
    x = snowFall[0]
    y = snowFall[1]
    Snow_size = snowFall[2]
    smallsize = Snow_size - 1 
    render_canvas.create_line(x-Snow_size,y, x+Snow_size,y, fill='white')
    render_canvas.create_line(x,y-Snow_size, x,y+Snow_size, fill='white')
    render_canvas.create_line(x+smallsize,y-smallsize, x-smallsize,y+smallsize, fill='white')
    render_canvas.create_line(x-smallsize,y-smallsize, x+smallsize,y+smallsize, fill='white')

def play_music():
    audio = resource_path("WithYou.mp3")
    playsound(audio)
    canvas.after(500, closeWindow)

def Main_screen():
    canvas.delete('all')
    for i in range(200):
        x = random.randrange(0, CANVAS_WIDTH)
        y = random.randrange(0, CANVAS_HEIGHT)
        Snow_size = random.randint(0,6)
        Snow_speed = random.randint(1,6)
        snowFall.append([x, y, Snow_size, Snow_speed])

    for i in range(10):
        x = random.randrange(0, CANVAS_WIDTH)
        y = random.randrange(800, 860)
        Tree.append([x, y])


    heart = Heart()
    next = 0
    for x,y in heart._points:
        if next <= 30:
            if next == 0 :
                text_1 = canvas.create_text(CANVAS_CENTER_X, CANVAS_CENTER_Y, text="Loading...", fill="#A00000", font=('Helvetica 13'))
            elif next == 30:
                canvas.delete(text_1)
            next = next + 1
        elif next > 30 and next <= 60:
            if next == 31 :
                text_2 = canvas.create_text(CANVAS_CENTER_X, CANVAS_CENTER_Y, text="Loading??..", fill="#A00000", font=('Helvetica 13'))
            elif next == 60:
                canvas.delete(text_2)
            next = next + 1
        elif next > 60 and next <= 90:
            if next == 61 :
                text_3 = canvas.create_text(CANVAS_CENTER_X, CANVAS_CENTER_Y, text="Loading.??.", fill="#A00000", font=('Helvetica 13'))
            elif next == 90:
                canvas.delete(text_3)
            next = next + 1
        elif next > 90 and next <= 120:
            if next == 91 :
                text_4 = canvas.create_text(CANVAS_CENTER_X, CANVAS_CENTER_Y, text="Loading..??", fill="#A00000", font=('Helvetica 13'))
            elif next == 120:
                canvas.delete(text_4)
            next = next + 1
        elif next > 120:
            next = 0
        canvas.create_rectangle(x, y, x + 1, y + 1, width = 0, fill = HEART_COLOR)
        root.update()
        time.sleep(0.02)

    canvas.delete(text_1)
    canvas.delete(text_2)
    canvas.delete(text_3)
    canvas.delete(text_4)
    root.update()

    countdown = 10
    for i in range(11):
        text_5 = canvas.create_text(CANVAS_CENTER_X, CANVAS_CENTER_Y, text=str(countdown), fill="#FFFFFF", font=('Helvetica 16'))
        root.update()
        time.sleep(1)
        canvas.delete(text_5)
        root.update()
        countdown = countdown - 1


    draw(root, canvas, heart)
    t2.start()

def Write(str, delta):
    canvas_t = canvas.create_text(CANVAS_CENTER_X,CANVAS_CENTER_Y,text='',fill="#FFFFFF", font=('Helvetica 16'))
    ourtex = str
    delay = 0
    for x in range(len(ourtex) + 1):
        s = ourtex[:x]
        newtext = lambda s=s: canvas.itemconfigure(canvas_t, text = s)
        canvas.after(delay, newtext)
        delay += delta
    
def WriteFisrt():
    Write('Hi Crush!!!!', 200)
    canvas.after(4000, WriteSecond)

def WriteSecond():
    canvas.delete('all')
    Write('Thanks for not rejecting me and I very happy the days with you', 90)
    canvas.after(9000, WriteThird)

def WriteThird():
    canvas.delete('all')
    Write('I have a thing that I want to show you, But I have a question first', 100)
    canvas.after(9000, WriteFourth)

def WriteFourth():
    canvas.delete('all')
    Write('Do you agree to go date with me on Christmas Eve 24th Dec?', 100)
    canvas.after(7000, yes_no_button)

def ThankyouWindow():
    canvas.delete('all')
    Write('Thank you <3', 200)
    canvas.after(5000, Main_screen)

def closeWindow():
    canvas.destroy()
    root.destroy()

def HandleIfPressNoButton():
    canvas.delete('all')
    canvas.create_text(CANVAS_CENTER_X,CANVAS_CENTER_Y,text='C??i g?? ????y? sao em l???i nh???m v?? n??t n??y!!!! Kh???i cho coi tr??i tim lu??n',fill="#FFFFFF", font=('Helvetica 16'))
    canvas.after(4000,closeWindow)

def yes_button(event):
    ThankyouWindow()

def no_button(event):
    HandleIfPressNoButton()

def yes_no_button():

    #button yes 
    buttonBG_YES = canvas.create_rectangle(3*CANVAS_WIDTH/4, 3*CANVAS_HEIGHT/4, 3*CANVAS_WIDTH/4+100, 3*CANVAS_HEIGHT/4+30, fill="black", outline="white")
    buttonTXT_YES = canvas.create_text(3*CANVAS_WIDTH/4+50, 3*CANVAS_HEIGHT/4+15, text="YES", fill='white')
    canvas.tag_bind(buttonBG_YES, "<Button-1>", yes_button) ## when the square is clicked runs function "clicked".
    canvas.tag_bind(buttonTXT_YES, "<Button-1>", yes_button) ## same, but for the text.

    buttonBG_NO = canvas.create_rectangle(CANVAS_WIDTH/4, 3*CANVAS_HEIGHT/4, CANVAS_WIDTH/4+100, 3*CANVAS_HEIGHT/4+30, fill="black", outline="white")
    buttonTXT_NO = canvas.create_text(CANVAS_WIDTH/4+50, 3*CANVAS_HEIGHT/4+15, text="NO", fill='white')
    canvas.tag_bind(buttonBG_NO, "<Button-1>", no_button) ## when the square is clicked runs function "clicked".
    canvas.tag_bind(buttonTXT_NO, "<Button-1>", no_button) ## same, but for the text.

def raise_frame(frame):
    frame.tkraise()

if __name__ == '__main__':
    t2 = threading.Thread(target=play_music)
    root = tk.Tk()
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    root.state('zoomed')
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    canvas = tk.Canvas(root, bg='black', height=screen_height, width=screen_width)
    canvas.pack()
    CANVAS_WIDTH = screen_width
    CANVAS_HEIGHT = screen_height
    CANVAS_CENTER_X = CANVAS_WIDTH / 2
    CANVAS_CENTER_Y = CANVAS_HEIGHT / 2
    snowFall = []
    Tree = []
    WriteFisrt()
    root.mainloop()