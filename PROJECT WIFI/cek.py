from pywifi import PyWiFi

wifi = PyWiFi()
ift = wifi.interfaces()

donggle_name = "wlxd46e0e0afd07" # linux saya dengan donggle tp link 300mbps

ifc = None
for iface in ift:
    if iface.name() == donggle_name:
        ift = iface
        break

if ift is None:
    print(f"WIfi tidak ada yang terdeteksi!!!")
else:
    print(f"Gunakan Interface: {ift.name()}")


# AKTIVKAN INI DAN NONAKTIVKAN SRIPT YANG ADA DI ATAS UNTUK CEK DONGGLE
# for i, iface in enumerate(ift):
#     print(f"{i}: {iface.name()}")