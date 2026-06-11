import requests
import sys
import os
from datetime import datetime
from colorama import init, Fore, Style

# Инициализация стилей
init(autoreset=True)

SUCCESS = Fore.GREEN + Style.BRIGHT
WARNING = Fore.RED + Style.BRIGHT
RESET = Style.RESET_ALL

# Файл отчета всегда создается рядом со скриптом
REPORT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scan_report.txt")

def save_to_report(data):
    """Автоматическая запись найденных уязвимостей в файл"""
    try:
        with open(REPORT_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().strftime('%d.%m %H:%M:%S')}] {data}\n")
    except Exception as e:
        print(f"{WARNING}[!] Ошибка записи: {e}{RESET}")

def scout_info(target):
    """Анализ ОС и заголовков безопасности"""
    print(f"\n{SUCCESS}[!] АНАЛИЗ ЦЕЛИ: {target}{RESET}")
    weaknesses = []
    try:
        r = requests.get(f"http://{target}", timeout=5)
        server_info = r.headers.get('Server', 'Неизвестно')
        print(f"{SUCCESS}[+] ОС/СЕРВЕР: {server_info}{RESET}")
        save_to_report(f"Target: {target} | Server: {server_info}")
        
        # Проверка безопасности заголовков
        check_list = ['X-Frame-Options', 'Content-Security-Policy', 'Strict-Transport-Security']
        for header in check_list:
            if header in r.headers:
                print(f"{SUCCESS}[+] {header}: OK{RESET}")
            else:
                weakness = f"Отсутствует заголовок: {header}"
                weaknesses.append(weakness)
                print(f"{WARNING}[!] {weakness}{RESET}")
        
        if weaknesses:
            save_to_report(f"Target: {target} | Vulnerabilities: {', '.join(weaknesses)}")
            print(f"{SUCCESS}[+] Отчет сохранен в {REPORT_FILE}{RESET}")
            
    except Exception as e:
        print(f"{WARNING}[x] Ошибка: {e}{RESET}")

def find_directories(target):
    """Поиск скрытых директорий"""
    print(f"\n{SUCCESS}[!] ПОИСК ПУТЕЙ НА {target}...{RESET}")
    wordlist = ["admin", "login", "config", "backup", "uploads", "test", "db", "api"]
    
    for folder in wordlist:
        url = f"http://{target}/{folder}"
        try:
            r = requests.get(url, timeout=2)
            if r.status_code == 200:
                print(f"{SUCCESS}[+] НАЙДЕНО: {url} (Status: 200){RESET}")
                save_to_report(f"Found path: {url}")
            elif r.status_code == 403:
                print(f"{WARNING}[-] ЗАКРЫТО: {url} (Status: 403){RESET}")
        except:
            continue
    print(f"{SUCCESS}[+] Поиск завершен. Результаты в {REPORT_FILE}{RESET}")

def main():
    while True:
        print(f"\n{SUCCESS}=== ARTILLERY HQ: FINAL VERSION ==={RESET}")
        print("1. [INFO + SEC] Сканирование заголовков и ОС")
        print("2. [DIR] Поиск директорий")
        print("0. [ВЫХОД]")
        
        choice = input("\nКоманда > ").strip()
        
        if choice == '1':
            target = input("Введите домен: ")
            scout_info(target)
        elif choice == '2':
            target = input("Введите домен для поиска: ")
            find_directories(target)
        elif choice == '0':
            sys.exit()
        else:
            print(f"{WARNING}Неверная команда.{RESET}")

if __name__ == "__main__":
    main()