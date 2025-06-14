# wireframe_block_mixed_axes.py

import tkinter as tk
import math
import time

class WireframeBlockMixedAxes:
    def __init__(self, master, width=200, height=100, depth=150):
        self.master = master
        self.canvas = tk.Canvas(master, width=600, height=600, bg='white')
        self.canvas.pack()

        # half-sizes
        w2, h2, d2 = width/2, height/2, depth/2
        # panjang sumbu di model-space
        self.axis_length = max(width, height, depth) * 1.2

        # block vertices
        self.vertices = [
            [-w2, -h2, -d2],
            [ w2, -h2, -d2],
            [ w2,  h2, -d2],
            [-w2,  h2, -d2],
            [-w2, -h2,  d2],
            [ w2, -h2,  d2],
            [ w2,  h2,  d2],
            [-w2,  h2,  d2],
        ]
        self.edges = [
            (0,1),(1,2),(2,3),(3,0),
            (4,5),(5,6),(6,7),(7,4),
            (0,4),(1,5),(2,6),(3,7),
        ]

        # rotation state
        self.vx = 0.0   # W/S → pitch (sumbu X)
        self.vz = 0.0   # A/D → roll  (sumbu Z)
        self.ang_x = 0.0
        self.ang_z = math.radians(20)  # initial tilt

        master.bind('<KeyPress>',  self.on_keypress)
        master.bind('<KeyRelease>', self.on_keyrelease)

        self.last_time = time.time()
        self.animate()

    def project(self, x, y, z):
        """Orthographic projection + center at (300,300)."""
        return 300 + x, 300 - z

    def rotate(self, x, y, z):
        """Rotate point around X then Z."""
        # about X
        cx, sx = math.cos(self.ang_x), math.sin(self.ang_x)
        y, z = y*cx - z*sx, y*sx + z*cx
        # about Z
        cz, sz = math.cos(self.ang_z), math.sin(self.ang_z)
        x, y = x*cz - y*sz, x*sz + y*cz
        return x, y, z

    def on_keypress(self, e):
        sp = 0.03
        if e.keysym == 'w':   self.vx =  sp
        elif e.keysym == 's': self.vx = -sp
        elif e.keysym == 'a': self.vz =  sp
        elif e.keysym == 'd': self.vz = -sp

    def on_keyrelease(self, e):
        if e.keysym in ('w','s'): self.vx = 0
        if e.keysym in ('a','d'): self.vz = 0

    def animate(self):
        now = time.time()
        dt = now - self.last_time
        self.last_time = now

        # update angles
        self.ang_x += self.vx * dt * 30
        self.ang_z += self.vz * dt * 30

        self.canvas.delete('all')

        # origin in screen coords
        ox, oy = self.project(0,0,0)

        # 1) draw static Z-axis (blue, vertical up)
        zx, zy = ox, oy - self.axis_length
        self.canvas.create_line(ox, oy, zx, zy, fill='blue', width=2, arrow=tk.LAST)

        # 2) draw rotating X-axis (red)
        x_end = self.rotate(self.axis_length, 0, 0)
        xx, xy = self.project(*x_end)
        self.canvas.create_line(ox, oy, xx, xy, fill='red', width=2, arrow=tk.LAST)

        # 3) draw the block
        pts = [ self.project(*self.rotate(x,y,z)) for x,y,z in self.vertices ]
        for i,j in self.edges:
            x1,y1 = pts[i]
            x2,y2 = pts[j]
            self.canvas.create_line(x1,y1, x2,y2, fill='black', width=2)

        # schedule next frame
        self.master.after(33, self.animate)

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Wireframe Block + Mixed Axes")
    WireframeBlockMixedAxes(root, width=250, height=120, depth=180)
    root.mainloop()
