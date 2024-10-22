import re

def extract_information(text):
    # Ekstraksi semua tanggal (dd MM yyyy atau dd-MM-yyyy)
    date_pattern = r"\b\d{1,2} (?:Januari|Februari|Maret|April|Mei|Juni|Juli|Agustus|September|Oktober|November|Desember) \d{4}\b"
    dates = re.findall(date_pattern, text)

    # Ekstraksi semua tipe pesawat
    aircraft_type_pattern = r"Pesawat tipe ([\w\s\-()]+)"
    aircraft_types = re.findall(aircraft_type_pattern, text, re.IGNORECASE)

    # Ekstraksi semua call sign
    call_sign_pattern = r"call sign (\w+)"
    call_signs = re.findall(call_sign_pattern, text)

    # Ekstraksi semua asal negara
    country_pattern = r"pesawat militer asal ([\w\s]+)"
    countries = re.findall(country_pattern, text, re.IGNORECASE)

    # Gabungkan semua informasi menjadi list of dictionaries
    results = []
    for i in range(len(aircraft_types)):  # Gunakan panjang dari aircraft_types
        result = {
            "Tanggal": dates[0] if dates else None,  # Asumsikan semua data berada di tanggal yang sama
            "Tipe Pesawat": aircraft_types[i] if i < len(aircraft_types) else None,
            "Call Sign": call_signs[i] if i < len(call_signs) else None,
            "Asal Negara": countries[i] if i < len(countries) else None
        }
        results.append(result)
    
    return results

# Contoh teks
# text = """
# Pada 2 Oktober 2024, berdasarkan pantauan sistem ADS-B (Automatic Dependent Surveillance Broadcast), diperoleh informasi pesawat yang terindikasi melakukan pelanggaran penerbangan di wilayah udara teritorial Indonesia, sebagai berikut:
# 1. Pesawat tipe BOEING [P8], dengan call sign KIW775, jenis pesawat militer asal Timor Leste. Pesawat lepas landas pada pukul 04.26 WIB dari Bandar Udara Internasional Adelaide, Australia dengan tujuan tidak diketahui. Pesawat memasuki wilayah udara Indonesia melalui Laut Banda sekitar pukul 08.53 WIB dengan mematikan radar.
# 2. Pesawat tipe POSEIDON [P9], dengan call sign KIW776, jenis pesawat militer asal Papua Nugini. Pesawat lepas landas pada pukul 04.26 WIB dari Bandar Udara Internasional Adelaide, Australia dengan tujuan tidak diketahui. Pesawat memasuki wilayah udara Indonesia melalui Laut Banda sekitar pukul 08.53 WIB dengan mematikan radar.
# 3. Pesawat tipe P-8A [P10], dengan call sign KIW778, jenis pesawat militer asal Malaysia. Pesawat lepas landas pada pukul 04.26 WIB dari Bandar Udara Internasional Adelaide, Australia dengan tujuan tidak diketahui. Pesawat memasuki wilayah udara Indonesia melalui Laut Banda sekitar pukul 08.53 WIB dengan mematikan radar.
# 4. Pesawat tipe P-9S [P11], dengan call sign KUY778, jenis pesawat militer asal Malaysia. Pesawat lepas landas pada pukul 04.26 WIB dari Bandar Udara Internasional Adelaide, Australia dengan tujuan tidak diketahui. Pesawat memasuki wilayah udara Indonesia melalui Laut Banda sekitar pukul 08.53 WIB dengan mematikan radar.
# """

text = """
Pada 30 September 2024, berdasarkan pantauan sistem ADS-B (Automatic
Dependent Surveillance Broadcast), diperoleh informasi pesawat yang terindikasi
melakukan pelanggaran penerbangan di wilayah udara teritorial Indonesia,
sebagai berikut:
1. Pesawat tipe LOCKHEED C-130H HERCULES [C130], dengan call sign
KIW681, jenis pesawat militer asal New Zealand. Pesawat lepas landas pada
pukul 09.03 WIB dari Bandar Udara Butterworth, Malaysia dengan tujuan tidak
diketahui. Pesawat tersebut memasuki wilayah udara Indonesia pada pukul
11:13 WIB melalui Selat Karimata, dan menghilang dari pantauan radar di
sekitar Sungai Putri pada pukul 11.47 WIB. Kemudian terdeteksi kembali oleh
radar di sekitar Parang Batang pada pukul 12.28 WIB.
2. Pesawat tipe BOEING C-17A GLOBEMASTER III (C17), dengan call sign
BLOCKED, jenis pesawat militer asal Australia. Pesawat lepas landas pada
pukul 10.21 WIB dari Bandara Internasional Tan Son Nhat, Vietnam dengan
tujuan tidak diketahui. Pesawat tersebut memasuki wilayah udara Indonesia di
sekitar Kalimantan Utara pada pukul 11.56 WIB kemudian menghilang dari
pantauan radar di sekitar Poso pada pukul 12.48 WIB. Pesawat terdeteksi
kembali oleh radar di sekitar Laut Banda pada pukul 13.51 WIB, kemudian
keluar wilayah udara Indonesia melalui Laut Timur.
"""

# Ekstraksi informasi
extracted_info = extract_information(text)

# Output
for i, info in enumerate(extracted_info, start=1):
    print(f"Pesawat {i}:")
    for key, value in info.items():
        print(f"  {key}: {value}")
    print()
