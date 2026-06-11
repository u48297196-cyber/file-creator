import tkinter as tk
from tkinter import ttk
from pathlib import Path

FORMATS = {
    "TXT": ".txt",
    "BAT": ".bat",
    "VBS": ".vbs",
    "PS1": ".ps1",
    "HTML": ".html",
    "PY": ".py",
    "JS": ".js",
    "LUA": ".lua"
}

def create_file():
    name = name_entry.get().strip()

    if not name:
        status.config(text="Введите имя файла")
        return

    ext = FORMATS[combo.get()]

    desktop = Path.home() / "Desktop"
    path = desktop / f"{name}{ext}"

    open(path, "w", encoding="utf-8").close()

    status.config(text=f"Создан: {name}{ext}")

root = tk.Tk()
root.title("File Creator")
root.geometry("400x250")

tk.Label(root, text="Имя файла").pack(pady=5)

name_entry = tk.Entry(root, width=30)
name_entry.pack()

tk.Label(root, text="Формат").pack(pady=5)

combo = ttk.Combobox(
    root,
    values=list(FORMATS.keys()),
    state="readonly"
)
combo.pack()
combo.current(0)

tk.Button(
    root,
    text="Добавить на стол",
    command=create_file
).pack(pady=20)

status = tk.Label(root, text="")
status.pack()

root.mainloop()
