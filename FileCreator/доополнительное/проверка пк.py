import tkinter as tk
import random
import psutil
import GPUtil
import time

# --- КОНСОЛЬНЫЙ ЛОГ ---
print("--- [INITIALIZING CYBER SENTINEL V6] ---")
time.sleep(0.3)
print("[DEBUG] Linking thermal sensors...")
print("[DEBUG] Initializing cooling protocols...")
print("[OK] Systems Ready.")
print("--- [ALL SYSTEMS OPERATIONAL] ---")

def matrix_rain():
    rain = "".join(str(random.randint(0, 1)) + " " for _ in range(25))
    matrix_log.config(state=tk.NORMAL)
    matrix_log.insert(tk.END, rain + "\n")
    if int(matrix_log.index('end-1c').split('.')[0]) > 20:
        matrix_log.delete('1.0', '2.0')
    matrix_log.see(tk.END)
    matrix_log.config(state=tk.DISABLED)
    root.after(30, matrix_rain)

def set_fans(mode):
    # Это "хакерская заглушка" для управления вентиляторами
    print(f"[ACTION] Cooling set to: {mode} MODE")
    fan_status_lbl.config(text=f"COOLING: {mode}")

def update_stats():
    try:
        gpus = GPUtil.getGPUs()
        if gpus:
            gpu = gpus[0]
            load = int(gpu.load * 100) if (gpu.load == gpu.load) else 0
            temp = int(gpu.temperature) if (gpu.temperature == gpu.temperature) else 0
            # Симулируем FPS (нагрузка обратно пропорциональна FPS)
            fps = 144 - load  
            info = f"GPU: {gpu.name[:15]}\nTEMP: {temp}°C | LOAD: {load}%\nFPS ESTIMATE: {fps}"
        else:
            info = "GPU: OFFLINE"
        
        cpu = psutil.cpu_percent()
        main_label.config(text=f"{info}\nCPU LOAD: {cpu}%")
    except:
        main_label.config(text="SENSORS: STANDBY")
    
    root.after(1000, update_stats)

root = tk.Tk()
root.title("CYBER_SENTINEL_V6")
root.geometry("400x600")
root.configure(bg="black")

main_label = tk.Label(root, text="INITIALIZING...", font=("Courier", 12, "bold"), bg="black", fg="#00FF00")
main_label.pack(pady=20)

# Кнопки управления вентиляторами
btn_frame = tk.Frame(root, bg="black")
btn_frame.pack()
tk.Button(btn_frame, text="QUIET", command=lambda: set_fans("QUIET"), bg="black", fg="#00FF00").pack(side="left", padx=5)
tk.Button(btn_frame, text="TURBO", command=lambda: set_fans("TURBO"), bg="black", fg="#00FF00").pack(side="left", padx=5)

fan_status_lbl = tk.Label(root, text="COOLING: AUTO", font=("Courier", 10), bg="black", fg="#00F2FE")
fan_status_lbl.pack(pady=10)

matrix_log = tk.Text(root, height=15, width=30, bg="black", fg="#00FF00", font=("Courier", 10), borderwidth=0)
matrix_log.pack(pady=10)

matrix_rain()
update_stats()
root.mainloop()