from flask import Flask, request, jsonify, send_file
import os
import re
import logging
import pythoncom
import pdfplumber
from docx2pdf import convert
import time
import threading
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS to allow requests from other domains

# Set up logging
logging.basicConfig(level=logging.INFO)

def extract_information(text):
    date_pattern = r"\b\d{1,2} (?:Januari|Februari|Maret|April|Mei|Juni|Juli|Agustus|September|Oktober|November|Desember) \d{4}\b"
    dates = re.findall(date_pattern, text)

    if dates:
        months = {
            "Januari": "01", "Februari": "02", "Maret": "03", "April": "04",
            "Mei": "05", "Juni": "06", "Juli": "07", "Agustus": "08",
            "September": "09", "Oktober": "10", "November": "11", "Desember": "12"
        }
        extracted_date = dates[0]
        day, month_word, year = extracted_date.split()
        month = months[month_word]
        formatted_date = f"{year}-{month}-{int(day):02d}"
    else:
        formatted_date = None

    aircraft_type_pattern = r"Pesawat tipe\s+([^,]+)"
    aircraft_types = re.findall(aircraft_type_pattern, text)

    call_sign_pattern = r"call sign\s+([^,]+)"
    call_signs = re.findall(call_sign_pattern, text)

    country_pattern = r"asal ([\w\s]+)"
    countries = re.findall(country_pattern, text, re.IGNORECASE)

    results = []
    num_entries = max(len(aircraft_types), len(call_signs), len(countries))

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
    indikasi_pattern = r"I\. INDIKASI([\s\S]+?)(II\.|$)"
    match = re.search(indikasi_pattern, text, re.IGNORECASE)
    return match.group(1).strip() if match else None

@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "File not found."}), 400

    file = request.files['file']

    if not file.filename or not file.filename.endswith('.pdf'):
        return jsonify({"status": "error", "message": "Only PDF files are accepted."}), 400

    pdf_path = os.path.join('uploads', file.filename)
    file.save(pdf_path)

    try:
        full_text = extract_text_from_pdf(pdf_path)
        indikasi_text = extract_indikasi_section(full_text)

        if indikasi_text:
            extracted_info = extract_information(indikasi_text)
            return jsonify({"status": "success", "data": extracted_info})

        return jsonify({"status": "warning", "message": "Bagian 'INDIKASI' tidak ditemukan dalam dokumen."})

    except Exception as e:
        logging.error(f"Error processing PDF: {e}")
        return jsonify({"status": "error", "message": "An error occurred while processing the PDF."}), 500

    finally:
        if os.path.exists(pdf_path):
            os.remove(pdf_path)  # Cleanup

def get_unique_filename(directory, base_filename):
    """Generate a unique filename by appending a count if the file already exists."""
    count = 1
    filename, extension = os.path.splitext(base_filename)
    new_filename = base_filename

    while os.path.exists(os.path.join(directory, new_filename)):
        new_filename = f"{filename}({count}){extension}"
        count += 1

    return new_filename

@app.route('/convert', methods=['POST'])
def convert_docx_to_pdf():
    if 'file' not in request.files:
        return jsonify({'status': 'error', 'message': 'No file part'}), 400
    
    file = request.files['file']
    
    if not file.filename or not file.filename.endswith('.docx'):
        return jsonify({'status': 'error', 'message': 'File must be a DOCX'}), 400

    unique_filename = get_unique_filename('uploads', file.filename)
    filepath = os.path.join('uploads', unique_filename)
    file.save(filepath)

    pdf_filename = f"{os.path.splitext(unique_filename)[0]}.pdf"
    pdf_filepath = os.path.join('uploads', pdf_filename)

    try:
        pythoncom.CoInitialize()

        convert(filepath, pdf_filepath)

        return send_file(pdf_filepath, as_attachment=True, mimetype='application/pdf')

    except Exception as e:
        logging.error(f"Error converting DOCX to PDF: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

    finally:
        if os.path.exists(filepath):
            os.remove(filepath)

def cleanup_old_files():
    """Delete files older than 24 hours in the uploads directory."""
    current_time = time.time()
    for filename in os.listdir('uploads'):
        file_path = os.path.join('uploads', filename)
        # Check if the file is older than 1 day (86400 seconds)
        if os.path.isfile(file_path) and current_time - os.path.getmtime(file_path) > 86400:
            os.remove(file_path)
            logging.info(f"Deleted old file: {filename}")

def run_cleanup():
    """Run the cleanup function periodically."""
    while True:
        cleanup_old_files()
        time.sleep(3600)  # Run every hour

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    pythoncom.CoInitialize()  # Initialize COM once when the app starts
    
    # Start the cleanup thread
    cleanup_thread = threading.Thread(target=run_cleanup)
    cleanup_thread.daemon = True  # Daemonize thread
    cleanup_thread.start()

    app.run(debug=True)
