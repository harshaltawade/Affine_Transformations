import streamlit as st
import numpy as np
from PIL import Image
import math

# Transformation functions

def translate_image(image, tx, ty):
    width, height = image.size
    translated_image = Image.new("RGB", (width, height))

    for x in range(width):
        for y in range(height):
            new_x = x - tx
            new_y = y - ty

            if 0 <= new_x < width and 0 <= new_y < height:
                pixel = image.getpixel((new_x, new_y))
                translated_image.putpixel((x, y), pixel)

    return translated_image

def rotate_image(image, angle_degrees):
    angle_radians = math.radians(angle_degrees)
    width, height = image.size
    new_width = int(abs(width * math.cos(angle_radians)) + abs(height * math.sin(angle_radians)))
    new_height = int(abs(width * math.sin(angle_radians)) + abs(height * math.cos(angle_radians)))

    rotated_image = Image.new("RGB", (new_width, new_height))

    for x in range(new_width):
        for y in range(new_height):
            src_x = int((x - new_width / 2) * math.cos(angle_radians) - (y - new_height / 2) * math.sin(angle_radians) + width / 2)
            src_y = int((x - new_width / 2) * math.sin(angle_radians) + (y - new_height / 2) * math.cos(angle_radians) + height / 2)

            if 0 <= src_x < width and 0 <= src_y < height:
                pixel = image.getpixel((src_x, src_y))
                rotated_image.putpixel((x, y), pixel)

    return rotated_image

def reflect_image(image, horizontal=True):
    width, height = image.size
    reflected_image = Image.new("RGB", (width, height))

    for x in range(width):
        for y in range(height):
            if horizontal:
                src_x = width - 1 - x
                src_y = y
            else:
                src_x = x
                src_y = height - 1 - y

            pixel = image.getpixel((src_x, src_y))
            reflected_image.putpixel((x, y), pixel)

    return reflected_image

def shear_image(image, shear_factor_x, shear_factor_y):
    width, height = image.size
    sheared_width = max(1, int(width + shear_factor_x * height))
    sheared_height = height

    sheared_image = Image.new("RGB", (sheared_width, sheared_height))

    for x in range(sheared_width):
        for y in range(sheared_height):
            src_x = max(0, x - int(shear_factor_x * y))
            src_y = y

            if 0 <= src_x < width and 0 <= src_y < height:
                pixel = image.getpixel((src_x, src_y))
                sheared_image.putpixel((x, y), pixel)

    return sheared_image

def scale_image(image, scale_factor):
    width, height = image.size
    scaled_width = int(width * scale_factor)
    scaled_height = int(height * scale_factor)

    scaled_image = Image.new("RGB", (scaled_width, scaled_height))

    for x in range(scaled_width):
        for y in range(scaled_height):
            src_x = int(x / scale_factor)
            src_y = int(y / scale_factor)

            if 0 <= src_x < width and 0 <= src_y < height:
                pixel = image.getpixel((src_x, src_y))
                scaled_image.putpixel((x, y), pixel)

    return scaled_image

# Streamlit app
st.title("Image Transformations")
st.write("Upload an image and choose a transformation:")

uploaded_image = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])
if uploaded_image is not None:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    transformation_type = st.selectbox("Select Transformation", ["Translate", "Rotate", "Reflect", "Shear", "Scale"])
    if transformation_type == "Translate":
        tx = st.slider("Translation X", -400, 400, 0)
        ty = st.slider("Translation Y", -400, 400, 0)
        if st.button("Apply Translation"):
            transformed_image = translate_image(image, tx, ty)
            st.image(transformed_image, caption="Translated Image", use_column_width=True)

    elif transformation_type == "Rotate":
        angle_degrees = st.slider("Rotation Angle (degrees)", -180.0, 180.0, 0.0)
        if st.button("Apply Rotation"):
            transformed_image = rotate_image(image, angle_degrees)
            st.image(transformed_image, caption="Rotated Image", use_column_width=True)

    elif transformation_type == "Reflect":
        horizontal = st.checkbox("Horizontal Reflection")
        if st.button("Apply Reflection"):
            transformed_image = reflect_image(image, horizontal)
            st.image(transformed_image, caption="Reflected Image", use_column_width=True)

    elif transformation_type == "Shear":
        shear_factor_x = st.slider("Shearing Factor X", -2.0, 2.0, 0.0)
        shear_factor_y = st.slider("Shearing Factor Y", -2.0, 2.0, 0.0)
        if st.button("Apply Shearing"):
            transformed_image = shear_image(image, shear_factor_x, shear_factor_y)
            st.image(transformed_image, caption="Sheared Image", use_column_width=True)

    elif transformation_type == "Scale":
        scale_factor = st.slider("Scaling Factor", 0.1, 5.0, 1.0)
        if st.button("Apply Scaling"):
            transformed_image = scale_image(image, scale_factor)
            st.image(transformed_image, caption="Scaled Image", use_column_width=True)
