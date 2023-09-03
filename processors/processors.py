import pandas as pd
import random
import nltk
from nltk.corpus import wordnet
import cv2
import numpy as np
import base64
import os
import shutil
import zipfile
import tempfile


def augment_tabular_data(data_frame, noise_std=0.1):
    augmented_data = data_frame.copy()
    numeric_columns = augmented_data.select_dtypes(include=["number"]).columns

    for column in numeric_columns:
        augmented_data[column] += np.random.normal(
            0, noise_std, size=len(augmented_data)
        )

    return augmented_data


def augment_image(image, rotation_angle=30):
    height, width = image.shape[:2]
    center = (width / 2, height / 2)
    rotation_matrix = cv2.getRotationMatrix2D(
        center, random.uniform(-rotation_angle, rotation_angle), 1.0
    )
    augmented_image = cv2.warpAffine(image, rotation_matrix, (width, height))

    return augmented_image


"""
All processors have a run method

This run methods applies every augmentation techniques defined by the processor on the data           
"""
