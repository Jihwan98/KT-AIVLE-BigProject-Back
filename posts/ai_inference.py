import tensorflow as tf
from tensorflow.keras.applications.inception_v3 import preprocess_input
from PIL import Image
import numpy as np

def binary_model_inference(data_io, input_shape=(299, 299)):
    model = tf.keras.models.load_model('posts/ai_models/binary_model.h5')
    img = preprocess_input(np.array(Image.open(data_io).resize(input_shape))[np.newaxis, :, :, :3])
    binary_result = 1 - model.predict(img)[0][0] # 모델 결과 0이 유증상, 1이 무증상이어서 반대로 표현하기 위해 빼줌
    return binary_result

labels = ['구진, 플라크', '비듬, 각질, 상피성잔고리', '태선화, 과다색소침착', '농포, 여드름', '미란, 궤양', '결절, 종괴']
def class_model_inference(data_io, input_shape=(299, 299)):
    model = tf.keras.models.load_model('posts/ai_models/first_model.h5')
    img = preprocess_input(np.array(Image.open(data_io).resize(input_shape))[np.newaxis, :, :, :3])
    class_result = model.predict(img)[0]
    disease_result = labels[np.argmax(class_result)]
    confidence = max(class_result)
    return f"{confidence * 100:0.2f}%의 확률로 [{disease_result}]이/가 예상됩니다."
