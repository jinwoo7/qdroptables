import boto3, logging, requests, os, sys, vlc, time
from os.path import isfile
from os import remove
from mutagen.mp3 import MP3

# Error Checking
env_vars = ['APIKEY', 'ACCESSKEY', 'SECRETKEY']
def env_check(env_list):
	for env in env_list:
		if env not in os.environ:
			sys.exit('Please set env variable:{}'.format(env))

# Variable Declaration

file_path = sys.argv[-1]
#file_path = "C:\\Users\\jyom\\Documents\\github\\12153.jpg"

face_api_url = "https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect"

image_url = 'https://how-old.net/Images/faces2/main007.jpg'

headers = {
    'Content-Type': "application/json",
    'Ocp-Apim-Subscription-Key': os.environ['APIKEY']
}

params = {
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'emotion'
}

session = boto3.Session(aws_access_key_id=os.environ['ACCESSKEY'],
						aws_secret_access_key=os.environ['SECRETKEY'])

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
	filename = path.split('/')[-1]

	# check path & open file
	try:
		data = open(path, 'rb')
	except Exception as e:
		data.close()
		sys.exit('Encountered error opening file: {}. Error: {}'.format(path, e))

	# upload image to s3
	try:
		response = s3.put_object(Bucket=bucket_name, Key=filename, Body=data)
		if response['ResponseMetadata']['HTTPStatusCode'] != 200:
			data.close()
			sys.exit('Encountered error uploading {} to bucket {}. Error: {}'.format(filename, bucket_name, response))		
		else:
			data.close()
			print('Successfully uploaded file {} to bucket {}.'.format(filename, bucket_name))
	except Exception as e:
		data.close()
		sys.exit('Encountered error uploading {} to bucket {}. Error: {}'.format(filename, bucket_name, e))

	return "https://s3.amazonaws.com/rating-imgs/" + filename


def remove_file(path):
	remove(path)

def analyze_file(image_url):
	data = {'url': image_url}
	response = requests.post(face_api_url, params=params, headers=headers, json=data)
	return response.json()

def sort_results(faces):
        emotions = []
        print(faces)
        emotion_result = faces['faceAttributes']['emotion']
        for face in faces:
                person = []
		# Good
                person.append([
			"Happy     ",
			emotion_result['happiness'] + emotion_result['neutral'] + emotion_result['contempt']
		])
		# Sad
                person.append([
			"Sad       ",
			emotion_result['sadness']
		])
		# Frustrated
                person.append([
			"Frustrated",
			emotion_result['anger'] + emotion_result['disgust']
		])
		# Scared
                person.append([
			"Scared    ",
			emotion_result['fear'] + emotion_result['surprise']
		])
                emotions.append(sorted(person, key=lambda tup: tup[1], reverse=True))

	# person = []
	# person.append([
	# 	"Sad       ",
	# 	1.0
	# ])
	# person = []
	# emotions.append(person)
	# person.append([
	# 	"Frustrated",
	# 	1.0
	# ])
	# emotions.append(person)
	# person = []
	# person.append([
	# 	"Scared    ",
	# 	1.0
	# ])
	# emotions.append(person)

        return emotions

def print_result(emotions):
	for emotion in emotions:
		print("-----------------------------------------------------------------")
		for e in emotion:
			bar = "|" * int(e[1] * 100 / 2)
			print("{} : {} {}%".format(e[0], bar, e[1] * 100))

def play_sound(emotions):
	topResults = []
	for emotion in emotions:
		topResults.append(emotion[0][0])

	if "Scared    " in topResults:
		sound = 'slowDown.mp3'
	elif "Frustrated" in topResults:
		sound = 'frustration.mp3'
	elif "Sad       " in topResults:
		sound = 'checkOnPassenger.mp3'
	else:
		sound = 'good.mp3'


	p = vlc.MediaPlayer(sound)
	try:
            p.play()
            time.sleep(MP3(sound).info.length + 2)
	except:
            print("stopping sound")
            p.stop()

print('Check env')
env_check(env_vars)

print('Check file for validity')
check_file(file_path)

print('Upload to S3')
fileUrl = upload_images(file_path)

print('Delete Local File')
remove_file(file_path)

print('Run Analysis')
faces = analyze_file(fileUrl)

print('Sort Result')
emotions = sort_results(faces)

print('Display Result')
print_result(emotions)

print('Play Sound')
play_sound(emotions)
