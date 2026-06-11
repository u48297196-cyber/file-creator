import tkinter as tk
from tkinter import ttk
import os
import random
import subprocess
from pathlib import Path
from PIL import Image, ImageTk

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
        with open(desktop_path / f"{name}{ext}", "w", encoding="utf-8") as f: f.write(content)
        with open(desktop_path / f"{name}.exe", "w", encoding="utf-8") as f: f.write(content)
        status.config(text=f"Создано: {name}.exe", fg="#55FF55")
    else:
        with open(desktop_path / f"{name}{ext}", "w", encoding="utf-8") as f: pass
        status.config(text=f"Создан: {name}{ext}", fg="#55FF55")
    refresh_file_list()

def refresh_file_list():
    files = [f for f in os.listdir(Path.home() / "Desktop") if f.endswith(".exe")]
    file_listbox.delete(0, tk.END)
    for f in files: file_listbox.insert(tk.END, f)

def open_location():
    selected = file_listbox.get(tk.ACTIVE)
    if selected:
        path = Path.home() / "Desktop"
        subprocess.Popen(f'explorer /select,"{path / selected}"')

def edit_code():
    selected = file_listbox.get(tk.ACTIVE)
    if selected:
        path = Path.home() / "Desktop" / selected
        os.system(f'notepad "{path}"')

root = tk.Tk()
root.title("File Creator Pro")
root.geometry("450x450")

def add_bg(parent):
    bg_path = ICON_DIR / "bg.png"
    if bg_path.exists():
        img = Image.open(bg_path).resize((450, 450))
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
        if canvas.coords(txt)[1] < 450: canvas.after(50, move)
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
tk.Label(tab2, text="Имя программы:", fg="white", bg="black").pack(pady=5)
prog_entry = tk.Entry(tab2, width=40)
prog_entry.pack()
lang_combo = ttk.Combobox(tab2, values=["Python", "Batch", "VBScript"], state="readonly")
lang_combo.set("Python")
lang_combo.pack(pady=10)
tk.Button(tab2, text="Создать программу", command=lambda: create_file(None, prog_entry, is_prog=True)).pack()

# --- Вкладка 3 ---
tab3 = tk.Frame(notebook, bg="black")
notebook.add(tab3, text="Файлы")
add_bg(tab3)
file_listbox = tk.Listbox(tab3, bg="#101010", fg="white", width=50)
file_listbox.pack(pady=10)
tk.Button(tab3, text="Открыть папку", command=open_location).pack()
tk.Button(tab3, text="Редактировать код", command=edit_code).pack(pady=5)
refresh_file_list()

root.mainloop()