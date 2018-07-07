import boto3
import pprint
import logging
from admin import AWS_SERVER_PUBLIC_KEY, AWS_SERVER_SECRET_KEY

'''
1. listen to rabbitmq
2. check path
3. upload to S3
4. analysis
5. display result
'''
session = boto3.Session(aws_access_key_id=AWS_SERVER_PUBLIC_KEY,
						aws_secret_access_key=AWS_SERVER_SECRET_KEY)
s3 = session.client('s3')

def upload_images(path):	
	bucket_name = 'rating-imgs'

	# check path & open file
	try:
		data = open(path, 'rb')
	except Exception as e:
		logging.error('Encountered error opening file: {}. Error: {}'.format(path, e))

	# upload image to s3
	try:
		response = s3.put_object(Bucket=bucket_name, Key=path, Body=data)
		if response['ResponseMetadata']['HTTPStatusCode'] != 200:
			logging.error('Encountered error uploading {} to bucket {}. Error: {}'.format(path, bucket_name, response))		
		else:
			logging.info('Successfully uploaded file {} to bucket {}.'.format(path, bucket_name))
	except Exception as e:
		logging.error('Encountered error uploading {} to bucket {}. Error: {}'.format(path, bucket_name, e))		

upload_images('hello.txt')
#listen()