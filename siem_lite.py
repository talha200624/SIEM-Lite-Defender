import re
import requests
import subprocess
from collections import Counter

# --- AYARLAR ---
TELEGRAM_BOT_TOKEN = "BURAYA_BOTFATHERDAN_ALDIGIN_TOKENI_YAZ"
TELEGRAM_CHAT_ID = "BURAYA_KENDI_ID_NUMARANI_YAZ"

# KENDİ IP ADRESİNİ BURAYA YAZ (Örn: "85.100.12.34"). Kendini banlamamak için çok önemli!
WHITELIST = ["127.0.0.1", "KENDI_PUBLIC_IP_ADRESIN"] 

def send_telegram_alert(ip, deneme_sayisi, ban_durumu):
    """
    Tehlike tespit edildiğinde Telegram üzerinden yöneticiye mesaj atar.
    Ban işleminin başarılı olup olmadığını da bildirir.
    """
    ban_mesaji = "✅ Başarıyla Engellendi (Iptables)" if ban_durumu else "❌ Engellenemedi / Beyaz Listede"
    
    mesaj = (
        f"🚨 *SIEM GÜVENLİK ALARMI* 🚨\n\n"
        f"⚠️ *Tehdit:* SSH Brute-Force Saldırısı\n"
        f"🌍 *Saldırgan IP:* `{ip}`\n"
        f"🔢 *Başarısız Deneme:* {deneme_sayisi}\n"
        f"🛑 *Aksiyon:* {ban_mesaji}"
    )
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": mesaj, "parse_mode": "Markdown"}
    
    try:
        if "BURAYA" not in TELEGRAM_BOT_TOKEN:
            requests.post(url, json=payload, timeout=5)
    except Exception:
        pass # Hata olsa bile scriptin çalışması durmasın

def block_ip(ip):
    """
    Belirtilen IP adresini Linux Iptables kullanarak sunucudan banlar.
    """
    if ip in WHITELIST:
        print(f"[-] KORUMA: {ip} adresi beyaz listede bulunuyor, banlanmadı!")
        return False

    try:
        # iptables komutu: -A (Kural ekle), INPUT (Gelen trafik), -s (Kaynak IP), -j DROP (Paketi düşür/yok et)
        komut = ["iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"]
        
        # subprocess.run ile komutu terminalde çalıştırıyoruz
        subprocess.run(komut, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"[+] AKTİF SAVUNMA: {ip} adresi güvenlik duvarından BAŞARIYLA BANLANDI!")
        return True
    except subprocess.CalledProcessError:
        print(f"[-] Hata: {ip} adresi banlanırken iptables komutu başarısız oldu. (Root yetkisi var mı?)")
        return False
    except FileNotFoundError:
        print("[-] Hata: iptables aracı bulunamadı. Sunucunuzda farklı bir güvenlik duvarı (örn: firewalld) olabilir.")
        return False

def analyze_real_log(log_path, threshold=5):
    """
    Logları okur, saldırganı tespit eder ve aktif savunmayı tetikler.
    """
    print(f"[*] {log_path} dosyası analiz ediliyor...\n")
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
                print(f"\n[!] ALARM (BRUTE-FORCE): {ip} adresinden {sayi} adet başarısız giriş tespit edildi!")
                
                # 1. Adım: Saldırganı Banla
                ban_durumu = block_ip(ip)
                
                # 2. Adım: Durumu Telegram'a Bildir
                send_telegram_alert(ip, sayi, ban_durumu)
                
                tehlike_yok = False
                
        if tehlike_yok:
            print("[-] Eşik değeri aşan şüpheli bir IP tespit edilmedi.")
            
    except PermissionError:
        print(f"[-] Hata: Okuma yetkiniz yok. Lütfen scripti 'sudo' ile çalıştırın.")
    except Exception as e:
        print(f"[-] Beklenmeyen hata: {e}")

if __name__ == "__main__":
    print("-" * 50)
    print("  SIEM LITE - AKTİF SAVUNMA SİSTEMİ (IPS)")
    print("-" * 50)
    
    # Kendi bulut sunucun (Oracle) için log yolu
    hedeflanan_log = "/var/log/secure"      
    
    # 5 ve üzeri başarısız deneme yapanlar anında banlanır.
    analyze_real_log(hedeflanan_log, threshold=5)
