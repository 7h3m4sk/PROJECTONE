#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#       _       _  _           _____     _ _____ 
#   __ | |___  | || | ___ __ _ \ ___| __| |  ___|
#  \ \| |__  \_| || |/ _ ' _` |/ _|  / _` |\ \   
#   >   / __|_   __| | | | | | (___| | | | \ \  
# /_/|_\___| |_|  |_| |_| |_|\____|_| |_|  \_\ 




import os
import sys
import time
import subprocess
import threading

# Kolory terminala
GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RESET = "\033[0m"
BOLD = "\033[1m"

# === Efekt "typing" - powolne wyświetlanie tekstu ===
def typing_effect(text, delay=0.002):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()  # nowa linia po napisie

# === Intro z bannerem ===
def print_intro():
    intro_text = f"""
{CYAN}{BOLD}

██████╗░██████╗░░█████╗░░░░░░██╗███████╗░█████╗░████████╗░█████╗░███╗░░██╗███████╗
██╔══██╗██╔══██╗██╔══██╗░░░░░██║██╔════╝██╔══██╗╚══██╔══╝██╔══██╗████╗░██║██╔════╝
██████╔╝██████╔╝██║░░██║░░░░░██║█████╗░░██║░░╚═╝░░░██║░░░██║░░██║██╔██╗██║█████╗░░
██╔═══╝░██╔══██╗██║░░██║██╗░░██║██╔══╝░░██║░░██╗░░░██║░░░██║░░██║██║╚████║██╔══╝░░
██║░░░░░██║░░██║╚█████╔╝╚█████╔╝███████╗╚█████╔╝░░░██║░░░╚█████╔╝██║░╚███║███████╗
╚═╝░░░░░╚═╝░░╚═╝░╚════╝░░╚════╝░╚══════╝░╚════╝░░░░╚═╝░░░░╚════╝░╚═╝░░╚══╝╚══════╝

                     ╔═════════════════════════════════════╗
                     ║ 1) Auto-change IP in X second       ║
                     ║ 2) Start Tor                        ║
                     ║ 3) Stop Tor                         ║
                     ║ 4) Restart Tor                      ║
                     ║ 5) Check status and IP              ║
                     ║ 6) Next IP                          ║
                     ║ 7) Install Tor  (Arch Linux)        ║
                     ║ 0) Exit                             ║
                     ╚═════════════════════════════════════╝





{RESET}
"""
    typing_effect(intro_text)
    time.sleep(1)
    clear()

# === Spinner ===
stop_spinner = False

def spinner(text="Pracuję"):
    global stop_spinner
    frames = ['|', '/', '-', '\\']
    i = 0
    while not stop_spinner:
        sys.stdout.write(f"\r{CYAN}[{frames[i % 4]}] {text}...{RESET}")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write('\r' + ' ' * 60 + '\r')

# === Sprawdzanie zależności ===
required_modules = {
    "stem": "python-stem",
    "requests": "python-requests"
}

missing = []

for module, package in required_modules.items():
    try:
        __import__(module)
    except ImportError:
        missing.append(f"{module} (pacman: {package})")

if missing:
    print(f"\n{RED}[!] Brakuje wymaganych bibliotek:{RESET}")
    for m in missing:
        print(f" - {YELLOW}{m}{RESET}")
    print(f"\n{BOLD}Zainstaluj brakujące pakiety na Arch Linux:{RESET}")
    print(f"{CYAN}sudo pacman -S {' '.join(pkg for _, pkg in required_modules.items())}{RESET}\n")
    sys.exit(1)

# === Import wymaganych bibliotek ===
from stem import Signal
from stem.control import Controller
import requests

# === Narzędzia ===
def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def check_root():
    if os.geteuid() != 0:
        print(f"\n{RED}[-] Uruchom ten skrypt jako root (sudo)!{RESET}\n")
        sys.exit(1)

def install_tor():
    print("[*] Sprawdzam czy tor jest zainstalowany...")
    if subprocess.call("which tor", shell=True) != 0:
        print("[*] Tor nie jest zainstalowany. Instaluję...")
        subprocess.call("pacman -Sy tor --noconfirm", shell=True)
    else:
        print("[*] Tor jest już zainstalowany.")

def start_tor():
    global stop_spinner
    stop_spinner = False
    t = threading.Thread(target=spinner, args=("Uruchamiam Tor",))
    t.start()
    subprocess.call("systemctl start tor", shell=True)
    time.sleep(3)
    stop_spinner = True
    t.join()


def stop_tor():
    global stop_spinner
    stop_spinner = False
    t = threading.Thread(target=spinner, args=("Zatrzymuję Tor",))
    t.start()
    subprocess.call("systemctl stop tor", shell=True)
    time.sleep(3)
    stop_spinner = True
    t.join()

def restart_tor():
    print("[*] Restartuję usługę tor...")
    subprocess.call("systemctl restart tor", shell=True)

def is_tor_running():
    status = subprocess.run("systemctl is-active tor", shell=True, capture_output=True, text=True)
    return status.stdout.strip() == "active"

def get_ip():
    try:
        ip = requests.get(
            "http://checkip.amazonaws.com",
            proxies={
                "http": "socks5://127.0.0.1:9050",
                "https": "socks5://127.0.0.1:9050"
            },
            timeout=10
        ).text.strip()
        return ip
    except Exception as e:
        return f"Error: {e}"

def change_ip():
    global stop_spinner
    stop_spinner = False
    t = threading.Thread(target=spinner, args=("Zmieniam IP przez Tor",))
    t.start()

    try:
        with Controller.from_port(port=9051) as controller:
            controller.authenticate()
            controller.signal(Signal.NEWNYM)
            time.sleep(5)
        return True
    except Exception as e:
        print(f"\n{RED}[!] Błąd zmiany IP: {e}{RESET}")
        return False
    finally:
        stop_spinner = True
        t.join()

def show_status():
    print(f"{BOLD}=== Status Tora i IP ==={RESET}")
    running = is_tor_running()
    status = f"{GREEN}Aktywna{RESET}" if running else f"{RED}Nieaktywna{RESET}"
    print(f"Usługa Tor: {status}")
    if running:
        ip = get_ip()
        print(f"Twoje IP przez Tor: {CYAN}{ip}{RESET}")
    print(f"{BOLD}========================={RESET}")

def print_menu():
    print(f"""{BOLD}{CYAN}

██████╗░██████╗░░█████╗░░░░░░██╗███████╗░█████╗░████████╗░█████╗░███╗░░██╗███████╗
██╔══██╗██╔══██╗██╔══██╗░░░░░██║██╔════╝██╔══██╗╚══██╔══╝██╔══██╗████╗░██║██╔════╝
██████╔╝██████╔╝██║░░██║░░░░░██║█████╗░░██║░░╚═╝░░░██║░░░██║░░██║██╔██╗██║█████╗░░
██╔═══╝░██╔══██╗██║░░██║██╗░░██║██╔══╝░░██║░░██╗░░░██║░░░██║░░██║██║╚████║██╔══╝░░
██║░░░░░██║░░██║╚█████╔╝╚█████╔╝███████╗╚█████╔╝░░░██║░░░╚█████╔╝██║░╚███║███████╗
╚═╝░░░░░╚═╝░░╚═╝░╚════╝░░╚════╝░╚══════╝░╚════╝░░░░╚═╝░░░░╚════╝░╚═╝░░╚══╝╚══════╝

                     ╔═════════════════════════════════════╗                  
                     ║ 1) Auto-change IP in X second       ║                  
                     ║ 2) Start Tor                        ║                  
                     ║ 3) Stop Tor                         ║                  
                     ║ 4) Restart Tor                      ║                  
                     ║ 5) Check status and IP              ║                  
                     ║ 6) Next IP                          ║                  
                     ║ 7) Install Tor  (Arch Linux)        ║                  
                     ║ 0) Exit                             ║                  
                     ╚═════════════════════════════════════╝
{RESET}""")

def auto_change_ip_loop():
    interval = input("Podaj interwał zmiany IP w sekundach (min 10): ")
    try:
        interval = int(interval)
        if interval < 10:
            print(f"{YELLOW}[!] Za krótki interwał. Ustawiam 10 sekund.{RESET}")
            interval = 10
    except:
        print(f"{YELLOW}[!] Nieprawidłowa wartość. Ustawiam 60 sekund.{RESET}")
        interval = 60
# === why?
    print(f"{CYAN}[+] Automatyczna zmiana IP co {interval} sekund. Ctrl+C aby przerwać.{RESET}\n")
    try:
        while True:
            if change_ip():
                ip = get_ip()
                print(f"{GREEN}[+] Nowe IP: {ip}{RESET}")
            else:
                print(f"{RED}[!] Nie udało się zmienić IP.{RESET}")
            time.sleep(interval)
    except KeyboardInterrupt:
        print(f"\n{YELLOW}[!] Automatyczne zmienianie IP przerwane.{RESET}")

# === Główna pętla ===
def main():
    check_root()
    clear()
    print_intro()
    while True:
        print_menu()
        choice = input("Wybierz opcję: ").strip()
        clear()

        if choice == '1':
            auto_change_ip_loop()
        elif choice == '2':
            start_tor()
        elif choice == '3':
            stop_tor()
        elif choice == '4':
            restart_tor()
        elif choice == '5':
            show_status()
        elif choice == '6':
            if change_ip():
                print(f"{GREEN}[+] IP zostało zmienione pomyślnie!{RESET}")
                print(f"Nowe IP: {CYAN}{get_ip()}{RESET}")
            else:
                print(f"{RED}[!] Nie udało się zmienić IP.{RESET}")
        elif choice == '7':
            install_tor()
        elif choice == '0':
            print(f"{YELLOW}Do zobaczenia!{RESET}")
            sys.exit(0)
        else:
            print(f"{RED}[!] Nieznana opcja.{RESET}")
        input(f"\n{CYAN}Naciśnij Enter, aby kontynuować...{RESET}")
        clear()

if __name__ == "__main__":
    main()
