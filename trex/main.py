import os
import socket
import re
import requests
import time
from concurrent.futures import ThreadPoolExecutor

# ===== COLORS =====
R = "\033[91m"; G = "\033[92m"; Y = "\033[93m"; C = "\033[96m"; W = "\033[0m"

RESULT_DIR = "results"
if not os.path.exists(RESULT_DIR):
    os.makedirs(RESULT_DIR)

OUTPUT = f"{RESULT_DIR}/scan.txt"

# ===== UI =====
def clear():
    os.system("clear" if os.name == "posix" else "cls")

def animate(text):
    for c in text:
        print(c, end="", flush=True)
        time.sleep(0.01)
    print()

def banner():
    clear()
    print(C)
    animate("╔══════════════════════════════╗")
    animate("║        T-REX PRO+ TOOL       ║")
    animate("╚══════════════════════════════╝")
    print(W)

def menu():
    print(f"""
{Y}[1]{W} Domain File Scanner
{Y}[2]{W} TCP / HTTP Scanner
{Y}[3]{W} Extract Domains
{Y}[4]{W} Clean Domains
{Y}[5]{W} Subdomain Finder
{Y}[6]{W} Exit
""")

def save(data):
    with open(OUTPUT, "a") as f:
        f.write(data + "\n")

# ===== Progress =====
def progress(i, total):
    percent = int((i / total) * 100)
    bar = "█" * (percent // 5) + "-" * (20 - (percent // 5))
    print(f"\r[{bar}] {percent}%", end="")

# ===== FEATURES =====

# 1 Domain Scanner
def scan_domain(domain):
    try:
        ip = socket.gethostbyname(domain)
        res = f"{domain} ➜ {ip}"
        print(G + res + W)
        save(res)
    except:
        res = f"{domain} ➜ Invalid"
        print(R + res + W)
        save(res)

def domain_scanner():
    file = input("File path: ")
    try:
        with open(file) as f:
            domains = f.read().splitlines()

        total = len(domains)
        print(Y + "\nScanning...\n" + W)

        with ThreadPoolExecutor(max_workers=25) as exe:
            for i, _ in enumerate(exe.map(scan_domain, domains), 1):
                progress(i, total)

    except:
        print(R + "File error!" + W)

# 2 TCP / HTTP Scanner
def tcp_scan(host, port):
    try:
        s = socket.socket()
        s.settimeout(1)
        s.connect((host, port))
        res = f"{host}:{port} OPEN"
        print(G + res + W)
        save(res)
        s.close()
    except:
        pass

def tcp_http():
    host = input("Domain/IP: ")
    ports = [21, 22, 80, 443, 8080]

    print(Y + "\nScanning Ports...\n" + W)

    with ThreadPoolExecutor(max_workers=50) as exe:
        for p in ports:
            exe.submit(tcp_scan, host, p)

    try:
        r = requests.get(f"http://{host}", timeout=5)
        res = f"HTTP {r.status_code}"
        print(C + res + W)
        save(res)
    except:
        print(R + "HTTP Fail" + W)

# 3 Extract Domains
def extract_domains():
    text = input("Paste text: ")
    found = set(re.findall(r'\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}', text))

    print(Y + "\nDomains:\n" + W)
    for d in found:
        print(G + d + W)
        save(d)

# 4 Clean Domains
def clean_domains():
    file = input("File path: ")
    try:
        with open(file) as f:
            data = f.read().splitlines()

        for d in set(data):
            if re.match(r'\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}', d):
                print(G + d + W)
                save(d)
    except:
        print(R + "Error" + W)

# 5 Subdomain Finder
def subdomain_finder():
    domain = input("Enter domain (example.com): ")

    wordlist = ["www", "mail", "ftp", "api", "dev", "test", "admin", "blog"]
    print(Y + "\nFinding subdomains...\n" + W)

    for sub in wordlist:
        url = f"{sub}.{domain}"
        try:
            socket.gethostbyname(url)
            res = f"FOUND: {url}"
            print(G + res + W)
            save(res)
        except:
            pass

# ===== ENTRY POINT =====
def run():
    while True:
        banner()
        menu()

        ch = input("➤ Select: ")

        if ch == "1":
            domain_scanner()
        elif ch == "2":
            tcp_http()
        elif ch == "3":
            extract_domains()
        elif ch == "4":
            clean_domains()
        elif ch == "5":
            subdomain_finder()
        elif ch == "6":
            break
        else:
            print(R + "Invalid" + W)

        input("\nPress Enter...")

if __name__ == "__main__":
    run()
