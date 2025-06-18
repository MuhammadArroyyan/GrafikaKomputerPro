import tkinter as tk
import math

class Wireframe3DBox:
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(master, width=600, height=600, bg="white")
        self.canvas.pack()

        # Sudut rotasi awal
        self.rot_x = -4.9
        self.rot_y = 2.9

        # Dimensi balok
        width = 200
        height = 160
        depth = 120

        # Vertices balok (8 titik sudut)
        self.vertices = [
            [-width/2, -height/2, -depth/2],  # 0: belakang kiri bawah
            [width/2, -height/2, -depth/2],   # 1: belakang kanan bawah
            [width/2, height/2, -depth/2],    # 2: belakang kanan atas
            [-width/2, height/2, -depth/2],   # 3: belakang kiri atas
            [-width/2, -height/2, depth/2],   # 4: depan kiri bawah
            [width/2, -height/2, depth/2],    # 5: depan kanan bawah
            [width/2, height/2, depth/2],     # 6: depan kanan atas
            [-width/2, height/2, depth/2]     # 7: depan kiri atas
        ]
        
        # Edges (garis-garis yang menghubungkan vertices)
        self.edges = [
            # Sisi belakang
            [0, 1], [1, 2], [2, 3], [3, 0],
            # Sisi depan
            [4, 5], [5, 6], [6, 7], [7, 4],
            # Sisi penghubung depan-belakang
            [0, 4], [1, 5], [2, 6], [3, 7]
        ]
       
        # Faces untuk hidden surface removal (tidak digunakan dalam wireframe)
        self.faces = [
            [0, 3, 2, 1],  # belakang
            [4, 5, 6, 7],  # depan  
            [0, 4, 7, 3],  # kiri
            [1, 2, 6, 5],  # kanan
            [3, 7, 6, 2],  # atas
            [0, 1, 5, 4]   # bawah
        ]

        # Kontrol keyboard
        self.master.bind("<KeyPress>", self.on_key)

        # Focus the canvas for keyboard input
        self.canvas.focus_set()

        # Render pertama
        self.render()

    def multiply_matrix(self, point, rot_x, rot_y):
        x, y, z = point

        # Rotasi X
        cos_x = math.cos(rot_x)
        sin_x = math.sin(rot_x)
        y1 = y * cos_x - z * sin_x
        z1 = y * sin_x + z * cos_x

        # Rotasi Y
        cos_y = math.cos(rot_y)
        sin_y = math.sin(rot_y)
        x2 = x * cos_y + z1 * sin_y
        z2 = -x * sin_y + z1 * cos_y

        return [x2, y1, z2]

    def project_3d(self, point):
        x, y = point[0], point[1]
        return x + 300, -y + 300  

    def draw_line(self, p1, p2):
        self.canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill="black", width=2)

    def render(self):
        self.canvas.delete("all")

        transformed = [self.multiply_matrix(v, self.rot_x, self.rot_y) for v in self.vertices]
        projected = [self.project_3d(p) for p in transformed]

        for edge in self.edges:
            p1 = projected[edge[0]]
            p2 = projected[edge[1]]
            self.draw_line(p1, p2)

    def on_key(self, event):
        step = 0.1
        key = event.keysym.lower()

        if key == 'a':
            self.rot_y -= step
        elif key == 'd':
            self.rot_y += step
        elif key == 'w':
            self.rot_x += step
        elif key == 's':
            self.rot_x -= step

        self.render()

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Wireframe")
    app = Wireframe3DBox(root)
    root.mainloop()