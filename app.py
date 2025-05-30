import streamlit as st
import hashlib
from firebase_setup import hash_ref
import function as fc
def get_url_hash(url):
    return hashlib.md5(url.encode()).hexdigest()

st.title('Movie Recommender System')
option = st.selectbox("Movie Database", options=['', 'Thêm phim','Tìm kiếm phim'], index=0)

if option == 'Thêm phim':
    st.subheader('Thêm phim mới')

    movie_name = st.text_input("Tên phim")
    movie_description = st.text_area("Mô tả phim")
    image_url = st.text_input("URL ảnh poster")

    if st.button("Lưu phim"):
        if not (movie_name and movie_description and image_url):
            st.warning("⚠️ Vui lòng nhập đầy đủ tên, mô tả và URL ảnh.")
        else:
            movie_hash = get_url_hash(image_url)
            uploaded_hashes = hash_ref.get() or {}

            if movie_hash in uploaded_hashes:
                st.warning("⚠️ Phim với ảnh này đã tồn tại!")
            else:
                try:
                    hash_ref.child(movie_hash).set({
                        "name": movie_name,
                        "description": movie_description,
                        "image_url": image_url
                    })
                    st.success(f"✅ Đã lưu phim {movie_name}")
                    st.image(image_url, caption=movie_name, use_container_width=True)
                except Exception as e:
                    st.error(f"❌ Lỗi ghi Firebase: {e}")

elif option == 'Tìm kiếm phim':
    text = st.text_input('Nhập mô tả của phim')
    search_option = st.radio(
        "Tìm kiếm theo:",
        ('Tên phim', 'Mô tả phim', 'Poster phim')
    )
    # Nút tìm kiếm → gọi hàm mới → lưu danh sách ID phim giống nhất vào session
    if st.button('🔍 Tìm kiếm'):
        matched_ids = fc.searchFilm(text,search_option)
        st.session_state['matched_ids'] = matched_ids

    try:
        uploaded_hashes = hash_ref.get() or {}
    except Exception as e:
        st.error(f"Lỗi khi đọc dữ liệu: {e}")
        uploaded_hashes = {}

    st.subheader("Danh sách phim")

    if not uploaded_hashes:
        st.info("Chưa có phim nào được lưu.")
    else:
        matched_ids = st.session_state.get('matched_ids', None)

        if matched_ids:
            if len(matched_ids) > 0:
                for search_id in matched_ids:
                    if search_id not in uploaded_hashes:
                        continue  # bỏ qua phim đã bị xoá

                    data = uploaded_hashes[search_id]
                    col1, col2 = st.columns([5, 1])
                    with col1:
                        st.markdown(f"### 🎬 {data.get('name', 'Không tên')}")
                        st.image(data.get('image_url', ''), use_container_width=True)
                        st.markdown(f"**Mô tả:** {data.get('description', 'Không có mô tả')}")
                    with col2:
                        if st.button(f'❌ Xóa phim', key=f'delete_{search_id}'):
                            try:
                                hash_ref.child(search_id).delete()
                                st.success(f"Đã xóa phim {data.get('name', '')}!")
                                st.session_state['matched_ids'].remove(search_id)
                                st.rerun()
                            except Exception as e:
                                st.error(f"Lỗi khi xóa: {e}")
            else:
                st.warning("Không tìm thấy phim nào phù hợp với mô tả.")
        else:
            # Hiển thị toàn bộ nếu chưa tìm hoặc vừa xoá hết matched
            for idx, (file_hash, data) in enumerate(uploaded_hashes.items(), 1):
                col1, col2 = st.columns([5, 1])
                with col1:
                    st.markdown(f"### 🎬 {data.get('name', 'Không tên')}")
                    st.image(data.get('image_url', ''), use_container_width=True)
                    st.markdown(f"**Mô tả:** {data.get('description', 'Không có mô tả')}")
                with col2:
                    if st.button(f'❌ Xóa', key=f'delete_{idx}'):
                        hash_ref.child(file_hash).delete()
                        st.success(f"Đã xóa phim {data.get('name', '')}!")
                        st.rerun()

            if st.button('🗑️ Xóa tất cả'):
                hash_ref.delete()
                st.success("Đã xóa toàn bộ phim!")
                st.rerun()

