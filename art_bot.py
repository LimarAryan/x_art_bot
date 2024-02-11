import psycopg2 #database adapter for python + postgresql
import tweepy #Twitter API

import json
import requests
import os
from PIL import Image

import random
import time
import datetime

# Twitter API keys
CONSUMER_KEY = "your_consumer_key"
CONSUMER_SECRET = "your_consumer_secret"
ACCESS_TOKEN = "your_access_token"
ACCESS_TOKEN_SECRET = "your_access_token_secret"

#Initialize Tweepy API
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

#Folder of images and JSON files
art_images_folder = 'art_images'
used_images_file = 'used_images.JSON'


class ArtworkManager:
    def __init__(self, art_images_folder, used_images_file):
        self.art_images_folder = art_images_folder
        self.used_images_file = used_images_file
        self.used_images = self.load_used_images()

    def load_used_images(self):
        try:
            with open(self.used_images_file, 'r') as file:
                return set(json.load(file))
        except (FileNotFoundError, json.JSONDecodeError):
            return set()

    def save_used_images(self):
        with open(self.used_images_file, 'w') as file:
            json.dump(list(self.used_images), file, indent=4)

    def get_unused_artwork(self):
        all_images = set(os.listdir(self.art_images_folder))
        unused_images = list(all_images - self.used_images)
        if unused_images:
            selected_image = random.choice(unused_images)
            self.used_images.add(selected_image)
            self.save_used_images()
            return selected_image
        else:
            print("No unused artwork available.")
            return None
    



def post_tweet_with_artwork(api, artwork_manager):
    selected_image_filename = artwork_manager.get_unused_artwork()
    if selected_image_filename:
        image_path = os.path.join(art_images_folder, selected_image_filename)
        
        # Extracting details from the file name
        # Assuming the format is 'Title_Artist_Year.jpg'
        details = selected_image_filename.rsplit('.', 1)[0].split('_')
        title, artist, year = '_'.join(details[:-2]), details[-2], details[-1]
        
        # Construct the tweet text
        tweet_text = f'"{title}" by {artist}, ({year})'
        
        # Post the tweet with the image
        try:
            media = api.media_upload(image_path)
            api.update_status(status=tweet_text, media_ids=[media.media_id_string])
            print("Tweet posted successfully.")
        except Exception as e:
            print(f"Error posting tweet: {e}")


def task():
    True
    #TODO: create controller task to organize functions and schedule tweet every 30 minutes

def main():
    artwork_manager = ArtworkManager(art_images_folder, used_images_file)
    post_tweet_with_artwork(api, artwork_manager)

if __name__ == "__main__":
    main()