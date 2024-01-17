from flask import Flask, request, render_template, redirect, url_for, after_this_request, send_file, send_from_directory
from werkzeug.utils import secure_filename, safe_join
import os
import uuid
from pdf.processing import PdfProcessor
from chatbot.chatbot import ChatBot
import threading
import time
from pdf.anonymizer import Anonymizer

app = Flask(__name__, template_folder='web/templates')
app.config['UPLOAD_FOLDER'] = './tmp'
app.config['UNPROCESSED_FILE'] = {}

# Ensure upload directory exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

chatbot = ChatBot()
anonymizer = Anonymizer()

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
    fText = anonymizer.anonymize_text(fText)
    hls = chatbot.get_highlights(fText)
    processed_path = processor.generate_highlights(hls)
    delayed_delete(file_path)

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

    file_path = safe_join(app.config['UPLOAD_FOLDER'], pdf_id + '.pdf')

    if os.path.exists(file_path) and file_path.endswith('.pdf'):
        # Function to delete the file after sending it
        @after_this_request
        def cleanup(response):
            delayed_delete(file_path)
            return response

        # Send the file and ensure it's deleted after the request
        return send_file(file_path, mimetype='application/pdf')
    else:
        return "File not found", 404
    
def delayed_delete(file_path, delay=5):
    """
    Delete the file after a specified delay.
    """
    def task():
        time.sleep(delay)  # Delay in seconds
        try:
            os.remove(file_path)
        except Exception as error:
            app.logger.error("Error removing file: %s", error)

    thread = threading.Thread(target=task)
    thread.start()


if __name__ == '__main__':
    app.run(port=8114, debug=True)