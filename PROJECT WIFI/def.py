import sys, time, os
from pywifi import PyWiFi
from scapy.all import *
from scapy.all import ARP, Ether, srp
from tabulate import tabulate


def scan():
    wifi = PyWiFi()
    ifnt = wifi.interact()

    ifnt.scan()
    time.sleep(5)

    hasil = ifnt.scan_results()
    uj = sorted(hasil, key=lambda x: x.signal, reverse=True)

    data = [[i + 1, jaringan.ssid, jaringan.signal] for i, jaringan, in enumerate(uj)]
    print(tabulate(data, headers=["NO", "SSID", "SIGNAL"], tablefmt="heavy_grid"))

    try:
        sy = int(input("\n Masukkan nomor jaringan yang ingin di scan : ".format(len(hasil))))

        if 1 <= sy <= len(hasil):
            jaringanGW = hasil[sy -1]
            print(f"\n SSID : ", {jaringanGW.ssid}, "SIGNAL : ", {jaringanGW.signal})

            print("Jika anda ingin mulai brute force ketik (y/n) n untuk exit")
            attack = input("Silahkan masukan Pilihan : ").lower()

            if attack == "y":
                return GasAttack()
            else:
                return "Terimakasih!"
        else:
            print("Pilihan Tidak Ada Di Menu!")
            os.system("cls" if os.name == "nt" else "clear")
            return scan()

    except ValueError: 
        print("mberoh")

def GasAttack():
    pass


if __name__ == "__main__":
    scan()