import time
from pywifi import PyWiFi, const, Profile 

#  start 
def Scaning():
    wifi = PyWiFi()
    ift = wifi.interfaces()[0] # ift singkatan dari interface muka 

    # scaning wifi 
    ift.scan()
    time.sleep(10) # kasih jeda waktu 10s

    hasil = ift.scan_results() # temukan wifi kasil

    # deteksi dan urutkan sesuai kekuatan jaringan 
    UrJarSin = sorted(hasil, key=lambda x: x.signal, reverse=True) 

    for jarinagn in hasil:
        print(f"SSID : {jarinagn.ssid} \n Sinyal : {jarinagn.signal}")

        return UrJarSin, ift
# melakukan koneksi
def Connect(ift, ssid, password):
    print("pengembangan!")


if __name__ == "__main__":
    Scaning()
