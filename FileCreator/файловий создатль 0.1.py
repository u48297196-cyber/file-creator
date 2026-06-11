import tkinter as tk
from tkinter import ttk, messagebox
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
        status.config(text="Ошибка: введите имя файла", fg="red")
        return

    ext = FORMATS[combo.get()]
    # Сохраняем на рабочий стол
    path = Path.home() / "Desktop" / f"{name}{ext}"

    try:
        # Создаем файл, если он не существует
        if not path.exists():
            path.touch()
            status.config(text=f"Успешно: {name}{ext}", fg="green")
        else:
            status.config(text="Ошибка: такой файл уже есть", fg="red")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось создать файл: {e}")

root = tk.Tk()
root.title("File Creator Pro")
root.geometry("300x250")

tk.Label(root, text="Имя файла (без расширения):").pack(pady=5)
name_entry = tk.Entry(root, width=30)
name_entry.pack()

tk.Label(root, text="Выберите формат:").pack(pady=5)
combo = ttk.Combobox(root, values=list(FORMATS.keys()), state="readonly")
combo.pack()
combo.current(0)

# Добавлена кнопка для открытия папки (очень удобно для проверки)
def open_desktop():
    import os
    os.startfile(Path.home() / "Desktop")

tk.Button(root, text="Создать файл", command=create_file, bg="#e1e1e1").pack(pady=10)
tk.Button(root, text="Открыть рабочий стол", command=open_desktop).pack()

status = tk.Label(root, text="", fg="black")
status.pack(pady=10)

root.mainloop()