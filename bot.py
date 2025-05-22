import os
import psutil
import time
from datetime import datetime
import telegram
from telegram.ext import Application, CommandHandler
import socket
import requests

# Ganti dengan token bot Telegram Anda
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

async def start(update, context):
    await update.message.reply_text(
        "Selamat datang di Bot Monitoring Server!\n\n"
        "Perintah yang tersedia:\n"
        "/sysinfo - Informasi sistem\n"
        "/memory - Penggunaan memori\n"
        "/cpu - Penggunaan CPU\n"
        "/disk - Penggunaan disk\n"
        "/network - Informasi jaringan\n"
        "/docker - Informasi Docker containers"
    )

async def sysinfo(update, context):
    # Informasi sistem
    boot_time = datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
    cpu_count = psutil.cpu_count()
    hostname = socket.gethostname()
    
    message = f"🖥 Informasi Sistem:\n\n"
    message += f"Hostname: {hostname}\n"
    message += f"Boot Time: {boot_time}\n"
    message += f"CPU Cores: {cpu_count}\n"
    message += f"OS: {os.uname().sysname} {os.uname().release}\n"
    
    await update.message.reply_text(message)

async def memory(update, context):
    # Informasi memori
    mem = psutil.virtual_memory()
    message = f"💾 Penggunaan Memori:\n\n"
    message += f"Total: {mem.total / (1024**3):.2f} GB\n"
    message += f"Tersedia: {mem.available / (1024**3):.2f} GB\n"
    message += f"Terpakai: {mem.used / (1024**3):.2f} GB\n"
    message += f"Persentase: {mem.percent}%\n"
    
    await update.message.reply_text(message)

async def cpu(update, context):
    # Informasi CPU
    cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
    message = f"⚡ Penggunaan CPU:\n\n"
    
    for i, percent in enumerate(cpu_percent):
        message += f"Core {i}: {percent}%\n"
    
    message += f"\nTotal CPU Usage: {sum(cpu_percent)/len(cpu_percent):.1f}%"
    
    await update.message.reply_text(message)

async def disk(update, context):
    # Informasi disk
    message = f"💽 Penggunaan Disk:\n\n"
    
    partitions = psutil.disk_partitions()
    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            message += f"Partition: {partition.mountpoint}\n"
            message += f"Total: {usage.total / (1024**3):.2f} GB\n"
            message += f"Terpakai: {usage.used / (1024**3):.2f} GB\n"
            message += f"Tersedia: {usage.free / (1024**3):.2f} GB\n"
            message += f"Persentase: {usage.percent}%\n\n"
        except:
            continue
    
    await update.message.reply_text(message)

async def network(update, context):
    # Informasi jaringan
    message = f"🌐 Informasi Jaringan:\n\n"
    
    # Get IP address
    try:
        ip = requests.get('https://api.ipify.org').text
        message += f"Public IP: {ip}\n\n"
    except:
        message += "Tidak dapat mengambil IP publik\n\n"
    
    # Network interfaces
    net_if = psutil.net_if_addrs()
    for interface, addrs in net_if.items():
        message += f"Interface: {interface}\n"
        for addr in addrs:
            if addr.family == socket.AF_INET:
                message += f"IPv4: {addr.address}\n"
            elif addr.family == socket.AF_INET6:
                message += f"IPv6: {addr.address}\n"
        message += "\n"
    
    await update.message.reply_text(message)

async def docker(update, context):
    # Informasi Docker
    try:
        docker_cmd = os.popen('docker ps -a').read()
        if docker_cmd:
            message = f"🐳 Informasi Docker Containers:\n\n{docker_cmd}"
        else:
            message = "Tidak ada container Docker yang berjalan"
    except:
        message = "Docker tidak terinstal atau tidak dapat diakses"
    
    await update.message.reply_text(f"```\n{message}\n```", parse_mode='Markdown')

def main():
    # Buat aplikasi
    application = Application.builder().token(TOKEN).build()

    # Tambahkan handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("sysinfo", sysinfo))
    application.add_handler(CommandHandler("memory", memory))
    application.add_handler(CommandHandler("cpu", cpu))
    application.add_handler(CommandHandler("disk", disk))
    application.add_handler(CommandHandler("network", network))
    application.add_handler(CommandHandler("docker", docker))

    # Jalankan bot
    print("Bot started...")
    application.run_polling(allowed_updates=True)

if __name__ == '__main__':
    main() 