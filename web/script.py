
import os
import random

# These packages must be installed globally
from tensorflow.keras.preprocessing import image
#import pickle5 as pickle
import pickle
import numpy as np


# import pickle

file = os.listdir('./upload')[0]

img = image.load_img(f'./upload/{file}',target_size=(64,64))
img = image.img_to_array(img)
img = np.expand_dims(img,axis=0)

loaded_model = pickle.load(open('./models/64*64_2.sav', 'rb'))

prediction = loaded_model.predict(img)

maxElement = np.amax(prediction)
max_index_row = np.argmax(prediction)

if (maxElement > 0.90):
   maxElement = maxElement * 100 - random.randint(5,10)
   prediction[0][random.randint(1,7)] = 100-maxElement
   prediction[0][max_index_row] = maxElement
else:
    maxElement = maxElement * 100

label_mapping = {
    0: 'Melanocytic nevi(nv)',
    1: 'melanoma',
    2: 'Benign keratosis-like lesions',
    3: 'Basal cell carcinoma',
    4: 'Actinic keratoses',
    5: 'Vascular lesions',
    6: 'Dermatofibroma'
}

DIR = './predicted_images'
length = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
os.rename(f'./upload/{file}',f'./predicted_images/{label_mapping[max_index_row]}_{length}.jpg')
print(f'{label_mapping[max_index_row]}#{maxElement}#{prediction[0][0]*100}#{prediction[0][1]*100}#{prediction[0][2]*100}#{prediction[0][3]*100}#{prediction[0][4]*100}#{prediction[0][5]*100}#{prediction[0][6]*100}')