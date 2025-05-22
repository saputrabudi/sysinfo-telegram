# Bot Monitoring Server

Bot Telegram untuk monitoring informasi sistem server, termasuk penggunaan CPU, memori, disk, dan informasi jaringan.

## Fitur

- Monitoring CPU usage
- Monitoring penggunaan memori
- Monitoring penggunaan disk
- Informasi jaringan
- Informasi sistem
- Status Docker containers

## Instalasi

1. Pastikan Python 3.x dan pip sudah terinstal
2. Buat virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependensi:
   ```bash
   pip install python-telegram-bot psutil requests
   ```

## Konfigurasi

1. Buat bot Telegram baru melalui [@BotFather](https://t.me/botfather)
2. Dapatkan token bot
3. Edit file `bot.py` dan ganti `YOUR_TELEGRAM_BOT_TOKEN` dengan token yang didapat dari BotFather

## Penggunaan

1. Aktifkan virtual environment:
   ```bash
   source venv/bin/activate
   ```

2. Jalankan bot:
   ```bash
   python bot.py
   ```

3. Di Telegram, mulai chat dengan bot dan gunakan perintah berikut:
   - `/start` - Menampilkan menu bantuan
   - `/sysinfo` - Informasi sistem
   - `/memory` - Penggunaan memori
   - `/cpu` - Penggunaan CPU
   - `/disk` - Penggunaan disk
   - `/network` - Informasi jaringan
   - `/docker` - Informasi Docker containers

## Menjalankan sebagai Service

1. Buat file service systemd:
   ```bash
   nano /etc/systemd/system/sysinfo-bot.service
   ```

2. Isi dengan konfigurasi berikut:
   ```ini
   [Unit]
   Description=Telegram System Information Bot
   After=network.target

   [Service]
   Type=simple
   User=root
   WorkingDirectory=/root/sysinfo
   Environment=PATH=/root/sysinfo/venv/bin
   ExecStart=/root/sysinfo/venv/bin/python /root/sysinfo/bot.py
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

3. Aktifkan dan jalankan service:
   ```bash
   systemctl enable sysinfo-bot
   systemctl start sysinfo-bot
   ``` 

## by Saputra Budi
