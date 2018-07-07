import requests, os, sys

if "QDROPTABLES-KEY" not in os.environ:
    sys.exit('Please set env variable: QDROPTABLES-KEY')

face_api_url = "https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect"

image_url = 'https://how-old.net/Images/faces2/main007.jpg'

headers = {
    'Content-Type': "application/json",
    'Ocp-Apim-Subscription-Key': os.environ['QDROPTABLES-KEY']
}

params = {
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'emotion'
}

data = {'url': image_url}

response = requests.post(face_api_url, params=params, headers=headers, json=data)
faces = response.json()

if len(faces) >= 1:
    print(faces[0]['faceAttributes']['emotion'])
    
# for face in faces:
#     print(face['faceAttributes']['emotion'])