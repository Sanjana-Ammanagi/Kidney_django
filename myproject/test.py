import tensorflow as tf
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import os
model = tf.keras.models.load_model(r'C:\Users\sanja\Downloads\model (1).h5', compile=False)
# print(model.summary())
model.compile(optimizer='adam', loss=tf.keras.losses.BinaryCrossentropy(), metrics=['accuracy'])

# im = Image.open(r'C:\Users\sanja\Downloads\Normal- (1008).jpg') 
# # im = Image.open(r'C:\Users\sanja\Downloads\Tumor- (1003).jpg') 
# newsize = (128, 128)

# im = im.resize(newsize)
# img = np.asarray(im)
# print(img.shape)
# plt.imshow(img)
# plt.show()
# l1 = np.ones(shape=(1,))
# l0 = np.zeros(shape=(1,))
# img = np.expand_dims(img, axis=0)
# print(img.shape)
# print(model.predict(img))
# print(model.evaluate(img, l1))
# print(model.evaluate(img, l0))
def process_image_with_model(file_path):
    try:
       
        im = Image.open(file_path)  
        newsize = (128, 128)
        im = im.resize(newsize)
        img = np.asarray(im)
        img = np.expand_dims(img, axis=0)
        
        
        prediction = model.predict(img)
        
        
        threshold = 0.5  
        if prediction[0][0] >= threshold:
            result = {"prediction": "yes"}
        else:
            result = {"prediction": "no"}
        
        
        os.remove(file_path)
        
        return result
    except Exception as e:
        print(f"Error processing image: {e}")
        return {"error": str(e)}