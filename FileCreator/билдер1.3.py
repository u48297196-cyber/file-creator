import tkinter as tk
from tkinter import ttk
from pathlib import Path
from PIL import Image, ImageTk, ImageDraw
import os
import random

# Пути
BASE_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
ICON_DIR = BASE_DIR / "тест"

def create_file(ext):
    name = name_entry.get().strip()
    if not name:
        status.config(text="Ошибка: введите имя!", fg="#FF5555")
        return
    desktop_path = Path.home() / "Desktop"
    file_path = desktop_path / f"{name}{ext}"
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            pass 
        status.config(text=f"Создан: {name}{ext}", fg="#55FF55")
    except Exception as e:
        status.config(text=f"Ошибка: {e}", fg="#FF5555")

root = tk.Tk()
root.title("File Creator Pro")
root.geometry("450x400")

# --- Фон с хакерским эффектом ---
bg_path = ICON_DIR / "bg.png"
if bg_path.exists():
    img = Image.open(bg_path).resize((450, 400))
    # Рисуем "цифры" прямо на картинке фона
    draw = ImageDraw.Draw(img)
    for _ in range(60): # Количество цифр
        x = random.randint(0, 450)
        y = random.randint(0, 400)
        draw.text((x, y), random.choice("01"), fill="#00FF41")
    
    bg_photo = ImageTk.PhotoImage(img)
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    bg_label.image = bg_photo

# --- Интерфейс ---
bg_color = "#000000"
fg_color = "#E0E0E0"

notebook = ttk.Notebook(root)
notebook.pack(pady=10, fill='both', expand=True)

# Вкладка 1
tab1 = tk.Frame(notebook, bg=bg_color)
notebook.add(tab1, text="Создание файлов")

tk.Label(tab1, text="Имя файла:", bg=bg_color, fg=fg_color).pack(pady=5)
name_entry = tk.Entry(tab1, width=40, bg="#101010", fg=fg_color, insertbackground=fg_color)
name_entry.pack()

frame = tk.Frame(tab1, bg=bg_color)
frame.pack(pady=10)

buttons_info = [(".txt", "txt.png", "Текст"), (".bat", "bat.png", "BAT"), 
                (".html", "html.png", "HTML"), (".js", "js.png", "JS"), (".lua", "lua.png", "Lua")]

for ext, icon_name, label_text in buttons_info:
    btn_container = tk.Frame(frame, bg=bg_color)
    btn_container.pack(side="left", padx=5)
    icon_path = ICON_DIR / icon_name
    
    # Кнопка с иконкой
    if icon_path.exists():
        img = Image.open(icon_path).resize((35, 35))
        photo = ImageTk.PhotoImage(img)
        btn = tk.Button(btn_container, image=photo, bg=bg_color, borderwidth=0, command=lambda e=ext: create_file(e))
        btn.image = photo
        btn.pack()
    else:
        tk.Button(btn_container, text=ext, command=lambda e=ext: create_file(e)).pack()
    
    tk.Label(btn_container, text=label_text, bg=bg_color, fg=fg_color, font=("Arial", 7)).pack()

status = tk.Label(tab1, text="Готов к работе", fg="#00FF41", bg=bg_color)
status.pack(pady=10)

# Вкладка 2
tab2 = tk.Frame(notebook, bg=bg_color)
notebook.add(tab2, text="Создать программу")
tk.Label(tab2, text="Выберите язык:", bg=bg_color, fg=fg_color).pack(pady=20)
lang_combo = ttk.Combobox(tab2, values=["Python", "Batch", "VBScript"], state="readonly")
lang_combo.pack()

root.mainloop()