import os
import socket
import re
import requests
import time
import ssl
from concurrent.futures import ThreadPoolExecutor

# ===== COLORS =====
C = {
    "RED": "\033[38;5;196m",
    "GREEN": "\033[38;5;46m",
    "YELLOW": "\033[38;5;226m",
    "CYAN": "\033[38;5;51m",
    "MAGENTA": "\033[38;5;201m",
    "BLUE": "\033[38;5;39m",
    "WHITE": "\033[0m",
    "BOLD": "\033[1m"
}

# ===== SETUP =====
RESULT_DIR = "results"
os.makedirs(RESULT_DIR, exist_ok=True)

OUTPUT = f"{RESULT_DIR}/scan_{int(time.time())}.txt"

VERSION = "1.2"
LATEST = "1.2"

# ===== UI =====
def clear():
    os.system("clear" if os.name == "posix" else "cls")

def banner():
    clear()
    print(C["RED"] + C["BOLD"])

    print(r"""
████████╗      ██████╗ ███████╗██╗  ██╗
╚══██╔══╝      ██╔══██╗██╔════╝╚██╗██╔╝
   ██║   █████╗██████╔╝█████╗   ╚███╔╝ 
   ██║   ╚════╝██╔══██╗██╔══╝   ██╔██╗ 
   ██║         ██║  ██║███████╗██╔╝ ██╗
   ╚═╝         ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
""")

    print(C["MAGENTA"] + "            🦖 T - R E X 🦖\n")

    print(C["CYAN"] + "╔══════════════════════════════════════╗")
    print(C["GREEN"] + "║   🟢 STATUS  : ONLINE              ║")
    print(C["YELLOW"] + f"║   ⚡ VERSION : {VERSION}                 ║")
    print(C["BLUE"] + "║   🔥 MODE    : ULTRA PRO MAX       ║")
    print(C["MAGENTA"] + "║   ⚡ POWER   : SNI + TCP + DOMAIN  ║")
    print(C["CYAN"] + "╚══════════════════════════════════════╝\n")

    print(C["MAGENTA"] + "⚙️ Booting T-Rex Engine ", end="")
    for _ in range(6):
        print("█", end="", flush=True)
        time.sleep(0.2)

    print("\n" + C["GREEN"] + "✅ T-Rex Ready To Hunt!\n" + C["WHITE"])

def menu():
    print(C["CYAN"] + """
[1] 🌐 Domain File Scanner
[2] 🔌 TCP / HTTP Scanner
[3] 🔐 SNI Scanner
[4] 🔎 Extract Domains
[5] 🧹 Clean Domains
[6] 🌍 Subdomain Finder
[7] 🔄 Update Tool
[8] 🚪 Exit
""" + C["WHITE"])

def save(data):
    with open(OUTPUT, "a") as f:
        f.write(data + "\n")

# ===== FEATURES =====

def scan_domain(domain):
    try:
        ip = socket.gethostbyname(domain)
        res = f"{domain} ➜ {ip}"
        print(C["GREEN"] + res + C["WHITE"])
        save(res)
    except:
        print(C["RED"] + f"{domain} ➜ Invalid" + C["WHITE"])

def domain_scanner():
    file = input("📁 File path: ")
    try:
        with open(file) as f:
            domains = f.read().splitlines()

        print(C["YELLOW"] + "\n🚀 Scanning...\n")

        with ThreadPoolExecutor(max_workers=30) as exe:
            exe.map(scan_domain, domains)

    except:
        print(C["RED"] + "❌ File error")

def tcp_scan(host, port):
    try:
        s = socket.socket()
        s.settimeout(1)
        if s.connect_ex((host, port)) == 0:
            res = f"{host}:{port} OPEN"
            print(C["GREEN"] + res)
            save(res)
        s.close()
    except:
        pass

def tcp_http():
    host = input("🌐 Domain/IP: ")
    ports = [21, 22, 80, 443, 8080]

    print(C["YELLOW"] + "\n🚀 Scanning Ports...\n")

    with ThreadPoolExecutor(max_workers=50) as exe:
        exe.map(lambda p: tcp_scan(host, p), ports)

    try:
        r = requests.get(f"http://{host}", timeout=5)
        print(C["CYAN"] + f"HTTP Status: {r.status_code}")
    except:
        print(C["RED"] + "HTTP Failed")

def sni_scan():
    host = input("🌐 Domain: ")

    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        s = ctx.wrap_socket(socket.socket(), server_hostname=host)
        s.settimeout(3)
        s.connect((host, 443))

        res = f"SNI OK: {host}"
        print(C["GREEN"] + res)
        save(res)
        s.close()

    except:
        print(C["RED"] + "❌ SNI FAILED")

def extract_domains():
    text = input("📋 Paste text: ")
    found = set(re.findall(r'\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}', text))

    for d in found:
        print(C["GREEN"] + d)
        save(d)

def clean_domains():
    file = input("📁 File: ")
    try:
        with open(file) as f:
            data = f.read().splitlines()

        for d in set(data):
            d = re.sub(r"http[s]?://", "", d).split("/")[0]
            print(C["GREEN"] + d)
            save(d)
    except:
        print(C["RED"] + "❌ Error")

def subdomain_finder():
    domain = input("🌍 Domain: ")
    words = ["www", "mail", "ftp", "api", "dev", "test", "admin", "blog"]

    print(C["YELLOW"] + "\n🔍 Finding subdomains...\n")

    for w in words:
        sub = f"{w}.{domain}"
        try:
            socket.gethostbyname(sub)
            res = f"FOUND: {sub}"
            print(C["GREEN"] + res)
            save(res)
        except:
            pass

def update():
    print(C["YELLOW"] + "\n🔄 Checking updates...\n")
    time.sleep(1)

    if VERSION != LATEST:
        print(C["GREEN"] + "✅ Update available")
    else:
        print(C["CYAN"] + "😎 Already latest version")

# ===== MAIN =====
if __name__ == "__main__":
    while True:
        banner()
        menu()
        ch = input("➤ Select: ")

        if ch == "1": domain_scanner()
        elif ch == "2": tcp_http()
        elif ch == "3": sni_scan()
        elif ch == "4": extract_domains()
        elif ch == "5": clean_domains()
        elif ch == "6": subdomain_finder()
        elif ch == "7": update()
        elif ch == "8":
            print(C["RED"] + "👋 Exiting T-Rex Tool")
            break
        else:
            print(C["RED"] + "❌ Invalid Option")

        input("\n👉 Press Enter to continue...")
