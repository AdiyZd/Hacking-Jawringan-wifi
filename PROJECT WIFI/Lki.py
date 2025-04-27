import os
import time

# Konfigurasi
interface = "wlxd46e0e0afd07"  # Ganti dengan interface WiFi yang benar
mac_address = "c2:e1:79:23:ae:04"  # Ganti dengan MAC Address target

download_limit = "1kbit"  # Batas kecepatan download
upload_limit = "1kbit"  # Batas kecepatan upload

def setup_bandwidth_limit():
    """Mengatur limit bandwidth menggunakan tc dan iptables."""
    
    # Hapus aturan sebelumnya agar tidak konflik
    os.system(f"tc qdisc del dev {interface} root 2>/dev/null")
    os.system(f"iptables -t mangle -D PREROUTING -m mac --mac-source {mac_address} -j MARK --set-mark 10 2>/dev/null")
    
    # Tambahkan aturan baru
    os.system(f"tc qdisc add dev {interface} root handle 1: htb default 30")
    os.system(f"tc class add dev {interface} parent 1: classid 1:1 htb rate {download_limit} ceil {upload_limit}")
    os.system(f"tc class add dev {interface} parent 1:1 classid 1:30 htb rate {download_limit} ceil {upload_limit}")
    
    # Gunakan iptables untuk memfilter MAC address dan beri tanda (mark)
    os.system(f"iptables -t mangle -A PREROUTING -m mac --mac-source {mac_address} -j MARK --set-mark 10")
    
    # Hubungkan tc dengan iptables mark
    os.system(f"tc filter add dev {interface} protocol ip parent 1:0 prio 1 handle 10 fw flowid 1:1")
    
    print(f"✅ Bandwidth untuk {mac_address} dibatasi: {download_limit} Download / {upload_limit} Upload")

def remove_bandwidth_limit():
    """Menghapus limit bandwidth yang sudah dibuat."""
    os.system(f"tc qdisc del dev {interface} root")
    os.system(f"iptables -t mangle -D PREROUTING -m mac --mac-source {mac_address} -j MARK --set-mark 10 2>/dev/null")
    
    print(f"❌ Limit bandwidth untuk {mac_address} telah dihapus.")

def countdown_timer(seconds):
    """Menampilkan hitungan mundur di terminal."""
    while seconds > 0:
        menit, detik = divmod(seconds, 60)
        print(f"\r⏳ Waktu tersisa: {menit:02d}:{detik:02d}", end="")
        time.sleep(1)
        seconds -= 1
    print("\n⏳ Waktu habis!")

try:
    # Input waktu limit
    menit = int(input("Masukan Durasi Limit (dalam menit): "))
    detik = int(input("Masukan Durasi Limit (dalam detik): "))

    # Konversi ke detik
    waktu_limit = (menit * 60) + detik
    print(f"⚡ Bandwidth akan dibatasi selama {menit} menit {detik} detik...\n")

    # Terapkan limit
    setup_bandwidth_limit()
    
    # Jalankan hitungan mundur
    countdown_timer(waktu_limit)
    
    # Hapus limit setelah waktu habis
    remove_bandwidth_limit()

except ValueError:
    print("❌ Masukkan angka yang valid!")
