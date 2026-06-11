import tkinter as tk
from tkinter import ttk
from pathlib import Path
from PIL import Image, ImageTk
import os
import sys

# Определяем путь к папке с иконками
BASE_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
ICON_DIR = BASE_DIR / "тест"

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
        status.config(text=f"Файл {name}{ext} успешно создан!", fg="green")
    except Exception as e:
        status.config(text=f"Ошибка: {e}", fg="red")

root = tk.Tk()
root.title("File Creator Pro")
root.geometry("450x400")

# Создаем систему вкладок
notebook = ttk.Notebook(root)
notebook.pack(pady=10, fill='both', expand=True)

# --- Вкладка 1: Создание файлов ---
tab1 = ttk.Frame(notebook)
notebook.add(tab1, text="Создание файлов")

tk.Label(tab1, text="Имя файла (без расширения):").pack(pady=10)
name_entry = tk.Entry(tab1, width=40)
name_entry.pack()

frame = tk.Frame(tab1)
frame.pack(pady=20)

buttons_info = [
    (".txt", "txt.png", "Текст"),
    (".bat", "bat.png", "BAT"),
    (".html", "html.png", "HTML"),
    (".js", "js.png", "JS"),
    (".lua", "lua.png", "Lua")
]

for ext, icon_name, label_text in buttons_info:
    btn_container = tk.Frame(frame)
    btn_container.pack(side="left", padx=10)
    icon_path = ICON_DIR / icon_name
    
    if icon_path.exists():
        img = Image.open(icon_path).resize((40, 40))
        photo = ImageTk.PhotoImage(img)
        btn = tk.Button(btn_container, image=photo, command=lambda e=ext: create_file(e))
        btn.image = photo 
        btn.pack()
    else:
        tk.Button(btn_container, text=ext, width=5, command=lambda e=ext: create_file(e)).pack()
    tk.Label(btn_container, text=label_text).pack()

status = tk.Label(tab1, text="Готов к работе", fg="blue")
status.pack(pady=10)

# --- Вкладка 2: Создать программу ---
tab2 = ttk.Frame(notebook)
notebook.add(tab2, text="Создать программу")

tk.Label(tab2, text="Выберите язык для создания программы:", font=("Arial", 10)).pack(pady=20)

lang_combo = ttk.Combobox(tab2, values=["Python", "Batch (.bat)", "VBScript (.vbs)"], state="readonly")
lang_combo.pack(pady=10)

tk.Button(tab2, text="Создать структуру программы", command=lambda: status2.config(text="Функция в разработке...")).pack(pady=20)

status2 = tk.Label(tab2, text="", fg="gray")
status2.pack(pady=10)

root.mainloop()