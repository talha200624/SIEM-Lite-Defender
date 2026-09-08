**🛡️ SIEM Lite - Active SSH Brute-Force Defender**

Bu proje, Linux sunucularına yönelik SSH kaba kuvvet (brute-force) saldırılarını tespit eden, sistem yöneticisine Telegram üzerinden anlık uyarı gönderen ve saldırganın IP adresini `iptables` güvenlik duvarı üzerinden otomatik olarak engelleyen hafif siklet bir IPS (Intrusion Prevention System) aracıdır.

**🚀 Özellikler**
* **Gerçek Zamanlı Log Analizi:** `/var/log/secure` üzerinden Regex ile anlık saldırgan tespiti.
* **Anlık Bildirim Sistemi:** Tehdit algılandığında Telegram API üzerinden detaylı uyarı mesajı gönderimi.
* **Aktif Savunma:** Belirlenen eşik değeri aşan IP adreslerini `iptables` ile kalıcı olarak banlama.
* **Beyaz Liste (Whitelist):** Sistem yöneticisinin kendini yanlışlıkla engellemesini önleyen koruma mekanizması.

**🛠️ Kurulum ve Kullanım**
1. Gerekli kütüphaneyi kurun: `pip install requests`
2. `siem_lite.py` içindeki `TELEGRAM_BOT_TOKEN` ve `TELEGRAM_CHAT_ID` kısımlarını kendi bilgilerinizle doldurun.
3. Kendinizi banlamamak için `WHITELIST` dizisine kendi IP adresinizi ekleyin.
4. Aracı root yetkisiyle çalıştırın: `sudo python3 siem_lite.py`

**⚠️ Yasal Uyarı**
Bu araç tamamen eğitim ve kişisel sunucu güvenliği amacıyla geliştirilmiştir. Kendi yetkiniz olmayan sistemlerde kullanmayınız.
