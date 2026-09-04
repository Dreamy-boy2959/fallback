import os
import streamlit as st
from PIL import Image
import requests

# --- CẤU HÌNH ---
RUNPOD_ENDPOINT_URL = "https://api.runpod.ai/v2/l1qe1g4du8a97b/runsync"  # Thay URL RunPod của bạn
RUNPOD_API_KEY = "YOUR_RUNPOD_API_KEY"                                     # Thay API Key của bạn

# Thư mục chứa ảnh gốc trên laptop (Ví dụ: thư mục 'images' nằm cùng cấp với app.py)
LOCAL_IMAGE_DIR = "./Keyframe" 

st.title("🔍 Local Video/Image Search (GPU RunPod)")
st.write("Hệ thống tính toán vector trên RunPod, hiển thị ảnh trực tiếp từ ổ cứng laptop.")

# Ô nhập từ khóa tìm kiếm
search_type = st.selectbox("Chọn loại tìm kiếm (searchType):", ["text", "image"])
query = st.text_input("Nhập từ khóa tìm kiếm (q):", "ví dụ: chiếc xe đỏ")

if st.button("Tìm kiếm"):
    if not query:
        st.warning("Vui lòng nhập từ khóa tìm kiếm!")
    else:
        with st.spinner("Đang gửi yêu cầu lên RunPod để tính toán vector..."):
            try:
                # 1. Gửi request lên RunPod Serverless
                headers = {
                    "Authorization": f"Bearer {RUNPOD_API_KEY}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "input": {
                        "searchType": search_type,
                        "q": query
                    }
                }
                
                response = requests.post(RUNPOD_ENDPOINT_URL, json=payload, headers=headers)
                data = response.json()
                
                # Xử lý kết quả trả về từ RunPod (chỉ chứa tên file và ID)
                output = data.get("output", {})
                results = output.get("result", [])
                
                if not results:
                    st.info("Không tìm thấy kết quả phù hợp.")
                else:
                    st.success(f"Tìm thấy {len(results)} kết quả!")
                    
                    # 2. Laptop tự duyệt qua tên file và load ảnh từ ổ cứng local
                    cols = st.columns(3) # Hiển thị dạng lưới 3 cột
                    for idx, item in enumerate(results):
                        file_name = item.get("file_name") # Ví dụ: "folder/frame_01.jpg"
                        video_id = item.get("id")
                        
                        local_path = os.path.join(LOCAL_IMAGE_DIR, file_name)
                        
                        with cols[idx % 3]:
                            if os.path.exists(local_path):
                                # Load và hiển thị ảnh bằng PIL và Streamlit
                                img = Image.open(local_path)
                                st.image(img, caption=f"ID: {video_id}\nFile: {file_name}", use_column_width=True)
                            else:
                                st.error(f"Thiếu file local:\n`{file_name}`")
                                
            except Exception as e:
                st.error(f"Đã xảy ra lỗi kết nối tới RunPod: {e}")
