import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import random
import os
from pathlib import Path

BASE_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
ICON_DIR = BASE_DIR / "тест"

def create_file(ext):
    name = name_entry.get().strip()
    desktop_path = Path.home() / "Desktop"
    file_path = desktop_path / f"{name}{ext}"
    try:
        with open(file_path, "w", encoding="utf-8") as f: pass
        status.config(text=f"Создан: {name}{ext}", fg="#55FF55")
    except Exception as e:
        status.config(text=f"Ошибка: {e}", fg="#FF5555")

root = tk.Tk()
root.title("File Creator Pro")
root.geometry("450x400")
root.configure(bg="black")

# Функция добавления фона в любой контейнер
def add_bg(parent):
    bg_path = ICON_DIR / "bg.png"
    if bg_path.exists():
        img = Image.open(bg_path).resize((450, 400))
        photo = ImageTk.PhotoImage(img)
        lbl = tk.Label(parent, image=photo, bg="black")
        lbl.place(x=0, y=0, relwidth=1, relheight=1)
        lbl.image = photo

# Создаем Notebook
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

# --- Вкладка 1 ---
tab1 = tk.Frame(notebook, bg="black")
notebook.add(tab1, text="Создание файлов")
add_bg(tab1) # Фон в первой вкладке

# Хакерский холст ТОЛЬКО внутри tab1
matrix_canvas = tk.Canvas(tab1, bg="black", highlightthickness=0)
matrix_canvas.place(x=0, y=0, relwidth=1, relheight=1)

def draw_matrix():
    # Создаем падающий символ
    x = random.randint(0, 430)
    text_id = matrix_canvas.create_text(x, -20, text=random.choice("01"), fill="#00FF41", font=("Courier", 12))
    
    def move():
        matrix_canvas.move(text_id, 0, 5)
        pos = matrix_canvas.coords(text_id)
        if pos[1] < 400:
            matrix_canvas.after(50, move)
        else:
            matrix_canvas.delete(text_id)
    move()
    matrix_canvas.after(300, draw_matrix)

draw_matrix()

# Элементы поверх холста
name_entry = tk.Entry(tab1, width=40)
name_entry.pack(pady=20)
tk.Button(tab1, text="Создать .txt", command=lambda: create_file(".txt")).pack()
status = tk.Label(tab1, text="Система активна", fg="#00FF41", bg="black")
status.pack(pady=20)

# --- Вкладка 2 ---
tab2 = tk.Frame(notebook, bg="black")
notebook.add(tab2, text="Создать программу")
add_bg(tab2) # Фон во второй вкладке
tk.Label(tab2, text="Выберите язык:", fg="white", bg="black").pack(pady=20)
ttk.Combobox(tab2, values=["Python", "Batch", "VBScript"]).pack()

root.mainloop()