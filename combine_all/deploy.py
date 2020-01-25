from flask import Flask, render_template
from flask import jsonify
from flask import request
import numpy as np
import base64
from io import BytesIO
import pickle
from PIL import Image
import cv2
from run_model1 import infer_all

import warnings
warnings.filterwarnings("ignore")

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

def decd(b64_string):
    # reconstruct image as an numpy array
    image = Image.open(BytesIO(base64.b64decode(b64_string)))
    img = np.array(image)
    return img

def encd(img):
    
    pil_img = Image.fromarray(img.astype('uint8'))
    buff = BytesIO()
    pil_img.save(buff, format="png")
    image = base64.b64encode(buff.getvalue()).decode("utf-8")
    return image

inf_=infer_all()
app=Flask(__name__,template_folder='static')

@app.route('/',methods=["GET"])
def home():
    return render_template('index.html')

@app.route('/app',methods=["GET"])
def app_home():
    return render_template('app.html')

@app.route('/capture',methods=['POST'])
def capture():
    image=request.form['img']
    
    img=decd(image[22:])
    
    img=img[:,:,:3]
    
    im,flag,wt=inf_.predict(img)

    

    im=cv2.cvtColor(im,cv2.COLOR_BGR2RGB)
    im=encd(im)

    flag=cv2.cvtColor(flag,cv2.COLOR_BGR2RGB)
    flag=encd(flag)
    
    return jsonify({'img':im,'traffic':flag,'weather':wt})

if __name__ == '__main__':
    app.run(debug=True)