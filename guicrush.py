import random
from math import sin, cos, pi, log
from tkinter import *
import turtle
import time

CANVAS_WIDTH = 640
CANVAS_HEIGHT = 640
CANVAS_CENTER_X = CANVAS_WIDTH / 2
CANVAS_CENTER_Y = CANVAS_HEIGHT / 2
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
        self.build(1000)
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
        all_points = []
        for x, y in self._points:
            x, y = self.calc_position(x, y, ratio)
            size = 1
            # all_points.append((x, y, size))
        for x, y in self._edge_diffusion_points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 2)
            all_points.append((x, y, size))
        for x, y in self._center_diffusion_points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 2)
            all_points.append((x, y, size))
        self.all_points[generate_frame] = all_points

    def render(self, render_canvas, render_frame):
        for x, y, size in self.all_points[render_frame % self.generate_frame]:
            render_canvas.create_rectangle(x, y, x + size, y + size, width = 0, fill = HEART_COLOR)

def draw(root: Tk, render_canvas: Canvas, render_heart:Heart, render_frame = 0):
    render_canvas.delete('all')
    render_heart.render(render_canvas, render_frame)
    root.after(160, draw, root, render_canvas, render_heart, render_frame +1)

if __name__ == '__main__':
    root = Tk()
    canvas = Canvas(root, bg='black', height=CANVAS_HEIGHT, width=CANVAS_WIDTH)
    canvas.pack()
    heart = Heart()
    for x,y in heart._points:
        canvas.create_rectangle(x, y, x + 1, y + 1, width = 0, fill = HEART_COLOR)
        root.update()
        time.sleep(0.03)

    draw(root, canvas, heart)
    root.mainloop()
