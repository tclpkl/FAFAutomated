from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from image_processing import process_FAF
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['PROCESSED_FOLDER'] = 'static/processed'

@app.route('/')
def index():
    # Home page where users upload 768x768 .tif FAF images
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if request.method == 'POST':

        # Getting user uploaded file and filename 
        file = request.files['file']
        filename = secure_filename(file.filename)

        # Making filepath for where user uploaded file goes 
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Saving file to filepath 
        file.save(filepath)

        # Processing photo with helper function and getting output filepath of processed image and measurement metric 
        processed_image, measurements = process_image(filepath, filename)

        # Render results.html with following attributes
        return render_template('results.html', processed_image=processed_image, measurements=measurements)

def process_image(filepath, filename):

    # Making output filepath for processed image
    output_path = filename.split(".")[0] + "_PROCESSED.png"
    processed_image_path = os.path.join(app.config['PROCESSED_FOLDER'], output_path)
    
    # Given input photo file path, output processed image to output filepath and return proportion deteriorated 
    percent_deterioration = process_FAF(input_filepath=filepath, output_filepath=processed_image_path)
    return processed_image_path, percent_deterioration

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))