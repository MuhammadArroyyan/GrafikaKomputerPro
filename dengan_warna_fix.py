import tkinter as tk
import math

class Solid3DBox:
    def __init__(self, master):
        # inisialisasi window dan canvas putih dengan ukuran 800x600
        self.master = master
        self.canvas = tk.Canvas(master, width=800, height=600, bg="white")
        self.canvas.pack()
        
        # sudut rotasi awal: miring sedikit dari atas dan kanan
        self.rot_x = -4.9
        self.rot_y = 2.9
        self.rot_z = 0
        
        # dimensi balok (lebar, tinggi, kedalaman)
        width, height, depth = 180, 140, 120
        
        # titik-titik sudut balok (8 vertices)
        # tiap titik: [x, y, z]
        self.vertices = [
            [-width/2, -height/2, -depth/2],  # belakang kiri bawah
            [ width/2, -height/2, -depth/2],  # belakang kanan bawah
            [ width/2,  height/2, -depth/2],  # belakang kanan atas
            [-width/2,  height/2, -depth/2],  # belakang kiri atas
            [-width/2, -height/2,  depth/2],  # depan kiri bawah
            [ width/2, -height/2,  depth/2],  # depan kanan bawah
            [ width/2,  height/2,  depth/2],  # depan kanan atas
            [-width/2,  height/2,  depth/2],  # depan kiri atas
        ]
        
        # daftar pasangan indeks untuk menggambar garis antar vertices
        self.edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),  # sisi belakang
            (4, 5), (5, 6), (6, 7), (7, 4),  # sisi depan
            (0, 4), (1, 5), (2, 6), (3, 7),  # garis penghubung depan-belakang
        ]
        
        # daftar face (4 vertices) untuk menyembunyikan garis yang tidak terlihat
        # urutan counterclockwise agar normal menghadap keluar
        self.faces = [
            [0, 3, 2, 1],  # belakang
            [4, 5, 6, 7],  # depan  
            [0, 4, 7, 3],  # kiri
            [1, 2, 6, 5],  # kanan
            [3, 7, 6, 2],  # atas
            [0, 1, 5, 4],  # bawah
        ]
        
        # hubungkan tombol keyboard ke fungsi on_key_press
        self.master.bind("<KeyPress>", self.on_key_press)
        
        # mulai dengan menggambar sekali
        self.render()
        
        # agar canvas bisa menerima input keyboard
        self.canvas.focus_set()
    
    def multiply_matrix(self, point, rot_x, rot_y, rot_z):
        # rotasi titik 3D sesuai sudut X, Y, Z
        x, y, z = point
        
        # rotasi sekitar sumbu X (pitch)
        cos_x, sin_x = math.cos(rot_x), math.sin(rot_x)
        y1 = y * cos_x - z * sin_x
        z1 = y * sin_x + z * cos_x
        
        # rotasi sekitar sumbu Y (yaw)
        cos_y, sin_y = math.cos(rot_y), math.sin(rot_y)
        x2 = x * cos_y + z1 * sin_y
        z2 = -x * sin_y + z1 * cos_y
        
        # rotasi sekitar sumbu Z (roll)
        cos_z, sin_z = math.cos(rot_z), math.sin(rot_z)
        x3 = x2 * cos_z - y1 * sin_z
        y3 = x2 * sin_z + y1 * cos_z
        
        return [x3, y3, z2]
    
    def project_3d(self, point):
        # proyeksi ortografis sederhana: geser ke tengah canvas
        x = point[0] + 400  # lebar/2
        y = -point[1] + 300 # tinggi/2, dibalik agar positif ke atas
        return [x, y]
    
    def calculate_normal(self, face, verts):
        # hitung normal face via cross product vektor (v1->v2) x (v1->v3)
        v1 = verts[face[0]]
        v2 = verts[face[1]]
        v3 = verts[face[2]]
        
        vec1 = [v2[i] - v1[i] for i in range(3)]
        vec2 = [v3[i] - v1[i] for i in range(3)]
        
        normal = [
            vec1[1]*vec2[2] - vec1[2]*vec2[1],
            vec1[2]*vec2[0] - vec1[0]*vec2[2],
            vec1[0]*vec2[1] - vec1[1]*vec2[0]
        ]
        return normal
    
    def is_face_visible(self, face, verts):
        # hanya gambar face yang normal-nya menghadap kamera (z>0)
        normal = self.calculate_normal(face, verts)
        return normal[2] > 0
    
    def is_edge_visible(self, edge, visible_faces):
        # edge terlihat jika merupakan sisi salah satu face yang terlihat
        for fi in visible_faces:
            face = self.faces[fi]
            # pastikan kedua titik edge ada di face ini dan berdekatan
            for i in range(len(face)):
                j = (i + 1) % len(face)
                if (edge[0] == face[i] and edge[1] == face[j]) or \
                   (edge[1] == face[i] and edge[0] == face[j]):
                    return True
        return False
    
    def render(self):
        # bersihkan canvas
        self.canvas.delete("all")
        
        # transform semua vertices
        tverts = [self.multiply_matrix(v, self.rot_x, self.rot_y, self.rot_z)
                  for v in self.vertices]
        # proyeksikan ke 2D
        pverts = [self.project_3d(v) for v in tverts]
        
        # cari face yang terlihat
        visible = [i for i,f in enumerate(self.faces)
                   if self.is_face_visible(f, tverts)]
        
        # gambar hanya edge yang termasuk di face terlihat
        for edge in self.edges:
            if self.is_edge_visible(edge, visible):
                p1 = pverts[edge[0]]
                p2 = pverts[edge[1]]
                self.canvas.create_line(p1[0], p1[1], p2[0], p2[1], width=2)
    
    def on_key_press(self, event):
        # ubah sudut rotasi sesuai tombol
        step = 0.1
        k = event.keysym.lower()
        
        if k == 'a':        # putar kiri/kanan
            self.rot_y -= step
        elif k == 'd':
            self.rot_y += step
        elif k == 'w':      # putar atas/bawah
            self.rot_x += step
        elif k == 's':
            self.rot_x -= step
        
        # render ulang setelah perubahan sudut
        self.render()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Tertutup")
    app = Solid3DBox(root)
    root.mainloop()