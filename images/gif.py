import streamlit as st
from auth.login import login_user
from dashboard.admin import admin_dashboard



# =====================================================
#create gif and save it
# =====================================================
from PIL import Image

# Images ka path
image_paths = [
    r"C:\Users\user\Desktop\BBAU\images\ambedkarbhawan.jpeg",
    r"C:\Users\user\Desktop\BBAU\images\Babasaheb-Bhimrao-Ambedkar-University-Lucknow-Campus-View-2.jpg",
    r"C:\Users\user\Desktop\BBAU\images\download.webp",
    r"C:\Users\user\Desktop\BBAU\images\OIP.webp",
]

frames = []

# Sab images ko same size me convert karenge
SIZE = (1920, 1080)

for path in image_paths:
    img = Image.open(path).convert("RGB")
    img = img.resize(SIZE, Image.LANCZOS)
    frames.append(img)

# GIF save
output_path = r"C:\Users\user\Desktop\BBAU\images\bbau_watermark.gif"

frames[0].save(
    output_path,
    save_all=True,
    append_images=frames[1:],
    duration=3000,   # 3000 ms = 3 seconds per image
    loop=0           # Infinite loop
)
