from locust import HttpUser, TaskSet, task
import pandas as pd
from glob import glob
import json
import numpy as np
from PIL import Image
import numpy as np

class MetricsLocust(HttpUser):

    def on_start(self):
       	self.test_files =  glob("train/*")
       	self.test_size = len(self.test_files)

        # Compose a JOSN Predict request (send the image tensor).
        jpeg_rgb = Image.open(self.test_files[0])
        # Normalize and batchify the image
        jpeg_rgb = np.expand_dims(np.array(jpeg_rgb) / 255.0, 0).tolist()
        
        self.image_data = json.dumps({'instances': jpeg_rgb})


    @task()
    def post_metrics(self):
        headers = {'Content-Type': 'application/json',}

        self.client.post("/test1", headers=headers, data=self.image_data)