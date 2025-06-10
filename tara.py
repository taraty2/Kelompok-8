import tkinter as tk
from PIL import Image, ImageTk
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder

# Baca dataset dari Excel
df = pd.read_excel("jurusan.xlsx")

# Label encoding untuk kolom kategori
le_minat = LabelEncoder()
le_subminat = LabelEncoder()
le_jurusan = LabelEncoder()

# Encode kolom
df['Minat_enc'] = le_minat.fit_transform(df['Minat'])
df['MinatSpesifik_enc'] = le_subminat.fit_transform(df['Minat Spesifik'])
df['Jurusan_enc'] = le_jurusan.fit_transform(df['Jurusan'])

# Model training
X = df[['Minat_enc', 'MinatSpesifik_enc']]
y = df['Jurusan_enc']
model = DecisionTreeClassifier()
model.fit(X, y)

# Detail jurusan
grouped = df.groupby("Jurusan").agg({
    "Deskripsi": lambda x: "\n\n".join(x.unique()),
    "Prospek Kerja": lambda x: "\n\n".join(x.unique()),
    "Akreditasi": lambda x: ", ".join(x.unique())})
jurusan_detail = grouped.to_dict(orient="index")

class JurusanDecisionTreeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rekomendasi Jurusan Berdasarkan Minat")
        self.root.state('zoomed')
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        self.minat = None
        self.minat_spesifik = None
        self.pred_jurusan = None

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
            bg="white", fg="darkred", padx=30, pady=10, command=self.start_questions
        )
        self.start_button.place(relx=0.5, rely=0.5, anchor="center")

        self.frame_awal.pack()
        self.label = tk.Label(root, text="", font=("Arial", 16), wraplength=800)
        self.options_frame = tk.Frame(root)

    def start_questions(self):
        self.frame_awal.pack_forget()
        self.frame_pertanyaan = tk.Frame(self.root, width=self.screen_width, height=self.screen_height)
        self.frame_pertanyaan.pack_propagate(False)
        self.frame_pertanyaan.pack()

        bg_image2 = Image.open("Merah Kuning Profesional Zoom Latar Belakang (1).png")
        bg_image2 = bg_image2.resize((self.screen_width, self.screen_height), Image.Resampling.LANCZOS)
        self.bg_photo2 = ImageTk.PhotoImage(bg_image2)

        self.bg_label2 = tk.Label(self.frame_pertanyaan, image=self.bg_photo2)
        self.bg_label2.place(x=0, y=0, relwidth=1, relheight=1)

        self.options_frame = tk.Frame(self.frame_pertanyaan)
        self.options_frame.place(relx=0.5, rely=0.35, anchor="n")

        self.show_minat_options()

    def clear_options(self):
        for widget in self.options_frame.winfo_children():
            widget.destroy()

    def show_minat_options(self):
        self.clear_options()
        minat_list = sorted(df["Minat"].unique())
        for m in minat_list:
            btn = tk.Button(self.options_frame, text=m, width=50, font=("Arial", 16), command=lambda m=m: self.select_minat(m))
            btn.pack(pady=5)

    def select_minat(self, minat):
        self.minat = minat
        self.show_minat_spesifik_options()

    def show_minat_spesifik_options(self):
        self.frame_pertanyaan.pack_forget()
        self.frame_minat_spesifik = tk.Frame(self.root, width=self.screen_width, height=self.screen_height)
        self.frame_minat_spesifik.pack_propagate(False)
        self.frame_minat_spesifik.pack()

        bg_image_sub = Image.open("Merah Kuning Profesional Zoom Latar Belakang (6).png")
        bg_image_sub = bg_image_sub.resize((self.screen_width, self.screen_height), Image.Resampling.LANCZOS)
        self.bg_photo_sub = ImageTk.PhotoImage(bg_image_sub)

        self.bg_label_sub = tk.Label(self.frame_minat_spesifik, image=self.bg_photo_sub)
        self.bg_label_sub.place(x=0, y=0, relwidth=1, relheight=1)

        self.options_frame = tk.Frame(self.frame_minat_spesifik)
        self.options_frame.place(relx=0.5, rely=0.4, anchor="n")

        sub_list = sorted(df[df["Minat"] == self.minat]["Minat Spesifik"].unique())
        for s in sub_list:
            btn = tk.Button(self.options_frame, text=s, width=50, font=("Arial", 16),
                            command=lambda s=s: self.select_minat_spesifik(s))
            btn.pack(pady=5)

    def select_minat_spesifik(self, minat_spesifik):
        self.minat_spesifik = minat_spesifik
        self.predict_jurusan()

    def predict_jurusan(self):
        minat_enc = le_minat.transform([self.minat])[0]
        subminat_enc = le_subminat.transform([self.minat_spesifik])[0]
        X_input = pd.DataFrame([[minat_enc, subminat_enc]], columns=['Minat_enc', 'MinatSpesifik_enc'])
        pred_encoded = model.predict(X_input)[0]
        self.pred_jurusan = le_jurusan.inverse_transform([pred_encoded])[0]
        self.show_result()

    def show_result(self):
        self.frame_minat_spesifik.pack_forget()
        self.frame_result = tk.Frame(self.root, width=self.screen_width, height=self.screen_height)
        self.frame_result.pack_propagate(False)
        self.frame_result.pack()

        bg_image3 = Image.open("Merah Kuning Profesional Zoom Latar Belakang (5).png")
        bg_image3 = bg_image3.resize((self.screen_width, self.screen_height), Image.Resampling.LANCZOS)
        self.bg_photo_result = ImageTk.PhotoImage(bg_image3)
        bg_label = tk.Label(self.frame_result, image=self.bg_photo_result)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        btn = tk.Button(self.frame_result, text=self.pred_jurusan, width=50, font=("Arial", 18),
                        command=lambda: self.show_detail(self.pred_jurusan))
        btn.place(relx=0.5, rely=0.4, anchor="center")

        self.detail_label = tk.Label(self.frame_result, text="", font=("Arial", 14), bg="white", justify="left",
                                     wraplength=1000, anchor="nw", relief="groove", bd=2, padx=10, pady=10)
        self.detail_label.place_forget()

    def show_detail(self, jurusan):
        row = jurusan_detail[jurusan]
        detail = (
            f"Jurusan: {jurusan}\n\n"
            f"Deskripsi: {row['Deskripsi']}\n\n"
            f"Prospek Kerja: {row['Prospek Kerja']}\n\n"
            f"Akreditasi: {row['Akreditasi']}"
        )
        self.detail_label.config(text=detail)
        self.detail_label.place(relx=0.5, rely=0.5, anchor="n")

def print_tree_structure():
    print("Struktur Pohon Keputusan Berdasarkan Excel:\n")
    grouped = df.groupby(["Minat", "Minat Spesifik"])
    for (minat, minat_spesifik), group in grouped:
        print(f"Minat: {minat}")
        print(f"Minat Spesifik: {minat_spesifik}")
        for jurusan in group["Jurusan"]:
            print(f"    - {jurusan}")
        print()

if __name__ == "__main__":
    print_tree_structure()
    root = tk.Tk()
    app = JurusanDecisionTreeApp(root)
    root.mainloop()
