import time, os, sys
from pywifi import PyWiFi, const, Profile

# sebelom start
if os.name == "nt": # windows 
    os.system("cls")
else: # linux dan mac
    os.system("clear")

#  start 
def Scaning():
    wifi = PyWiFi()
    ift = wifi.interfaces()[1]    # inisialisasi wifi

    # linux saya dengan adapter
    name = "wlxd46e0e0afd07"

    # scaning wifi 
    ift.scan()
    time.sleep(10) # kasih jeda waktu 10s

    hasil = ift.scan_results() # temukan

    # deteksi dan urutkan sesuai kekuatan jaringan 
    UrJarSin = sorted(hasil, key=lambda x: x.signal, reverse=True) 

    for index, jaringan in enumerate(UrJarSin, start=1):
        print(f"{index}.SSID : {jaringan.ssid}, Signal : {jaringan.signal} dBm")


    
    
    return UrJarSin, ift
# koneksi ke jaringan target

def koneksi(ift, ssid, password):

    profile = Profile()
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP # JENIS ENSKRIPSI
    profile.key = password

    ift.remove_all_network_profiles() # hapus semua profile jaringan
    profile = ift.add_network_profile(profile) # tambahkan profile baru

    ift.connect(profile) # percobaan koneksi ke jaringan
    time.sleep(7) # tunggu proses koneksi 

    if ift.status() == const.IFACE_CONNECTED:
        print(f"Berhasil Terhubung ke SSID : {ssid}")
    else:
        print(f"Tidak Dapat Terhubung ke SSID : {ssid}")


if __name__ == "__main__":
    # CONTROLLER ADMIN
    jaringan_list, ift = Scaning()
    if jaringan_list:
        pilihan = int(input("\n Pilih Nomor Jaringan Yang Ingin Di Sambung : ")) -1
        ssid = jaringan_list[pilihan].ssid
        password = input(f"\nSilahkan Masukan Password Nya : ")
        koneksi(ift, ssid, password)

    else:
        print("Tidak Ada Jaringan Yang Di Temukan!!!")



