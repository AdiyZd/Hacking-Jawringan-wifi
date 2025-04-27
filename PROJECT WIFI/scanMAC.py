from scapy.all import ARP, Ether, srp
import scapy.all as scapy
import requests
import socket
from tabulate import tabulate

def Device_hp(ip):
    try:
        hostname, _, _ = socket.gethostbyaddr(ip)
        return hostname
    except socket.herror:
        return "Mberoh Hp Ne Opo"

def macFUNDER(mac):
    url = f"https://api.macvendors.com/{mac}"
    try:
        response_url = requests.get(url=url)
        if response_url.status_code == 200:
            return response_url.text
        else:
            return "I DONT KNOW COK!"
    except:
        return "Requests Error!"

def scan(Jaringan_Target):
    # membuat paket arp requests agar dapat menemukan perangkat dalam jaringan 
    arp_req = scapy.ARP(pdst=Jaringan_Target)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff") # brotkes paket ke semua ajringan
    paket = ether / arp_req
    send_paket = srp(paket, timeout=5, verbose=False)[0]

    # send
    # print(" IP addresess\t\t MAC addreses\t\t Device Name")
    # print("=" * 80)

    data = []

    for i, Jar in send_paket:
        ip = Jar.psrc
        mac = Jar.hwsrc
        vendor = macFUNDER(mac)
        Device = Device_hp(ip)
        data.append([ip, mac, vendor, Device])

    # Tampilkan Hasil Scaning
    print(tabulate(data, headers=["IP ADDRESS", "MAC ADDRESS", "VEMDOR", "DEVICE NAME"], tablefmt="heavy_grid"))

#  KONTROL ADMIN
Jaringan_Target = "192.168.1.0/24"
scan(Jaringan_Target) 

