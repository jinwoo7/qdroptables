import boto3, pprint, logging, requests, os, sys
from os.path import isfile
from os import remove

# Error Checking
env_vars = ['QDROPTABLES-KEY', 'AWS_SERVER_PUBLIC_KEY', 'AWS_SERVER_SECRET_KEY']
def env_check(env_list):
	for env in env_list:
		if env not in os.environ:
			sys.exit('Please set env variable:{}'.format(env))

# Variable Declaration
file_path = sys.argv[-1]

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

session = boto3.Session(aws_access_key_id=os.environ['AWS_SERVER_PUBLIC_KEY'],
						aws_secret_access_key=os.environ['AWS_SERVER_SECRET_KEY'])

s3 = session.client('s3')

# Function Definition
def check_file(path):
	# check that file exists & is jpg extension
	if not isfile(path):
		sys.exit('File {} does not exist'.format(path))
	elif not path.endswith('.jpg'):
		remove(path)
		sys.exit('File {} is not a .jpg file.'.format(path))

def upload_images(path):	
	bucket_name = 'rating-imgs'

	# check path & open file
	try:
		data = open(path, 'rb')
	except Exception as e:
		data.close()
		sys.exit('Encountered error opening file: {}. Error: {}'.format(path, e))

	# upload image to s3
	try:
		response = s3.put_object(Bucket=bucket_name, Key=path, Body=data)
		if response['ResponseMetadata']['HTTPStatusCode'] != 200:
			data.close()
			sys.exit('Encountered error uploading {} to bucket {}. Error: {}'.format(path, bucket_name, response))		
		else:
			data.close()
			print('Successfully uploaded file {} to bucket {}.'.format(path, bucket_name))
	except Exception as e:
		data.close()
		sys.exit('Encountered error uploading {} to bucket {}. Error: {}'.format(path, bucket_name, e))		

def remove_file(path):
	remove(path)

def analyze_file(path):
	response = requests.post(face_api_url, params=params, headers=headers, json=data)
	return response.json()

def print_result(faces):
	if len(faces) >= 1:
		print(faces[0]['faceAttributes']['emotion'])


print('Check env')
env_check(env_vars)

print('Check file for validity')
check_file(file_path)

print('Upload to S3')
upload_images(file_path)

print('Delete Local File')
remove_file(file_path)

print('Run Analysis')
faces = analyze_file(file_path)

print('Display Result')
print_result(faces)