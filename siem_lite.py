import re
import requests
import subprocess
from collections import Counter

# --- SETTINGS ---
TELEGRAM_BOT_TOKEN = "WRITE_THE_TOKEN_YOU_RECEIVED_FROM_BOTFATHER_HERE"
TELEGRAM_CHAT_ID = "WRITE_YOUR_OWN_ID_NUMBER_HERE"

# Enter your own IP address here (e.g., "85.100.12.34"). This is crucial to avoid banning yourself!
WHITELIST = ["127.0.0.1", "YOUR_PUBLIC_IP_ADDRESS"] 

def send_telegram_alert(ip, number_of_attempts, ban_status):
    """
    When a danger is detected, it sends a message to the administrator via Telegram.
    It also reports whether the ban operation was successful.
    """
    ban_msg = "✅ Successfully Blocked (Iptables)" if ban_status else "❌ Not Blocked / Whitelisted"
    
    msg = (
        f"🚨 *SIEM Security Alarm* 🚨\n\n"
        f"⚠️ *Threatening:* SSH Brute-Force Attack\n"
        f"🌍 *Attacker IP:* `{ip}`\n"
        f"🔢 *Başarısız Deneme:* {number_of_attempts}\n"
        f"🛑 *Action:* {ban_msg}"
    )
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"}
    
    try:
        if "BURAYA" not in TELEGRAM_BOT_TOKEN:
            requests.post(url, json=payload, timeout=5)
    except Exception:
        pass # The script should not stop running even if an error occurs.
def block_ip(ip):
    """
    Ban the specified IP address from the server using Linux Iptables..
    """
    if ip in WHITELIST:
        print(f"[-] PROTECTION: {ip} The address is on the whitelist; it hasn't been banned!")
        return False

    try:
        # iptables command: -A (Append rule), INPUT (Incoming traffic), -s (Source IP), -j DROP (Drop/discard packet)
        komut = ["iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"]
        
        # We run the command in the terminal using subprocess.run.
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"[+] ACTIVE DEFENSE: {ip} The address has been SUCCESSFULLY BANNED from the firewall!")
        return True
    except subprocess.CalledProcessError:
        print(f"[-] Error: {ip} The iptables command failed while banning the address. (Do you have root privileges?)")
        return False
    except FileNotFoundError:
        print("[-] Error: The iptables tool was not found. Your server might be using a different firewall (e.g., firewalld).")
        return False

def analyze_real_log(log_path, threshold=5):
    """
    It reads the logs, identifies the attacker, and triggers active defense.
    """
    print(f"[*] {log_path} The file is being analyzed...\n")
    regex_deseni = r"Failed password for .* from ([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)"
    ip_sayici = Counter()
    
    try:
        with open(log_path, "r") as dosya:
            for satir in dosya:
                eslesme = re.search(regex_deseni, satir)
                if eslesme:
                    ip = eslesme.group(1)
                    ip_sayici[ip] += 1
                    
        tehlike_yok = True
        for ip, sayi in ip_sayici.items():
            if sayi >= threshold:
                print(f"\n[!] ALARM (BRUTE-FORCE): {number} failed login attempts detected from {ip} address!")
                
                # Step 1: Block the attacker.
                ban_status = block_ip(ip)
                
                # Step 2: Report the situation to Telegram.
                send_telegram_alert(ip, sayi, ban_status)
                
                tehlike_yok = False
                
        if tehlike_yok:
            print("[-] No suspicious IP exceeding the threshold value was detected..")
            
    except PermissionError:
        print(f"[-] Error: You do not have read permission. Please run the script with 'sudo'.")
    except Exception as e:
        print(f"[-] Unexpected error: {e}")

if __name__ == "__main__":
    print("-" * 50)
    print("  SIEM LITE - ACTIVE DEFENSE SYSTEM (IPS)")
    print("-" * 50)
    
    # Log path for your own cloud server (Oracle)
    hedeflanan_log = "/var/log/secure"      
    
    # Those who make 5 or more failed attempts are instantly banned.
    analyze_real_log(hedeflanan_log, threshold=5)
