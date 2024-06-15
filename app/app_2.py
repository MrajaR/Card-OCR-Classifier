from flask import Flask,render_template, request
import socket
from flask import jsonify
import cv2
import numpy as np
import ocr_2
import easyocr
from tensorflow.keras.models import load_model
import tensorflow as tf
from PIL import Image


import json

app = Flask(__name__)

reader = easyocr.Reader(lang_list=['id'], detector='dbnet18')
resnet_model = load_model('app/detection_model/card_classifier.h5')

@app.route('/', methods=['GET'])
def index():
    return "Hello, ngetes OCR."

@app.route('/api/ocr', methods=['POST'])
def upload_image():
    try:
            image_file = request.files['image']
            
            # Read the image data from the uploaded file
            img_data = image_file.read()

            # Convert binary data to numpy array
            img = cv2.imdecode(np.frombuffer(img_data, np.uint8), cv2.IMREAD_UNCHANGED)

            # Convert the NumPy array to a TensorFlow tensor
            img_tensor = tf.convert_to_tensor(img, dtype=tf.float32)

            # Resize the image using TensorFlow function
            resized_img = tf.image.resize(img_tensor, (256, 256))
            
            # Expand dimensions if needed
            input_image = tf.expand_dims(resized_img, axis=0)

            # Assuming 'resnet_model' is your pre-trained ResNet model
            yhat = resnet_model.predict(input_image)

            labels = {0 : 'kis',
                    1 : 'ktp',
                    2 : 'npwp'}

            prediction_index = np.argmax(yhat)
            # print("Predicted Class Index:", labels[prediction_index])

            if prediction_index == 0:
                ocr_result_json = ocr_2.read_ocr_bpjs(img, reader)
                json.loads(ocr_result_json)

                return jsonify({'code': 200,
                        'message': 'Success to read ocr',
                        'errors':None,
                        'data': json.loads(ocr_result_json)})
            
            elif prediction_index == 1:
                ocr_result_json = ocr_2.read_ocr_ktp(img, reader)
                json.loads(ocr_result_json)
                print(ocr_result_json)

                return jsonify({'code': 200,
                        'message': 'Success to read ocr',
                        'errors':None,
                        'data': json.loads(ocr_result_json)})
            
            elif prediction_index == 2:
                 ocr_result_json = ocr_2.read_ocr_npwp(img, reader)
                 json.loads(ocr_result_json)
                 print(ocr_result_json)

                 return jsonify({'code': 200,
                                 'message': 'Success to read ocr',
                                 'errors': None,
                                 'data': json.loads(ocr_result_json)})
            
    except Exception as e:
        error_message = str(e)
        return jsonify({'code': 200,
                        'message': 'file not supported, please upload image file',
                        'errors':error_message,
                        'data': None})
                 


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)