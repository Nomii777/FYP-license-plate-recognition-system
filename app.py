from flask import Flask, render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
from detect import detect_license_plate
from recognize import recognize_plate_text
from flask import send_from_directory
import uuid
from datetime import datetime


app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'mp4', 'avi', 'mov'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/image', methods=['GET', 'POST'])
def process_image():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            unique_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(filepath)
            
            # Detect license plate
            plate_image_path = detect_license_plate(filepath)
            
            if plate_image_path:
                # Recognize text from plate
                plate_info = recognize_plate_text(plate_image_path)
                
                return render_template('results.html', 
                                    original_image=unique_filename,
                                    plate_image=os.path.basename(plate_image_path),
                                    plate_info=plate_info)
            else:
                flash('No license plate detected')
                return redirect(request.url)
    
    return render_template('image.html')

@app.route('/video', methods=['GET', 'POST'])
def process_video():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            unique_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(filepath)
            
            # Process video (this would be more complex in reality)
            # For demo, we'll just use the first frame
            plate_results = process_video_file(filepath)
            
            return render_template('results.html', 
                                  original_video=unique_filename,
                                  plate_results=plate_results)
    
    return render_template('video.html')

def process_video_file(video_path):
    # This is a simplified version - in reality you'd process multiple frames
    import cv2
    vidcap = cv2.VideoCapture(video_path)
    success, image = vidcap.read()
    
    results = []
    if success:
        # Save first frame as image
        frame_filename = f"frame_{os.path.basename(video_path).split('.')[0]}.jpg"
        frame_path = os.path.join(app.config['UPLOAD_FOLDER'], frame_filename)
        cv2.imwrite(frame_path, image)
        
        # Detect and recognize
        plate_image_path = detect_license_plate(frame_path)
        if plate_image_path:
            plate_info = recognize_plate_text(plate_image_path)
            results.append({
                'frame': frame_filename,
                'plate_image': os.path.basename(plate_image_path),
                'plate_text': plate_info['text'],
                'registration_info': plate_info['registration_info']  

            })
    
    return results

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)