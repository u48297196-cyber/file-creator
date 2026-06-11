import tkinter as tk
import random
import string
import pyperclip # Для этой кнопки нужно: pip install pyperclip

def generate():
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    name_parts = ["Cyber", "Shadow", "Neon", "Void", "Ghost", "X", "Pulse", "Titan"]
    
    password = "".join(random.choice(chars) for _ in range(16))
    nickname = random.choice(name_parts) + str(random.randint(100, 999))
    
    # Сохраняем во временную переменную для копирования
    root.generated_password = password
    
    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, f"> PASSWORD: {password}\n")
    result_text.insert(tk.END, f"> NICKNAME: {nickname}\n")
    result_text.config(state=tk.DISABLED)

def copy_to_clipboard():
    if hasattr(root, 'generated_password'):
        pyperclip.copy(root.generated_password)
        log.insert(tk.END, "> COPIED TO CLIPBOARD!\n")

root = tk.Tk()
root.title("MATRIX_SEC_TOOL")
root.geometry("450x350")
root.configure(bg="black")

# Кнопки
btn_gen = tk.Button(root, text="GENERATE", command=generate, bg="black", fg="#00FF00", font=("Courier", 10, "bold"))
btn_gen.pack(pady=10)

btn_copy = tk.Button(root, text="COPY PASSWORD", command=copy_to_clipboard, bg="black", fg="#00FF00", font=("Courier", 10))
btn_copy.pack(pady=5)

# Поле вывода
result_text = tk.Text(root, height=4, width=50, bg="black", fg="#00FF00", font=("Courier", 11), borderwidth=0)
result_text.pack(pady=10)

# Матричный лог (имитация хакерского экрана)
log = tk.Text(root, height=6, width=50, bg="black", fg="#005500", font=("Courier", 9))
log.pack(pady=10)
log.insert(tk.END, "SYSTEM READY... ACCESS GRANTED.\nLOADING MATRIX_DECRYPTION.EXE...")

root.mainloop()