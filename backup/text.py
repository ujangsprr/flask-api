
import pdfplumber

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        full_text = ''
        for page in pdf.pages:
            full_text += page.extract_text()
        return full_text

# Path ke file PDF yang diunggah
pdf_path = 'dokumen/Lapin_30_September_2024_Indikasi_Pelanggaran_Penerbangan_di_Wilayah_Teritorial_Udara_Indone.pdf'

# Ekstraksi teks dari PDF
full_text = extract_text_from_pdf(pdf_path)

# Output hasil ekstraksi teks dari PDF
full_text[:2000]  # Menampilkan 2000 karakter pertama dari teks yang diekstraksi
print(full_text)