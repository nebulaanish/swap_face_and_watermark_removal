import os
import cv2
import numpy as np
import requests
FACESWAP_API_KEY = ""   # Obtained from rapidapi
EDENAI_API_KEY = "" # Obtained from edenai
CLIPDROP_API_KEY = ""   # Obtained from clipdrop website



def face_swap(image_url, face_url):
    url = "https://faceswap-image-transformation-api.p.rapidapi.com/faceswap"
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": FACESWAP_API_KEY,
        "X-RapidAPI-Host": "faceswap-image-transformation-api.p.rapidapi.com"
    }

    payload = {
        "TargetImageUrl": image_url,
        "SourceImageUrl": face_url
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        result_url = response.json().get('ResultImageUrl')
        return result_url
    except requests.RequestException as e:
        error_message = f"Error calling external API 1: {e}"
        print(error_message)
        return image_url
    
    # For testing purpose to save api calls
    # result = "https://i.ibb.co/44s61sb/image.jpg"
    # return result

def download_image(result_url, save_path):
    try: 
        response = requests.get(result_url, stream=True)
        response.raise_for_status()
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
    except requests.RequestException as e:
        print(f"Error downloading image: {e}")
        return None

def create_mask(result_url, result_path, mask_path):
    mask_width, mask_height = get_dimensions(result_path)
    response = detect_logo(result_path)
    mask = np.zeros((mask_height, mask_width, 4), dtype=np.uint8)
    mask[:, :, 3] = 0  
    vertices = response["google"]["items"][0]["bounding_poly"]["vertices"]
    vertices_array = np.array([(point["x"], point["y"]) for point in vertices], dtype=np.int32)
    vertices_array = vertices_array.reshape((-1, 1, 2))
    cv2.fillPoly(mask, [vertices_array], color=(255, 255, 255, 255)) 
    cv2.imwrite(mask_path, mask)
    

def get_dimensions(image_path):
    image = cv2.imread(image_path)

    if image is not None:
        height, width = image.shape[:2]
        return width, height
    else:
        print("Couldn't load image")
        return None

def detect_logo(result_path):

    headers = {"Authorization": f"Bearer {EDENAI_API_KEY}"}
    url = "https://api.edenai.run/v2/image/logo_detection"
    data = {
        "providers": "google",
        "fallback_providers": ""
    }
    files = {'file': open(result_path, 'rb')}
    response = requests.post(url, data=data, files=files, headers=headers)
    return response.json()

def remove_watermark(image_path, mask_path, final_result_path):
    image_name = os.path.basename(image_path)
    mask_name = os.path.basename(mask_path)
    with open(image_path, "rb") as f:
        image_file_object = f.read()
    with open(mask_path, "rb") as f:
        mask_file_object = f.read()
    r = requests.post('https://clipdrop-api.co/cleanup/v1',
    files = {
        'image_file': (image_name, image_file_object, 'image/jpeg'),
        'mask_file': (mask_name, mask_file_object, 'image/png')
        },
    headers = { 'x-api-key':CLIPDROP_API_KEY }
    )
    print(f"Watermark Api response: ")
    if (r.ok):
        with open(final_result_path, 'wb') as output_file:
            output_file.write(r.content)
        return r.content
    else:
        print("Watermark Error")
        r.raise_for_status()
        
def image_to_b64(image_path):
    with open(image_path, "rb") as f:
        image_file_object = f.read()
    return image_file_object