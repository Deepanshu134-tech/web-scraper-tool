from flask import Flask, render_template, request, send_file, redirect, url_for
import os
from datetime import datetime
from scraper import WebScraper

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        if not url:
            return render_template('index.html', error="Please enter a URL")
        
        scraper = WebScraper()
        data, error = scraper.scrape_url(url)
        
        if error:
            return render_template('index.html', error=error)
        
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        domain = url.split('//')[-1].split('/')[0].replace('.', '_')
        filename = f"scrape_{domain}_{timestamp}.csv"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        success, csv_error = scraper.create_csv(data, filepath)
        if not success:
            return render_template('index.html', error=csv_error)
        
        return render_template('index.html', 
                             success=f"Successfully scraped data!",
                             download_url=url_for('download_file', filename=filename))
    
    return render_template('index.html')

@app.route('/download/<filename>')
def download_file(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)