from __future__ import print_function

from flask import Flask, render_template, flash, request
from os import environ

import base64
import io
import json
import time

import numpy as np
from PIL import Image
import requests

from send_queue import RabbitMqClient

app = Flask(__name__)

time.sleep(20)
rabbitmq_client = RabbitMqClient()

def tfserving_request(IMAGE_URL, model_name): #1

    """
    Should change to grpc from json

    """

    # The server URL specifies the endpoint of your server running the ResNet
    # model with the name "resnet" and using the predict interface.
    SERVER_URL = 'http://resnet-cluster-ip-service:8501/v1/models/resnet_classification:predict'

    # Current Resnet model in TF Model Garden (as of 7/2021) does not accept JPEG
    # as input
    MODEL_ACCEPT_JPG = False

    dl_request = requests.get(IMAGE_URL, stream=True)
    dl_request.raise_for_status()


    if MODEL_ACCEPT_JPG:
        # Compose a JSON Predict request (send JPEG image in base64).
        jpeg_bytes = base64.b64encode(dl_request.content).decode('utf-8')
        predict_request = '{"instances" : [{"b64": "%s"}]}' % jpeg_bytes
    else:
        # Compose a JOSN Predict request (send the image tensor).
        jpeg_rgb = Image.open(io.BytesIO(dl_request.content))
        # Normalize and batchify the image
        jpeg_rgb = np.expand_dims(np.array(jpeg_rgb) / 255.0, 0).tolist()
        predict_request = json.dumps({'instances': jpeg_rgb})


    answer = rabbitmq_client.call(predict_request)
    
    print("sender_answer:", answer)

    # response = requests.post(SERVER_URL, data=predict_request)
    # response.raise_for_status()
    #prediction = response['predictions'][0]

    return np.argmax(answer)

@app.route("/",methods=["GET","POST"])
@app.route("/home",methods=["GET","POST"]) #1
def home():
    if request.method == "POST": #2
        # resnet_classification is the model name
        IMAGE_URL = request.form["IMAGE_URL"]
        response = tfserving_request(IMAGE_URL, "resnet_classification") #4

        flash(f"Predicted class for {IMAGE_URL} is  {response}", 'success') #6

    return render_template("index.html") #7

@app.route("/test",methods=["GET","POST"]) #1
def test():
    if request.method == "POST": #2
        # resnet_classification is the model name
        SERVER_URL1 = 'http://resnet-cluster-ip-service:8501/v1/models/resnet_classification:predict'

        SERVER_URL2 = 'http://resnetalt-cluster-ip-service:8501/v1/models/resnet_classification:predict'

        predict_request = json.dumps(request.json)
        response = requests.post(SERVER_URL1, data=predict_request)
        response.raise_for_status() 
        prediction = response.json()['predictions'][0]

        return str(prediction)

app.secret_key = "nlhkjtgjhfhvhjfyfgcjgdtdgcngcghdt"
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(environ.get('PORT', 8080)))

