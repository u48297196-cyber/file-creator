import socket
from colorama import init, Fore, Style

init(autoreset=True)

SUCCESS = Fore.GREEN + Style.BRIGHT
WARNING = Fore.RED + Style.BRIGHT
RESET = Style.RESET_ALL

def scout_ip(target):
    print(f"\n{SUCCESS}[!] СКАНИРОВАНИЕ ЦЕЛИ: {target}{RESET}")
    # Проверяем порты для понимания состояния системы
    ports = [21, 22, 80, 443, 3389, 5938]
    
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        if sock.connect_ex((target, port)) == 0:
            print(f"{SUCCESS}[+] Порт {port} ОТКРЫТ{RESET}")
        sock.close()
    print(f"{SUCCESS}[+] Разведка завершена.{RESET}")

def main():
    print(f"\n{SUCCESS}=== ARTILLERY SCOUT ==={RESET}")
    target = input("Введите IP для разведки: ")
    scout_ip(target)
    print(f"\n{SUCCESS}[*] Данные получены. Переходи к AnyDesk для работы.{RESET}")

if __name__ == "__main__":
    main()