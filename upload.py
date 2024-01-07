from dotenv import load_dotenv
import os
import base64
import requests

def get_api_key():
    load_dotenv()
    return os.getenv("IMG_API_KEY")


def upload_image_to_imgbb(image_path):
    url='https://api.imgbb.com/1/upload'
    api_key = get_api_key()
    with open(image_path, 'rb') as file:
        image_data = base64.b64encode(file.read()).decode('utf-8')
        payload = { 'key': api_key, 'image': image_data }
        response = requests.post(url, data=payload)
        response.raise_for_status()
        return response.json()
