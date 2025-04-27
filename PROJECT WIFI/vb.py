from scapy.all import srp, Ether, ARP

def get_mac(ip):
    ans, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip), timeout=2, verbose=True)
    for sent, received in ans:
        return received.hwsrc
    return None

target_ip = "192.168.1.6"  # Sesuaikan dengan target
mac = get_mac(target_ip)
print(f"MAC Address: {mac}" if mac else "[!] Gagal mendapatkan MAC Address!")
