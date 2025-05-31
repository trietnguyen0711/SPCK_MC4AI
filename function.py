import streamlit as st
import requests
from io import BytesIO
from PIL import Image
from uform import get_model, Modality
import numpy as np
from firebase_setup import hash_ref
# Load Model Uform
processors, models = get_model('unum-cloud/uform3-image-text-multilingual-base')
model_text = models[Modality.TEXT_ENCODER]
model_image = models[Modality.IMAGE_ENCODER]
processor_text = processors[Modality.TEXT_ENCODER]
processor_image = processors[Modality.IMAGE_ENCODER]
# Tải ảnh từ firebasefirebase
# DataAll là một list chứa các thông tin của các bộ phimphim
try:
    uploaded_hashes = hash_ref.get() or {}
except Exception as e :
    st.error(f"Lỗi khi đọc dữ liệu: {e}")
    uploaded_hashes = {}
dataAll = []
dataId = []
for id,data in uploaded_hashes.items():
    dataAll.append(data)
    dataId.append(id)
# print(dataAll[0].get('description')) 

def imageGet(image_url):
    image = Image.open(BytesIO(requests.get(image_url, verify=False).content))
    image_data = processor_image(image)
    _, image_embedding = model_image.encode(image_data)
    return image_embedding
# print(imageGet(dataAll[0].get('image_url')))

def get_embedd(text):
  text_data = processor_text(text)
  _, text_embedding = model_text.encode(text_data)
  return text_embedding

def cosineSimilarity(text, img):
  return (text@img.T)/(np.linalg.norm(text)*np.linalg.norm(img))

def searchFilm(text, type):
    text_embedding = get_embedd(text)
    results = []

    for i in range(len(dataAll)):
        if type =='Tên phim':
            title_text = dataAll[i].get('name','')
            title_embedding = get_embedd(title_text)
            similarity = cosineSimilarity(text_embedding, title_embedding)
        elif type =='Mô tả phim':
            desc_text = dataAll[i].get('description', '')
            desc_embedding = get_embedd(desc_text)
            similarity = cosineSimilarity(text_embedding, desc_embedding)
        else:
            image_embedding = imageGet(dataAll[i].get('image_url'))
            similarity = cosineSimilarity(text_embedding, image_embedding)

        results.append((dataId[i], similarity))
    # Sắp xếp theo độ tương đồng cao → thấp
    results.sort(key=lambda x: x[1], reverse=True)
    return [item[0] for item in results]
# print(searchFilm(text='Vu Tru', type='Tên phim'))