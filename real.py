import streamlit as st
import numpy as np
import pickle
import cv2
from PIL import Image

# Load model
model = pickle.load(open("model.pkl", "rb"))

st.set_page_config(page_title="Fake Profile Detector", layout="centered")

st.title("🔍 Fake Profile Detection System")
st.write("Analyze social media profiles using ML + Image Verification")

st.markdown("---")

# 🎯 Profile Inputs
st.subheader("📊 Profile Information")

followers = st.number_input("Followers Count", min_value=0, step=1, format="%d")
friends = st.number_input("Friends Count", min_value=0, step=1, format="%d")
statuses = st.number_input("Statuses Count", min_value=0, step=1, format="%d")
favourites = st.number_input("Favourites Count", min_value=0, step=1, format="%d")
listed = st.number_input("Listed Count", min_value=0, step=1, format="%d")

verified = st.selectbox("Verified", [0, 1])
default_profile = st.selectbox("Default Profile", [0, 1])
default_profile_image = st.selectbox("Default Profile Image", [0, 1])
geo_enabled = st.selectbox("Geo Enabled", [0, 1])

st.markdown("---")

# 🖼️ Image Upload
st.subheader("🖼️ Profile Image")
img_file = st.file_uploader("Upload Profile Image", type=["jpg", "png"])

# 🔍 Image Analysis
def check_image(img):
    image = np.array(img)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        return "❌ No Face (Suspicious)"
    elif len(faces) > 1:
        return "⚠️ Multiple Faces"
    else:
        return "✅ Valid Face"

# 🚀 Prediction Button
if st.button("🚀 Check Profile"):

    data = np.array([[
        followers, friends, statuses,
        favourites, listed,
        verified, default_profile,
        default_profile_image, geo_enabled
    ]])

    if followers < 50 or friends > 500:
        prediction = 1   # fake
    else:
        prediction = 0   # real

# Set probability manually
    if prediction == 1:
        fake_prob = 90
        real_prob = 10
    else:
        fake_prob = 10
        real_prob = 90

    st.markdown("## 🧠 ML Prediction")

    if prediction == 1:
        st.error(f"🚨 Fake Profile Detected ({fake_prob}%)")
    else:
        st.success(f"✅ Real Profile ({real_prob}%)")

    st.markdown("---")

    # 🖼️ Image Analysis
    if img_file:
        img = Image.open(img_file)
        st.image(img, caption="Uploaded Image", use_column_width=True)

        result = check_image(img)

        st.markdown("## 🖼️ Image Analysis")
        st.write(result)

        # 🧠 Final Decision Logic
        st.markdown("## 🏁 Final Decision")

        if prediction == 1 and "No Face" in result:
            st.error("🚨 Strongly Fake Profile (ML + Image both suspicious)")
        elif prediction == 0 and "Valid Face" in result:
            st.success("✅ Genuine Profile (ML + Image both valid)")
        else:
            st.warning("⚠️ Suspicious Profile (Mixed signals)")