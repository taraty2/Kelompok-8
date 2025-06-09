import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pandas as pd

# Baca decision tree dari Excel
excel_path = "decision_tree_fmipa_unesa.xlsx"
df_tree = pd.read_excel(excel_path)
df_tree.set_index("ID", inplace=True)

class JurusanDecisionTreeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rekomendasi Jurusan Berdasarkan Minat")

        self.root.state('zoomed')
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        # ===== Halaman Awal =====
        self.frame_awal = tk.Frame(root, width=self.screen_width, height=self.screen_height)
        self.frame_awal.pack_propagate(False)

        bg_image = Image.open("Merah Kuning Profesional Zoom Latar Belakang.png")
        bg_image = bg_image.resize((self.screen_width, self.screen_height), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(bg_image)

        self.bg_label = tk.Label(self.frame_awal, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.start_button = tk.Button(
            self.frame_awal, text="Mencari Jurusan", font=("Arial", 22, "bold"),
            bg="white", fg="darkred", padx=30, pady=10, command=self.start_tree
        )
        self.start_button.place(relx=0.5, rely=0.5, anchor="center")

        self.frame_awal.pack()

        self.current_id = 1  # mulai dari root decision tree

    def start_tree(self):
        self.frame_awal.pack_forget()
        self.show_question(self.current_id)

    def show_question(self, node_id):
        node = df_tree.loc[node_id]
        self.clear_screen()

        frame = tk.Frame(self.root, width=self.screen_width, height=self.screen_height)
        frame.pack_propagate(False)
        frame.pack()

        bg_image = Image.open("Merah Kuning Profesional Zoom Latar Belakang (1).png")
        bg_image = bg_image.resize((self.screen_width, self.screen_height), Image.Resampling.LANCZOS)
        self.bg_photo_q = ImageTk.PhotoImage(bg_image)

        bg_label = tk.Label(frame, image=self.bg_photo_q)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        label = tk.Label(frame, text=node["Pertanyaan"], font=("Arial", 20), wraplength=1000, bg="white")
        label.place(relx=0.5, rely=0.3, anchor="center")

        if pd.isna(node['Rekomendasi']):
            btn_yes = tk.Button(frame, text="Ya", font=("Arial", 18), width=15,
                                 command=lambda: self.show_question(int(node["Jika_Ya"])))
            btn_yes.place(relx=0.4, rely=0.5, anchor="center")

            btn_no = tk.Button(frame, text="Tidak", font=("Arial", 18), width=15,
                                command=lambda: self.show_question(int(node["Jika_Tidak"])))
            btn_no.place(relx=0.6, rely=0.5, anchor="center")
        else:
            result_label = tk.Label(frame, text=f"Rekomendasi Jurusan:{node['Rekomendasi']}",
                                     font=("Arial", 22, "bold"), bg="white", wraplength=1000, justify="center")
            result_label.place(relx=0.5, rely=0.5, anchor="center")

            btn_kembali = tk.Button(frame, text="Ulangi", font=("Arial", 16),
                                     command=self.restart_app)
            btn_kembali.place(relx=0.5, rely=0.65, anchor="center")

        self.active_frame = frame

    def restart_app(self):
        self.active_frame.pack_forget()
        self.frame_awal.pack()
        self.current_id = 1

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.pack_forget()


if __name__ == "__main__":
    root = tk.Tk()
    app = JurusanDecisionTreeApp(root)
    root.mainloop()