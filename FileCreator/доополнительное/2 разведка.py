import socket
import socket

def scout_target(domain):
    try:
        # 1. Получаем реальный IP
        ip = socket.gethostbyname(domain)
        print(f"[!] Цель найдена: {domain} -> {ip}")
        
        # 2. Проверяем самые частые «дыры» в файрволе (порты)
        ports = [80, 443, 8080]
        for port in ports:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            if s.connect_ex((ip, port)) == 0:
                print(f"[*] Порт {port} открыт — возможный путь.")
            else:
                print(f"[x] Порт {port} закрыт (файрвол активен).")
            s.close()
            
    except Exception as e:
        print(f"[!] Ошибка разведки: {e}")

# Введи сюда сайт для проверки
target = input("Введите адрес сайта (без http://): ")
scout_target(target)