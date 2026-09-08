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




**🛡️ SIEM Lite - Active SSH Brute-Force Defender**

This project is a lightweight IPS (Intrusion Prevention System) tool that detects SSH brute-force attacks targeting Linux servers, sends instant alerts to the system administrator via Telegram, and automatically blocks the attacker's IP address using the 'iptables' firewall.

**🚀 Features**

* **Real-Time Log Analysis:** Instant attacker detection using Regex on '/var/log/secure'.

* **Instant Notification System:** Sends detailed alert messages via the Telegram API when a threat is detected.

* **Active Defense:** Permanently bans IP addresses that exceed the defined threshold using 'iptables'.

* **Whitelist:** A protection mechanism that prevents system administrators from accidentally blocking their own IP addresses.

**🛠️ Installation and Usage**

1. Install the required library: 'pip install requests'

2. Fill in the 'TELEGRAM_BOT_TOKEN' and 'TELEGRAM_CHAT_ID' variables in 'siem_lite.py' with your own information.

3. Add your own IP address to the 'WHITELIST' array to avoid banning yourself.

4. Run the tool with root privileges: 'sudo python3 siem_lite.py'

**⚠️ Disclaimer**
This tool is developed strictly for educational and personal server security purposes. Do not use it on systems you are not authorized to manage.
