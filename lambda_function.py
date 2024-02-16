#Lambda code for AWS deployment
import tweepy
import os
import json
import boto3
import tempfile
import subprocess
import random

def list_tmp_contents():
    tmp_dir = '/tmp'
    contents = os.listdir(tmp_dir)
    print("Contents of /tmp:")
    for item in contents:
        print(item)

session = boto3.Session('s3')
s3_resource = boto3.resource('s3', region_name='us-east-1')
s3 = boto3.client('s3')
dynamodb = boto3.client('dynamodb', region_name='us-east-1')

#Fill in with your keys and tokens
api_key = "x"
api_secret = "x"
access_token = "x"
access_token_secret = "x"

def get_twitter_conn_v1(api_key, api_secret, access_token, access_token_secret) -> tweepy.API:
    """Get twitter conn 1.1"""

    auth = tweepy.OAuth1UserHandler(api_key, api_secret)
    auth.set_access_token(
        access_token,
        access_token_secret,
    )
    return tweepy.API(auth)

def get_twitter_conn_v2(api_key, api_secret, access_token, access_token_secret) -> tweepy.Client:
    """Get twitter conn 2.0"""

    client = tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
    )
    return client
    

    
def post_tweet_with_artwork(api_v1, api_v2, download_path, title, date, artist):
    if download_path:
        if not all((title, date, artist)):
            print(f"Incomplete metadata for filename: {filename}")
            return
        tweet_text = f'"{title}" by {artist}'
        if date:
            tweet_text += f", {date}"
        try:
            # Using v1 for media upload
            media_v1 = api_v1.media_upload(filename=download_path)
            media_id_v1 = media_v1.media_id_string  # Ensure correct attribute is used

            # Using v2 for posting tweet
            api_v2.create_tweet(text=tweet_text, media_ids=[media_id_v1])
            print("Tweet posted successfully.")
        except Exception as e:
            print(f"Error posting tweet: {e}")
            raise e
    else:
        print(f"Metadata not found for filename: {download_path}")
    

def is_filename_used(filename):
    try:
        response = dynamodb.get_item(
            TableName='used_images',
            Key={
                'filename': {
                    'S': filename
                }
            }
        )
        return 'Item' in response
    except Exception as e:
        print(f"Error checking filename in DynamoDB: {e}")
        raise e

def lambda_handler(event, context):
    bucket_name = 'artimages3'
    key = '.processed_entries.json'
    local_image_path = '/tmp'

    # Load json metadata from S3 bucket into JSON
    try:
        data = s3.get_object(Bucket=bucket_name, Key=key)
        json_data = json.loads(data['Body'].read().decode('utf-8'))
    except Exception as e:
        print(e)
        raise e
    print("Got keys")
    #chooses random filename from json
    random_filename = random.choice(list(json_data['filenames'].keys()))
    print("Random filename:", random_filename)

    #Loop to check if image has been used
    while True:
        random_filename = random.choice(list(json_data['filenames'].keys()))

        if random_filename in json_data['filenames']:
            artwork_info = json_data['filenames'][random_filename]
            title = artwork_info.get('title')
            date = artwork_info.get('displaydate')
            artist = artwork_info.get('attribution')

            print(title)

            # Check if filename has already been used
            if not is_filename_used(random_filename):
                break  # Exit the loop if filename is not used
            else:
                print(f"Filename {random_filename} is already used. Trying another one.")
    

    
    #Stores used/posted image in dynamodb
    try:
        response = dynamodb.put_item(
            TableName='used_images',
            Item={
                'filename': {
                    'S': random_filename  # 'S' denotes a String type in DynamoDB
                }
            }
        )
        print(f"Successfully stored filename: {random_filename}")
    except Exception as e:
        print(f"Error storing filename in DynamoDB: {e}")
        raise e
    
    #creates twitter client object
    client_v1 = get_twitter_conn_v1(api_key, api_secret, access_token, access_token_secret)
    client_v2 = get_twitter_conn_v2(api_key, api_secret, access_token, access_token_secret)

    try:
        tmp_dir = tempfile.gettempdir()
        # subprocess.call('rm -rf /tmp/*', shell=True)
        path = os.path.join(tmp_dir, random_filename)
        print(path)
    except Exception as e:
        print(f"Error getting file path")
        raise e
    
    download_path = '/tmp/' + random_filename
    
    try:
        s3_resource.Bucket(bucket_name).download_file(random_filename, download_path)
        print("file moved to /tmp")
        print(os.listdir(tmp_dir))
        
        list_tmp_contents()
        
        print("Path", download_path)
        post_tweet_with_artwork(client_v1, client_v2, download_path, title, date, artist)
        print("Success posting tweet!")
    except Exception as e:
        print(f"Error posting")
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
