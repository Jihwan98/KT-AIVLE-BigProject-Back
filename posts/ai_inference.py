import tensorflow as tf
from PIL import Image
import numpy as np


labels = ['A1 구진 플라크', 'A2 비듬 각질 상피성잔고리', 'A3 태선화 과다색소침착', 'A4 농포 여드름', 'A5 미란 궤양', 'A6 결절 종괴']

def ai_model_inference(data_io, input_shape=(299, 299)):
    model = tf.keras.models.load_model('posts/ai_models/first_model.h5')
    img = np.array(Image.open(data_io).resize(input_shape))[np.newaxis, :]
    y_index = np.argmax(model.predict(img)[0])
    return labels[y_index]
