import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import random
import os
from pathlib import Path

BASE_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
ICON_DIR = BASE_DIR / "тест"

# Шаблоны кода
LANG_TEMPLATES = {
    "Python": (".py", 'print("Hello World")\ninput("Нажми Enter...")'),
    "Batch": (".bat", '@echo off\necho Hello World\npause'),
    "VBScript": (".vbs", 'MsgBox "Hello World"')
}

def create_file(ext, name_val=None, is_prog=False):
    name = name_val.get().strip() if name_val else name_entry.get().strip()
    if not name:
        status.config(text="Ошибка: введите имя!", fg="#FF5555")
        return
    
    desktop_path = Path.home() / "Desktop"
    
    if is_prog:
        lang = lang_combo.get()
        ext, content = LANG_TEMPLATES.get(lang, (".py", ""))
        
        # 1. Создаем файл исходника (например, .py)
        source_path = desktop_path / f"{name}{ext}"
        with open(source_path, "w", encoding="utf-8") as f: f.write(content)
        
        # 2. Создаем "exe" (копию исходника с расширением .exe)
        exe_path = desktop_path / f"{name}.exe"
        with open(exe_path, "w", encoding="utf-8") as f: f.write(content)
            
        status.config(text=f"Создано: {name}.exe и {name}{ext}", fg="#55FF55")
    else:
        file_path = desktop_path / f"{name}{ext}"
        with open(file_path, "w", encoding="utf-8") as f: pass
        status.config(text=f"Создан: {name}{ext}", fg="#55FF55")

root = tk.Tk()
root.title("File Creator Pro")
root.geometry("450x400")

def add_bg(parent):
    bg_path = ICON_DIR / "bg.png"
    if bg_path.exists():
        img = Image.open(bg_path).resize((450, 400))
        photo = ImageTk.PhotoImage(img)
        lbl = tk.Label(parent, image=photo, bg="black")
        lbl.place(x=0, y=0, relwidth=1, relheight=1)
        lbl.image = photo

notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

# --- Вкладка 1 ---
tab1 = tk.Frame(notebook, bg="black")
notebook.add(tab1, text="Создание файлов")
add_bg(tab1)

canvas = tk.Canvas(tab1, bg="black", highlightthickness=0)
canvas.place(x=0, y=0, relwidth=1, relheight=1)
def draw_matrix():
    x = random.randint(0, 430)
    txt = canvas.create_text(x, -20, text=random.choice("01"), fill="#00FF41", font=("Courier", 12))
    def move():
        canvas.move(txt, 0, 5)
        if canvas.coords(txt)[1] < 400: canvas.after(50, move)
        else: canvas.delete(txt)
    move()
    canvas.after(300, draw_matrix)
draw_matrix()

name_entry = tk.Entry(tab1, width=40)
name_entry.pack(pady=10)
btn_frame = tk.Frame(tab1, bg="black")
btn_frame.pack()

buttons = [(".txt", "txt.png", "Текст"), (".bat", "bat.png", "BAT"), 
           (".html", "html.png", "HTML"), (".js", "js.png", "JS"), (".lua", "lua.png", "Lua")]
for ext, icon, label in buttons:
    f = tk.Frame(btn_frame, bg="black")
    f.pack(side="left", padx=5)
    if (ICON_DIR / icon).exists():
        img = Image.open(ICON_DIR / icon).resize((35, 35))
        photo = ImageTk.PhotoImage(img)
        btn = tk.Button(f, image=photo, command=lambda e=ext: create_file(e), borderwidth=0)
        btn.image = photo
        btn.pack()
    tk.Label(f, text=label, bg="black", fg="white", font=("Arial", 7)).pack()

status = tk.Label(tab1, text="Система активна", fg="#00FF41", bg="black")
status.pack(pady=10)

# --- Вкладка 2 ---
tab2 = tk.Frame(notebook, bg="black")
notebook.add(tab2, text="Создать программу")
add_bg(tab2)
tk.Label(tab2, text="Введите имя программы:", fg="white", bg="black").pack(pady=5)
prog_entry = tk.Entry(tab2, width=40)
prog_entry.pack()
tk.Label(tab2, text="Выберите язык:", fg="white", bg="black").pack(pady=10)
lang_combo = ttk.Combobox(tab2, values=["Python", "Batch", "VBScript"], state="readonly")
lang_combo.set("Python")
lang_combo.pack()
tk.Button(tab2, text="Создать программу", command=lambda: create_file(None, prog_entry, is_prog=True)).pack(pady=20)

root.mainloop()