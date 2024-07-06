import tensorflow as tf
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
model = tf.keras.models.load_model(r'C:\Users\sanja\Downloads\model (1).h5', compile=False)
# print(model.summary())
model.compile(optimizer='adam', loss=tf.keras.losses.BinaryCrossentropy(), metrics=['accuracy'])

im = Image.open(r'C:\Users\sanja\Downloads\Normal- (1008).jpg') 
# im = Image.open(r'C:\Users\sanja\Downloads\Tumor- (1003).jpg') 
newsize = (128, 128)

im = im.resize(newsize)
img = np.asarray(im)
print(img.shape)
plt.imshow(img)
plt.show()
l1 = np.ones(shape=(1,))
l0 = np.zeros(shape=(1,))
img = np.expand_dims(img, axis=0)
print(img.shape)
print(model.predict(img))
# print(model.evaluate(img, l1))
# print(model.evaluate(img, l0))

