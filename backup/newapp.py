import pdfplumber
import re

def extract_information(text):
    # Ekstraksi semua tanggal (dd MM yyyy atau dd-MM-yyyy)
    date_pattern = r"\b\d{1,2} (?:Januari|Februari|Maret|April|Mei|Juni|Juli|Agustus|September|Oktober|November|Desember) \d{4}\b"
    dates = re.findall(date_pattern, text)

    # Ekstraksi semua tipe pesawat, termasuk yang ada dalam tanda kurung
    aircraft_type_pattern = r"Pesawat tipe ([\w\s\-]+ \[\w+\])"
    aircraft_types = re.findall(aircraft_type_pattern, text, re.IGNORECASE)
        # aircraft_type_pattern = r"Pesawat tipe ([\w\s\-]+ [\[\(]\w+[\]\)])"
    # aircraft_types = re.findall(aircraft_type_pattern, text, re.IGNORECASE)

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

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        full_text = ''
        for page in pdf.pages:
            full_text += page.extract_text()
        return full_text

def extract_indikasi_section(text):
    # Cari bagian "INDIKASI"
    indikasi_pattern = r"I\. INDIKASI([\s\S]+?)(II\.|$)"  # Ambil teks di antara "INDIKASI" dan "ANALISIS" (atau akhir dokumen)
    match = re.search(indikasi_pattern, text, re.IGNORECASE)
    return match.group(1).strip() if match else None

# Path ke file PDF yang diunggah
pdf_path = 'dokumen/Lapin_30_September_2024_Indikasi_Pelanggaran_Penerbangan_di_Wilayah_Teritorial_Udara_Indone.pdf'

# Ekstraksi teks dari PDF
full_text = extract_text_from_pdf(pdf_path)

# Ambil bagian "INDIKASI" saja
indikasi_text = extract_indikasi_section(full_text)

print()
print(indikasi_text)
print()

if indikasi_text:
    # Ekstraksi informasi dari teks "INDIKASI"
    extracted_info = extract_information(indikasi_text)

    # Output
    for i, info in enumerate(extracted_info, start=1):
        print(f"Pesawat {i}:")
        for key, value in info.items():
            print(f"  {key}: {value}")
        print()
else:
    print("Bagian 'INDIKASI' tidak ditemukan dalam dokumen.")
