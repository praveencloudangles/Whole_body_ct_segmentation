from data_extraction import extract_data
from PIL import Image
import requests
from io import BytesIO
import os
import pathlib
import zipfile
import random
import plotly.graph_objects as go
import numpy as np
import nibabel as nib

def open_random_gz_files(path):
    all_files = [f for f in os.listdir(path) if f.endswith('.gz')]
    random.shuffle(all_files)
    gz_files = all_files[:4]
    
    return gz_files
    
    
def convert_and_save_gz_to_jpg(gz_file, output_path):
    img = nib.load(gz_file)
    print("img-------------", img)
    data = img.get_fdata()
    
    middle_slices = [
        data[data.shape[0] // 2, :, :],
        data[:, data.shape[1] // 2, :],
        data[:, :, data.shape[2] // 2]
    ]
    
    combined_image = np.hstack(middle_slices)
    fig = go.Figure(data=go.Heatmap(z=combined_image, colorscale='Gray'))
    
    fig.update_layout(title_text='Scan Array (Middle Slices)', height=600, width=1800)
    fig.write_image(output_path)
    
    
def visualize_gz_files():
    url = extract_data()
    url_response = requests.get(url)
    with zipfile.ZipFile(BytesIO(url_response.content)) as z:
        z.extractall('.')
        
    path = os.path.join(os.getcwd(), "totalSegmentator_mergedLabel_samples/imagesTr/")
    gz_files = open_random_gz_files(path)
    print("Random .gz files:", gz_files)
    
    for i, gz_file in enumerate(gz_files):
        full_gz_path = os.path.join(path, gz_file)
        output_path = f'sample_{i}.jpg'
        convert_and_save_gz_to_jpg(full_gz_path, output_path)
        print(f"Saved {output_path}")
    
    
    return url
    
visualize_gz_files()