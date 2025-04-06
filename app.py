"""
from flask import Flask, request, render_template, send_file
from extractor import extract_main_content
import os
import lxml.html.clean

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        content = extract_main_content(url)
        
        file_path = "extracted_content.txt"
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)
        
        return render_template('index.html', content=content, file_path=file_path)
    
    return render_template('index.html', content=None)

@app.route('/download')
def download():
    file_path = "extracted_content.txt"
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return "No file available to download."

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, render_template, send_file
from extractor import extract_main_content, summarize_content
import os
import lxml.html.clean

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        content = extract_main_content(url)
        summary = summarize_content(content)
        
        file_path = "extracted_summary.txt"
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(summary)
        
        return render_template('index.html', content=summary, file_path=file_path)
    
    return render_template('index.html', content=None)

@app.route('/download')
def download():
    file_path = "extracted_summary.txt"
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return "No file available to download."

if __name__ == '__main__':
    app.run(debug=True)
    """
from flask import Flask, request, jsonify, render_template, send_file
import os
from final_web_scraper import extract_main_content, summarize_content, truncate_content

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        data = request.json
        url = data.get("url")
        
        if not url:
            return jsonify({"error": "URL is required"}), 400
        
        content = extract_main_content(url)
        truncated_content = truncate_content(content)
        summary = summarize_content(truncated_content)
        
        # Save extracted content to a file
        file_path = "extracted_content.txt"
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)
        
        return jsonify({"summary": summary, "download_url": "/download"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/download')
def download_file():
    try:
        file_path = "extracted_content.txt"
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
