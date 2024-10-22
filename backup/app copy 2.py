from flask import Flask, request, jsonify
import pdfplumber
import re
import os
import datetime

app = Flask(__name__)

def extract_information(text):
    # Ekstraksi semua tanggal (dd MM yyyy atau dd-MM-yyyy)
    date_pattern = r"\b\d{1,2} (?:Januari|Februari|Maret|April|Mei|Juni|Juli|Agustus|September|Oktober|November|Desember) \d{4}\b"
    dates = re.findall(date_pattern, text)

    # Jika tanggal ditemukan, konversi ke format MySQL (YYYY-MM-DD)
    if dates:
        months = {
            "Januari": "01", "Februari": "02", "Maret": "03", "April": "04", "Mei": "05", "Juni": "06",
            "Juli": "07", "Agustus": "08", "September": "09", "Oktober": "10", "November": "11", "Desember": "12"
        }
        extracted_date = dates[0]  # Ambil tanggal pertama
        day, month_word, year = extracted_date.split()
        month = months[month_word]
        formatted_date = f"{year}-{month}-{int(day):02d}"  # Format YYYY-MM-DD
    else:
        formatted_date = None

    # Ekstraksi semua tipe pesawat, termasuk yang ada dalam tanda kurung
    aircraft_type_pattern = r"Pesawat tipe\s+([^,]+)"
    aircraft_types = re.findall(aircraft_type_pattern, text)

    # Ekstraksi semua call sign
    call_sign_pattern = r"call sign\s+([^,]+)"
    call_signs = re.findall(call_sign_pattern, text)

    # Ekstraksi semua asal negara
    country_pattern = r"asal ([\w\s]+)"
    countries = re.findall(country_pattern, text, re.IGNORECASE)

    # Gabungkan semua informasi menjadi list of dictionaries
    results = []
    num_entries = max(len(aircraft_types), len(call_signs), len(countries))  # Ambil panjang maksimum

    for i in range(num_entries):
        result = {
            "Tanggal": formatted_date,
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
            full_text += page.extract_text() or ''
        return full_text

def extract_indikasi_section(text):
    # Cari bagian "INDIKASI"
    indikasi_pattern = r"I\. INDIKASI([\s\S]+?)(II\.|$)"  # Ambil teks di antara "INDIKASI" dan "ANALISIS" (atau akhir dokumen)
    match = re.search(indikasi_pattern, text, re.IGNORECASE)
    return match.group(1).strip() if match else None

@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "File not found."}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No file selected."}), 400

    # Simpan file ke server
    pdf_path = os.path.join('uploads', file.filename)
    file.save(pdf_path)

    # Ekstraksi teks dari PDF
    full_text = extract_text_from_pdf(pdf_path)

    # Ambil bagian "INDIKASI" saja
    indikasi_text = extract_indikasi_section(full_text)
    # print(indikasi_text)

    if indikasi_text:
        # Ekstraksi informasi dari teks "INDIKASI"
        extracted_info = extract_information(indikasi_text)
        # print(extracted_info)
        response = {
            "data": extracted_info
        }
    else:
        response = {
            "message": "Bagian 'INDIKASI' tidak ditemukan dalam dokumen."
        }

    # Hapus file setelah diproses (opsional)
    os.remove(pdf_path)

    return jsonify(response)

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)  # Buat folder uploads jika belum ada
    app.run(debug=True)
