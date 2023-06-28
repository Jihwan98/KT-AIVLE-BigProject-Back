import tensorflow as tf
from tensorflow.keras.applications.inception_v3 import preprocess_input
from PIL import Image
import numpy as np

labels = ['무증상', '구진, 플라크', '비듬, 각질, 상피성잔고리', '태선화, 과다색소침착', '농포, 여드름', '미란, 궤양', '결절, 종괴']
def class_model_inference(data_io, input_shape=(299, 299)):
    model = tf.keras.models.load_model('posts/ai_models/model_7class.h5')
    img = preprocess_input(np.array(Image.open(data_io).resize(input_shape))[np.newaxis, :, :, :3])
    class_result = model.predict(img)[0]
    disease_result = labels[np.argmax(class_result)]
    confidence = max(class_result) * 100
    # return f"{confidence * 100:0.2f}%의 확률로 [{disease_result}]이/가 예상됩니다."
    return disease_result, confidence