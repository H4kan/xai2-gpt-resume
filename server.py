from flask import Flask, request, render_template, redirect, url_for, send_from_directory, Response
from werkzeug.utils import secure_filename
import os
import uuid
from pdf.processing import PdfProcessor
from chatbot.chatbot import ChatBot

app = Flask(__name__, template_folder='web/templates')
app.config['UPLOAD_FOLDER'] = './tmp'
app.config['UNPROCESSED_FILE'] = {}

chatbot = ChatBot()

@app.route('/')
def index():
    return send_from_directory('web', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('web', path)

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and file.filename.endswith('.pdf'):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            unique_id = str(uuid.uuid4())
            app.config['UNPROCESSED_FILE'][unique_id] = file_path

            return redirect(url_for('display_data', id=unique_id))
    return redirect(request.url)

@app.route('/display/<id>', methods=['GET'])
def display_data(id):
    file_path = app.config['UNPROCESSED_FILE'].get(id, "No data found.")
    processor = PdfProcessor(file_path)
    fText = processor.scrap_text()
    hls = chatbot.get_highlights(fText)
    processed_path = processor.generate_highlights(hls)

    data = {
        'fText': fText,
        'hls': hls,
        'processed_path': processed_path
    }

    return render_template('display.html', data=data)

@app.route('/pdf/<pdf_id>')
def serve_pdf(pdf_id):
    if '/' in pdf_id or '\\' in pdf_id:
        return "Invalid file path", 400

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_id + '.pdf')
    if os.path.exists(file_path) and file_path.endswith('.pdf'):
        return send_from_directory(app.config['UPLOAD_FOLDER'], pdf_id + '.pdf', mimetype='application/pdf')
    else:
        return "File not found", 404

def process_pdf(file_path):
    # Your PDF processing and data extraction logic
    return "Extracted Data from PDF"


if __name__ == '__main__':
    app.run(port=8114, debug=True)