import tkinter as tk
from pathlib import Path
from PIL import Image, ImageTk
import os
import sys

# Определяем путь к папке, где находится сам .exe или .py
if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(os.path.dirname(os.path.abspath(__file__)))

ICON_DIR = BASE_DIR / "тест"

def create_file(ext):
    name = name_entry.get().strip()
    if not name:
        status.config(text="Введите имя!", fg="red")
        return
    
    path = Path.home() / "Desktop" / f"{name}{ext}"
    try:
        path.touch()
        status.config(text=f"Создан: {name}{ext}", fg="green")
    except Exception as e:
        status.config(text=f"Ошибка: {e}", fg="red")

root = tk.Tk()
root.title("File Creator")
root.geometry("450x350")

tk.Label(root, text="Введите имя файла (без расширения):").pack(pady=10)
name_entry = tk.Entry(root, width=40)
name_entry.pack()

# Контейнер для кнопок
frame = tk.Frame(root)
frame.pack(pady=20)

# Список форматов и их иконок
buttons_info = [
    (".txt", "txt.png", "Текст"),
    (".bat", "bat.png", "Скрипт"),
    (".html", "html.png", "Web"),
    (".js", "js.png", "JS"),
    (".lua", "lua.png", "Lua")
]

for ext, icon_name, label_text in buttons_info:
    # Создаем фрейм для кнопки и надписи
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
        # Кнопка без иконки, если файла нет
        tk.Button(btn_container, text=ext, width=5, command=lambda e=ext: create_file(e)).pack()
    
    # Добавляем название под иконкой
    tk.Label(btn_container, text=label_text, font=("Arial", 8)).pack()

status = tk.Label(root, text="Готов к работе", fg="gray")
status.pack(pady=20)

root.mainloop()