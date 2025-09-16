import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.title("📷 QR Code 掃描器 - OpenCV 版")

# 上傳圖片
uploaded_file = st.file_uploader("請上傳 QR Code 圖片", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # 確保轉成 RGB
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="上傳的圖片", use_container_width=True)

    # 轉換為 OpenCV 格式
    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # 建立 QR Code 偵測器
    detector = cv2.QRCodeDetector()

    # 使用 detectAndDecodeMulti 支援多個 QR Code
    data_list, bbox_list, _ = detector.detectAndDecodeMulti(img)

    if bbox_list is not None:
        # 畫出每個 QR Code 的框線
        for bbox in bbox_list:
            pts = np.int32(bbox).reshape(-1, 2)
            for i in range(len(pts)):
                pt1 = tuple(pts[i])
                pt2 = tuple(pts[(i + 1) % len(pts)])
                cv2.line(img, pt1, pt2, (0, 255, 0), 3)

        # 顯示結果圖片
        st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), caption="偵測結果", use_container_width=True)

    # 顯示解碼結果
    if data_list:
        st.success("✅ 偵測到以下 QR Code：")
        for i, d in enumerate(data_list, start=1):
            st.write(f"**QR Code {i}**：{d}")
    else:
        st.error("❌ 沒有偵測到 QR Code")
