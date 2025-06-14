import tkinter as tk
import math
import time

class SolidBlockMixedAxes:
    def __init__(self, master, width=200, height=100, depth=150):
        self.master = master
        self.canvas = tk.Canvas(master, width=600, height=600, bg='white')
        self.canvas.pack()

        # half-sizes
        w2, h2, d2 = width/2, height/2, depth/2
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
        # edges (for optional outline)
        self.edges = [
            (0,1),(1,2),(2,3),(3,0),
            (4,5),(5,6),(6,7),(7,4),
            (0,4),(1,5),(2,6),(3,7),
        ]
        # faces for solid fill
        self.faces = [
            (0,1,2,3),  # back
            (4,5,6,7),  # front
            (0,1,5,4),  # bottom
            (2,3,7,6),  # top
            (1,2,6,5),  # right
            (0,3,7,4),  # left
        ]
        # unique colors per face
        self.colors = ['red', 'green', 'blue', 'yellow', 'cyan', 'magenta']

        # rotation state
        self.vx = 0.0   # W/S → pitch around X
        self.vz = 0.0   # A/D → roll around Z
        self.ang_x = 0.0
        self.ang_z = math.radians(20)  # initial tilt

        master.bind('<KeyPress>',  self.on_keypress)
        master.bind('<KeyRelease>', self.on_keyrelease)

        self.last_time = time.time()
        self.animate()

    def project(self, x, y, z):
        cx, cy = 300, 300
        return cx + x, cy - z

    def rotate(self, x, y, z):
        # rotate about X
        cx, sx = math.cos(self.ang_x), math.sin(self.ang_x)
        y, z = y*cx - z*sx, y*sx + z*cx
        # rotate about Z
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

        # update rotation angles
        self.ang_x += self.vx * dt * 30
        self.ang_z += self.vz * dt * 30

        # clear canvas
        self.canvas.delete('all')

        # transform all vertices
        transformed = [self.rotate(x, y, z) for x, y, z in self.vertices]

        # depth-sort faces by average Y (camera looks along +Y)
        order = []
        for idx, face in enumerate(self.faces):
            avg_y = sum(transformed[i][1] for i in face) / 4.0
            order.append((avg_y, idx))
        order.sort()

        # draw faces (solid)
        for _, idx in order:
            pts2d = [self.project(*transformed[i]) for i in self.faces[idx]]
            coords = [c for p in pts2d for c in p]
            self.canvas.create_polygon(coords, fill=self.colors[idx], outline='black')

        # draw edges on top
        for i, j in self.edges:
            x1, y1 = self.project(*transformed[i])
            x2, y2 = self.project(*transformed[j])
            self.canvas.create_line(x1, y1, x2, y2, fill='black', width=1)

        # schedule next frame
        self.master.after(33, self.animate)

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Menggunakan Warna Setiap Sisi Baloknya")
    SolidBlockMixedAxes(root, width=250, height=120, depth=180)
    root.mainloop()
