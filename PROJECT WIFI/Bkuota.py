import os

USER_IP = "192.168.1.100"
QUOTA_MB = 500  # Maksimum kuota dalam MB

def get_usage():
    result = os.popen(f"iptables -L -v -n | grep {USER_IP}").read()
    if result:
        data = result.split()
        bytes_used = int(data[1])  # Kolom ke-2 adalah jumlah bytes
        mb_used = bytes_used / (1024 * 1024)
        return mb_used
    return 0

def block_user():
    os.system(f"iptables -A INPUT -s {USER_IP} -j DROP")
    os.system(f"iptables -A OUTPUT -d {USER_IP} -j DROP")
    print(f"Pengguna {USER_IP} telah mencapai batas kuota {QUOTA_MB} MB dan diblokir.")

# Monitor penggunaan
while True:
    usage = get_usage()
    print(f"Penggunaan saat ini: {usage:.2f} MB")
    if usage > QUOTA_MB:
        block_user()
        break
