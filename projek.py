import tkinter as tk
from tkinter import messagebox
import csv

# Fungsi untuk membaca CSV dan membangun tree
def build_tree_from_csv(filename):
    tree = {}
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            minat = row["Minat"]
            kategori = row["Kategori"]
            jurusan = row["Jurusan"]
            deskripsi = row["Deskripsi"]
            prospek = row["Prospek Kerja"]
            akreditasi = row["Akreditasi"]

            tree.setdefault("Apa minat kamu?", {})
            tree["Apa minat kamu?"].setdefault(minat, {})
            tree["Apa minat kamu?"][minat].setdefault("Kategori Program Studi?", {})
            tree["Apa minat kamu?"][minat]["Kategori Program Studi?"].setdefault(kategori, {})
            tree["Apa minat kamu?"][minat]["Kategori Program Studi?"][kategori].setdefault("Jurusan", {})
            tree["Apa minat kamu?"][minat]["Kategori Program Studi?"][kategori]["Jurusan"][jurusan] = {
                "Deskripsi": deskripsi,
                "Prospek Kerja": prospek,
                "Akreditasi": akreditasi
            }
    return tree

class JurusanApp:
    def __init__(self, root, tree):
        self.root = root
        self.root.title("Rekomendasi Jurusan Berdasarkan Minat & Bakat")
        self.current_node = tree
        self.path = []

        self.question_label = tk.Label(root, text="", wraplength=400, font=("Arial", 14))
        self.question_label.pack(pady=20)

        self.options_frame = tk.Frame(root)
        self.options_frame.pack()

        self.display_question()

    def display_question(self):
        # Hapus tombol sebelumnya
        for widget in self.options_frame.winfo_children():
            widget.destroy()

        # Jika sudah di akhir
        if all(k in self.current_node for k in ("Deskripsi", "Prospek Kerja", "Akreditasi")):
            jurusan = self.path[-1][1]
            detail = f"Jurusan: {jurusan}\n\nDeskripsi: {self.current_node['Deskripsi']}\nProspek Kerja: {self.current_node['Prospek Kerja']}\nAkreditasi: {self.current_node['Akreditasi']}"
            messagebox.showinfo("Rekomendasi Jurusan", detail)
            self.root.quit()
            return

        # Tampilkan pertanyaan dan opsi
        if isinstance(self.current_node, dict):
            question = list(self.current_node.keys())[0]
            self.question_label.config(text=question)
            for option in self.current_node[question]:
                button = tk.Button(self.options_frame, text=option, width=40,
                                   command=lambda opt=option: self.select_option(opt))
                button.pack(pady=5)

    def select_option(self, option):
        question = list(self.current_node.keys())[0]
        self.path.append((question, option))
        self.current_node = self.current_node[question][option]
        self.display_question()

# Main program
if __name__ == "__main__":
    root = tk.Tk()
    tree = build_tree_from_csv("jurusan.csv")
    app = JurusanApp(root, tree)
    root.mainloop()


