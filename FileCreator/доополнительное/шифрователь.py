import tkinter as tk
from tkinter import filedialog, messagebox
import os
import random
import ctypes
import socket

# --- ФУНКЦИИ СЕЙФА (без изменений) ---
def set_hidden(path, hidden=True):
    try:
        attrs = ctypes.windll.kernel32.GetFileAttributesW(path)
        if hidden: ctypes.windll.kernel32.SetFileAttributesW(path, attrs | 2)
        else: ctypes.windll.kernel32.SetFileAttributesW(path, attrs & ~2)
    except: pass

def get_key_path(img_path): return os.path.splitext(img_path)[0] + ".key"

def process_file(mode):
    password = pass_entry.get()
    if not password:
        messagebox.showerror("Ошибка", "Введите пароль!")
        return
    key_val = sum(ord(c) for c in password) % 255
    try:
        if mode == "encrypt":
            file_path = filedialog.askopenfilename(title="Выберите файл")
            if not file_path: return
            img_path = filedialog.askopenfilename(title="Выберите картинку-ключ", filetypes=[("Images", "*.png;*.jpg")])
            if not img_path: return
            file_ext = os.path.splitext(file_path)[1]
            with open(file_path, "rb") as f: data = bytearray(f.read())
            for i in range(len(data)): data[i] ^= key_val
            locked_path = os.path.join(os.path.dirname(img_path), os.path.splitext(os.path.basename(img_path))[0] + ".locked")
            with open(locked_path, "wb") as f: f.write(file_ext.encode() + b"|DATA|" + data)
            set_hidden(locked_path, True)
            with open(get_key_path(img_path), "w", encoding="utf-8") as f: f.write(''.join(random.choices("ᚦᚷᚱᚾᛗᛚᛞᚹᚠᚢᚦᚩᚱᚲᚷᚹᚺᚾᛁᛄ", k=20)))
            set_hidden(get_key_path(img_path), True)
            os.remove(file_path)
            messagebox.showinfo("Готово", "Файл защищен.")
        elif mode == "decrypt":
            img_path = filedialog.askopenfilename(title="Выберите картинку-ключ", filetypes=[("Images", "*.png;*.jpg")])
            if not img_path: return
            locked_path = os.path.join(os.path.dirname(img_path), os.path.splitext(os.path.basename(img_path))[0] + ".locked")
            if not os.path.exists(locked_path):
                messagebox.showerror("Ошибка", "Файл не найден.")
                return
            with open(locked_path, "rb") as f: content = f.read()
            parts = content.split(b"|DATA|", 1)
            file_ext = parts[0].decode()
            data = bytearray(parts[1])
            for i in range(len(data)): data[i] ^= key_val
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            orig_name = os.path.join(desktop_path, os.path.splitext(os.path.basename(locked_path))[0] + file_ext)
            with open(orig_name, "wb") as f: f.write(data)
            set_hidden(orig_name, False)
            os.remove(locked_path)
            if os.path.exists(get_key_path(img_path)): os.remove(get_key_path(img_path))
            messagebox.showinfo("Готово", "Файл восстановлен.")
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))

# --- УМНЫЙ СКАНЕР (ОБНОВЛЕН) ---
def check_ip(ip, mode):
    ip = ip.strip()
    try:
        if mode == "DNS":
            socket.gethostbyname(ip)
            return "ONLINE: DNS доступен"
        else:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            # Имитация GoogleBot
            google_agent = (
                "GET / HTTP/1.1\r\n"
                "Host: google.com\r\n"
                "User-Agent: Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)\r\n"
                "Connection: close\r\n\r\n"
            )
            try:
                s.connect((ip, 80))
                s.send(google_agent.encode())
                response = s.recv(1024)
                s.close()
                return "ONLINE: Googlebot принят" if response else "OFFLINE: Молчит"
            except socket.error as e:
                return f"OFFLINE: Ошибка {e.errno}"
    except Exception as e: return f"ERROR: {str(e)}"

# --- ИНТЕРФЕЙС (без изменений) ---
def scan_window():
    win = tk.Toplevel(root)
    win.title("NetScanner")
    win.geometry("300x300")
    win.configure(bg="#050505")
    ip_entry = tk.Entry(win, bg="#101010", fg="#00FF41", insertbackground="white")
    ip_entry.pack(pady=5)
    tk.Button(win, text="ВСТАВИТЬ IP", command=lambda: [ip_entry.delete(0, tk.END), ip_entry.insert(0, root.clipboard_get())], bg="#222", fg="white").pack()
    method = tk.StringVar(value="TCP")
    tk.Radiobutton(win, text="Прямой запрос (TCP)", variable=method, value="TCP", bg="#050505", fg="white", selectcolor="#000").pack()
    tk.Radiobutton(win, text="Через Google DNS", variable=method, value="DNS", bg="#050505", fg="white", selectcolor="#000").pack()
    lbl = tk.Label(win, text="Статус: -", fg="white", bg="#050505")
    lbl.pack(pady=10)
    tk.Button(win, text="ПРОВЕРИТЬ", command=lambda: lbl.config(text=check_ip(ip_entry.get(), method.get())), bg="#003300", fg="white").pack()

root = tk.Tk()
root.title("CryptoCore")
root.geometry("300x300")
root.configure(bg="#050505")
pass_entry = tk.Entry(root, show="*", bg="#101010", fg="#00FF41", width=25, insertbackground="white")
pass_entry.pack(pady=20)
tk.Button(root, text="ВСТАВИТЬ ПАРОЛЬ", command=lambda: [pass_entry.delete(0, tk.END), pass_entry.insert(0, root.clipboard_get())], bg="#222", fg="white").pack(pady=5)
tk.Button(root, text="ЗАЩИТИТЬ", command=lambda: process_file("encrypt"), bg="#330000", fg="white").pack(fill="x", padx=30)
tk.Button(root, text="ОТКРЫТЬ", command=lambda: process_file("decrypt"), bg="#003300", fg="white").pack(fill="x", padx=30)
tk.Button(root, text="NET SCANNER", command=scan_window, bg="#111111", fg="#00FF41").pack(fill="x", padx=30, pady=10)
root.mainloop()