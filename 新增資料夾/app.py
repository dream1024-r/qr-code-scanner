import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.title("📷 QR Code 掃描器 - OpenCV 版")

uploaded_file = st.file_uploader("請上傳 QR Code 圖片", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # 讀取圖片
    image = Image.open(uploaded_file)
    st.image(image, caption="上傳的圖片", use_container_width=True)

    # 轉換為 OpenCV 格式
    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # 建立 QR Code 偵測器
    detector = cv2.QRCodeDetector()

    # 嘗試偵測多個 QR Code
    result = detector.detectAndDecodeMulti(img)

    data_list, bbox_list = [], None
    if isinstance(result, tuple):
        if len(result) == 3:
            data_list, bbox_list, _ = result
        elif len(result) == 2:
            data_list, bbox_list = result

    # 如果沒找到，改用 detectAndDecode (單一)
    if not data_list or (isinstance(data_list, list) and all(d == "" for d in data_list)):
        single_data, bbox = detector.detectAndDecode(img)
        if single_data:
            data_list = [single_data]
            bbox_list = [bbox]

    # 繪製框框並顯示結果
    if data_list_
