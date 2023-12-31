# -*- coding: utf-8 -*-
"""Resize & Merge.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1yNCKJIL4qCvJcPVKBJGruAPT5sUymjqo
"""

import os
import cv2
import pywt
import numpy as np
import matplotlib.pyplot as plt

# Input folder path that contains the images
input_folder_path = '/content/drive/MyDrive/Severe'

# Output folder path to save the fused images
output_folder_path = '/content/drive/MyDrive/Output'

# Common size for all images
width = 224
height = 224

# Get list of all image filenames in the folder
img_fn = [os.path.join(input_folder_path, filename) for filename in os.listdir(input_folder_path) if filename.endswith('.jpg') or filename.endswith('.png')]

# Read in and resize all the images
img_list = []
for fn in img_fn:
    try:
        img = cv2.imread(fn)
        img = cv2.resize(img, (width, height))
        img_list.append(img)
    except Exception as e:
        print(f"Error: could not read or resize image {fn}")
        print(e)

# Pairwise merge
for i in range(0, len(img_list)-1, 2):
    img1 = img_list[i]
    img2 = img_list[i+1]
    coeffs1 = pywt.dwt2(img1, 'haar')
    coeffs2 = pywt.dwt2(img2, 'haar')
    LL = (coeffs1[0] + coeffs2[0])/2
    LH = (coeffs1[1][:-1,:-1] + coeffs2[1][:-1,:-1])/2
    HL = (coeffs1[2][:-1,:-1] + coeffs2[2][:-1,:-1])/2
    HH = (coeffs1[3][:-1,:-1] + coeffs2[3][:-1,:-1])/2
    fused_coeffs = (LL, (LH, HL), HH)
    fused_img = pywt.idwt2(fused_coeffs, 'haar')
    # Save the fused image to output folder
    out_fn = f"fusion_{i}-{i+1}.png"
    cv2.imwrite(os.path.join(output_folder_path, out_fn), fused_img)
    # Display the fused image
    img = cv2.imread(os.path.join(output_folder_path, out_fn))
    if img is not None:
        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        plt.show()
    else:
        print(f"Error: could not read image {out_fn}")

