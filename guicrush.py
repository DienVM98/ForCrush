import random
from math import sin, cos, pi, log
from tkinter import *
import turtle
import time

IMAGE_ENLARGE = 11
HEART_COLOR = "#FF0000"
 
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
        self.build(3000)
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
        for _ in range(4000):
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
        halo_number = 100
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
                size = random.choice((2, 2, 1))
                all_points.append((x, y, size))
        for x, y in self._edge_diffusion_points:
            x, y = self.calc_position(x, y, ratio)
            size = 1
            all_points.append((x, y, size))
        for x, y in self._center_diffusion_points:
            x, y = self.calc_position(x, y, ratio)
            size = 1
            all_points.append((x, y, size))
        self.all_points[generate_frame] = all_points

    def render(self, render_canvas, render_frame):
        for x, y, size in self.all_points[render_frame % self.generate_frame]:
            render_canvas.create_rectangle(x, y, x + size, y + size, width = 0, fill = HEART_COLOR)
        render_tree(render_canvas)
        render_snow(render_canvas)

def draw(root: Tk, render_canvas: Canvas, render_heart:Heart, render_frame = 0):
    render_canvas.delete('all')
    render_heart.render(render_canvas, render_frame)
    root.after(160, draw, root, render_canvas, render_heart, render_frame +1)

def render_tree(render_canvas: Canvas):
    draw_tree(render_canvas, 70, 830)
    draw_tree(render_canvas, 142, 810)
    draw_tree(render_canvas, 250, 820)
    draw_tree(render_canvas, 329, 840)
    draw_tree(render_canvas, 402, 830)
    draw_tree(render_canvas, 475, 810)
    draw_tree(render_canvas, 595, 840)
    draw_tree(render_canvas, 675, 810)
    draw_tree(render_canvas, 783, 840)
    draw_tree(render_canvas, 847, 820)
    draw_tree(render_canvas, 925, 840)
    draw_tree(render_canvas, 1047, 830)
    draw_tree(render_canvas, 1119, 810)
    draw_tree(render_canvas, 1204, 840)
    draw_tree(render_canvas, 1269, 820)
    draw_tree(render_canvas, 1339, 840)
    draw_tree(render_canvas, 1458, 830)
    draw_tree(render_canvas, 1514, 810)
    draw_tree(render_canvas, 1644, 830)
    draw_tree(render_canvas, 1785, 820)
    draw_tree(render_canvas, 1859, 820)

def draw_tree(render_canvas: Canvas, x,y):
    print('')
    points = [x,y, x-30,y+80, x+30,y+80]
    render_canvas.create_polygon(points, fill='green')
    points = [x,y+40, x-30,y+120, x+30,y+120]
    render_canvas.create_polygon(points, fill='green')
    points = [x,y+80, x-30,y+160, x+30,y+160]
    render_canvas.create_polygon(points, fill='green')

def render_snow(render_canvas: Canvas):
    for i in range(len(snowFall)):
        draw_snow(render_canvas, snowFall[i])
 
        snowFall[i][1] += 2
        if snowFall[i][1] > CANVAS_HEIGHT:
            y = random.randrange(-50, -10)
            snowFall[i][1] = y
        
            x = random.randrange(0, CANVAS_WIDTH)
            snowFall[i][0] = x

def draw_snow(render_canvas: Canvas, snowFall):
    x = snowFall[0]
    y = snowFall[1]
    Snow_size = snowFall[2]
    smallsize = Snow_size - 1 
    render_canvas.create_line(x-Snow_size,y, x+Snow_size,y, fill='white')
    render_canvas.create_line(x,y-Snow_size, x,y+Snow_size, fill='white')
    render_canvas.create_line(x+smallsize,y-smallsize, x-smallsize,y+smallsize, fill='white')
    render_canvas.create_line(x-smallsize,y-smallsize, x+smallsize,y+smallsize, fill='white')

if __name__ == '__main__':
    root = Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    canvas = Canvas(root, bg='black', height=screen_height, width=screen_width)
    canvas.pack()
    CANVAS_WIDTH = screen_width
    CANVAS_HEIGHT = screen_height
    CANVAS_CENTER_X = CANVAS_WIDTH / 2
    CANVAS_CENTER_Y = CANVAS_HEIGHT / 2
    snowFall = []
    for i in range(200):
        x = random.randrange(0, CANVAS_WIDTH)
        y = random.randrange(0, CANVAS_HEIGHT)
        Snow_size = random.randint(0,4)
        snowFall.append([x, y, Snow_size])
    size = random.randint(3,5)
    heart = Heart()
    for x,y in heart._points:
        canvas.create_text(CANVAS_CENTER_X, CANVAS_CENTER_Y, text="HELLO WORLD", fill="red", font=('Helvetica 15 bold'))
        canvas.create_rectangle(x, y, x + 1, y + 1, width = 0, fill = HEART_COLOR)
        root.update()
        time.sleep(0.01)

    time.sleep(1)    
    draw(root, canvas, heart)
    root.mainloop()
