import numpy as np
import streamlit as st

st.title('Movie Recommender System')
if 'uploaded_img' not in st.session_state:
    st.session_state['uploaded_img'] = []
option = st.selectbox(
    "Movie DatabaseDatabase",
    options = ['','Tải ảnh lên', 'Xem ảnh đã tải'],
    index = 0
)
if option == 'Tải ảnh lên':
    st.subheader('Tải ảnh lên')
    uploaded_files = st.file_uploader(
        "Chọn images",
        type=["jpg", "jpeg", "png"],
        key= 'img_uploader',
        accept_multiple_files=True
    )
    if uploaded_files and st.button('Tải ảnh lên') :
        for uploaded_file in uploaded_files:
            if uploaded_file not in st.session_state['uploaded_img']:   
                st.session_state['uploaded_img'].append(uploaded_file) 
                st.image(uploaded_file, caption='Ảnh đã tải lên', use_container_width=True)
            else:
                st.warning(f'Ảnh {uploaded_file.name} đã tồn tại trong hệ thống')
elif option == 'Xem ảnh đã tải':
    st.subheader("Ảnh đã tải lên")
    for idx, img in enumerate(st.session_state['uploaded_img'], 1):
        col1, col2 = st.columns([4, 1])
            
        with col1:
            st.image(img, caption=f'Ảnh {idx}: {img.name}', use_container_width=True)
        with col2:
            if st.button(f'Xóa ảnh {idx}', key=f'delete_{idx}'):
                st.session_state['uploaded_img'].remove(img)
                st.success(f'Đã xóa ảnh {img.name}!')
                st.rerun()  

    if st.button('Xóa tất cả ảnh', key='delete_all'):
        st.session_state['uploaded_img'] = []
        st.success('Đã xóa tất cả ảnh!')
        st.rerun()  
        