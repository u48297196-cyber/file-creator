import tkinter as tk
from tkinter import ttk
from pathlib import Path
from PIL import Image, ImageTk
import os

# Пути
BASE_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
ICON_DIR = BASE_DIR / "тест"

def add_bg(parent):
    bg_path = ICON_DIR / "bg.png"
    if bg_path.exists():
        img = Image.open(bg_path).resize((450, 400))
        bg_photo = ImageTk.PhotoImage(img)
        lbl = tk.Label(parent, image=bg_photo)
        lbl.place(x=0, y=0, relwidth=1, relheight=1)
        lbl.image = bg_photo
        lbl.lower()

def create_file(ext):
    name = name_entry.get().strip()
    if not name:
        status.config(text="Ошибка: введите имя!", fg="red")
        return
    desktop_path = Path.home() / "Desktop"
    file_path = desktop_path / f"{name}{ext}"
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            pass 
        status.config(text=f"Создан: {name}{ext}", fg="green")
    except Exception as e:
        status.config(text=f"Ошибка: {e}", fg="red")

root = tk.Tk()
root.title("File Creator Pro")
root.geometry("450x400")

# Вкладки
notebook = ttk.Notebook(root)
notebook.pack(pady=10, fill='both', expand=True)

# Вкладка 1
tab1 = ttk.Frame(notebook)
notebook.add(tab1, text="Создание файлов")
add_bg(tab1) # Добавляем фон в первую вкладку

tk.Label(tab1, text="Имя файла:", bg="white").pack(pady=5)
name_entry = tk.Entry(tab1, width=40)
name_entry.pack()
frame = tk.Frame(tab1, bg="white")
frame.pack(pady=10)

buttons_info = [(".txt", "txt.png", "Текст"), (".bat", "bat.png", "BAT"), 
                (".html", "html.png", "HTML"), (".js", "js.png", "JS"), (".lua", "lua.png", "Lua")]

for ext, icon_name, label_text in buttons_info:
    btn_container = tk.Frame(frame, bg="white")
    btn_container.pack(side="left", padx=5)
    icon_path = ICON_DIR / icon_name
    if icon_path.exists():
        img = Image.open(icon_path).resize((35, 35))
        photo = ImageTk.PhotoImage(img)
        btn = tk.Button(btn_container, image=photo, command=lambda e=ext: create_file(e))
        btn.image = photo
        btn.pack()
    else:
        tk.Button(btn_container, text=ext, command=lambda e=ext: create_file(e)).pack()
    tk.Label(btn_container, text=label_text, bg="white", font=("Arial", 7)).pack()

status = tk.Label(tab1, text="Готов к работе", fg="blue", bg="white")
status.pack(pady=10)

# Вкладка 2
tab2 = ttk.Frame(notebook)
notebook.add(tab2, text="Создать программу")
add_bg(tab2) # Добавляем фон во вторую вкладку

tk.Label(tab2, text="Выберите язык:", bg="white").pack(pady=20)
lang_combo = ttk.Combobox(tab2, values=["Python", "Batch", "VBScript"], state="readonly")
lang_combo.pack()

root.mainloop()