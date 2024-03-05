import json
import requests
import time

def download_image(url, save_path):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        # Check if the request was successful
        if response.status_code == 200:
            # Open a file in binary write mode and write the content of the response to it
            with open(save_path, 'wb') as f:
                f.write(response.content)
            print(f"Image downloaded successfully and saved at {save_path}")
        else:
            print(f"Failed to download image. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

api_key = "API-KEY-HERE"
authorization = "Bearer %s" % api_key

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": authorization
}

# Load the JSON file
with open('prompts.json', 'r') as file:
    data = json.load(file)

index = 0

for prompt in data:
    # Get a presigned URL for uploading an image
    url = "https://cloud.leonardo.ai/api/rest/v1/init-image"

    payload = {"extension": "jpg"}

    response = requests.post(url, json=payload, headers=headers)

    print(response.status_code)

    # Upload image via presigned URL
    fields = json.loads(response.json()['uploadInitImage']['fields'])

    url = response.json()['uploadInitImage']['url']
    print(url)

    image_id = response.json()['uploadInitImage']['id']  # For getting the image later

    image_file_path = "source-image/cat-standing.jpeg"
    files = {'file': open(image_file_path, 'rb')}

    print(image_id)

    response = requests.post(url, data=fields, files=files) # Header is not needed

    print(response.status_code)

    # Generate with an image prompt
    url = "https://cloud.leonardo.ai/api/rest/v1/generations"

    payload = {
        "height": 512,
        "modelId": "ac614f96-1082-45bf-be9d-757f2d31c174", # Dream Shaper
        "prompt": prompt,
        "width": 512,
        "init_image_id": image_id, # Accepts an array of image IDs
        "seed": 163432960,
        "num_images": 1,
        "init_strength": 0.15,
        "guidance_scale": 7,
        "public": True,
        "promptMagic": False,
        "photoReal": False,
        "alchemy": False,
        "presetStyle": "LEONARDO",
        "negative_prompt": None
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.status_code)

    # Get the generation of images
    generation_id = response.json()['sdGenerationJob']['generationId']

    url = "https://cloud.leonardo.ai/api/rest/v1/generations/%s" % generation_id

    time.sleep(15)

    response = requests.get(url, headers=headers)

    print(response.text)

    image_url = response.json()['generations_by_pk']['generated_images'][0]['url']
    print(image_url)
    save_path = 'image%s.jpg' % index
    download_image(image_url, save_path)

    index += 1

    # time.sleep(1)