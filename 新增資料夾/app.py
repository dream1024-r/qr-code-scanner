import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.title("📷 QR Code 掃描器 - OpenCV 版")

uploaded_file = st.file_uploader("請上傳 QR Code 圖片", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # 讀取圖片，統一轉成 RGB 三通道
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="上傳的圖片", use_container_width=True)

    # 轉換為 OpenCV 格式 (BGR)
    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # 建立 QR Code 偵測器
    detector = cv2.QRCodeDetector()

    # 嘗試偵測多個 QR Code
    try:
        result = detector.detectAndDecodeMulti(img)
        if result is not None and len(result) == 3:
            data_list, bbox_list, _ = result
        else:
            data_list, bbox_list = [], None
    except:
        data_list, bbox_list = [], None

    # 如果 detectAndDecodeMulti 沒找到，改用 detectAndDecode
    if not data_list or (isinstance(data_list, list) and all(d == "" for d in data_list)):
        try:
            single_data, bbox, _ = detector.detectAndDecode(img)  # 支援新版本
            if single_data:
                data_list = [single_data]
                bbox_list = [bbox]
        except:
            data_list, bbox_list = [], None

    # 顯示結果 + 畫框框
    if data_list and any(d for d in data_list):
        output_img = img.copy()
        for i, data in enumerate(data_list):
            if data:
                st.success(f"🔍 偵測到 QR Code {i+1}：{data}")
                if bbox_list is not None:
                    if isinstance(bbox_list, list) and bbox_list[0] is not None:
                        points = np.int32(bbox_list[i]).reshape(-1, 2)
                        cv2.polylines(output_img, [points], True, (0, 255, 0), 3)

        # 顯示標記後的圖片
        st.image(cv2.cvtColor(output_img, cv2.COLOR_BGR2RGB), caption="📍 偵測結果", use_container_width=True)
    else:
        st.error("❌ 沒有偵測到 QR Code")
