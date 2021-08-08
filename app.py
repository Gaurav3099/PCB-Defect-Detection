from flask import *
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage

from tensorflow.keras.models import load_model
from keras.preprocessing import image
import numpy as np
import os


model = load_model('model.h5')
UPLOAD_FOLDER = './static'

def load_image(img_path):
    img=image.load_img(img_path, target_size=(244, 244))
    img_tensor=image.img_to_array(img)
    img_tensor=np.expand_dims(img_tensor, axis=0)
    img_tensor /= 255.
    return img_tensor

def prediction(img_path):
    new_image=load_image(img_path)
    pred=model.predict(new_image)
    # print(pred)
    
    labels = np.array(pred)
    labels[labels>=0.6]=1
    labels[labels<0.6]=0
    
    # print(labels)
    res = np.array(labels)
    
    if res[0][0]==1:
        return "Bad"
    else:
        return "Good"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  

  
@app.route('/')  
def customer():  
   return render_template('page1.html')  
  
@app.route('/success',methods = ['POST', 'GET'])  
def print_data():
	f = request.files['img']
	path = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
	f.save(path)

	fn=path
	result=prediction(fn)

	return render_template('page2.html', result = f.filename, pred=result)

if __name__ == '__main__':  
   app.run(debug = True)