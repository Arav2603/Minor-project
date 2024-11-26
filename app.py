from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.vgg16 import preprocess_input  # Correct import
import numpy as np
import os
import tempfile  # To handle temporary files

app = Flask(__name__)
CORS(app)  # Enable cross-origin requests

# Ensure the path to the model file is correct
MODEL_PATH = 'model/autism_model1.h5'

# Check if the model file exists
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")

# Load the trained model
model = load_model(MODEL_PATH)

@app.route('/')
def index():
    # Serve the HTML file for the frontend
    return send_from_directory('./templates', 'index.html')


@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']  # Uploaded file

    if file:
        try:
            # Save the file temporarily
            with tempfile.NamedTemporaryFile(delete=True) as temp_file:
                file.save(temp_file.name)  # Save uploaded file to temp path

                # Load the image for prediction
                img = load_img(temp_file.name, target_size=(224, 224))
                img_array = img_to_array(img)                        # Convert image to array
                img_array = np.expand_dims(img_array, axis=0)        # Add batch dimension
                img_array = preprocess_input(img_array)             # Preprocess image

                # Make prediction using the model
                prediction = model.predict(img_array)

                print("Raw Model Output:", prediction)  # Log raw prediction

                # Interpret the prediction result
                threshold = 0.5
                result = 'Autistic' if prediction[0][0] > threshold else 'Non-Autistic'

                return jsonify({'prediction': result, 'raw_output': float(prediction[0][0])})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Invalid file format'}), 400


if __name__ == '__main__':
    app.run(debug=True)
