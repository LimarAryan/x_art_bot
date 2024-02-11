import os
import random
import json
import tweepy
import time

# Twitter API keys - replace with your own values
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

# Folder of images and JSON files
art_images_folder = 'art_images'
used_images_file = 'used_images.json'  # Ensure the file extension is consistent (.json)
processed_entries_file = os.path.join('art_images', '.processed_entries.json')  # Use os.path.join for compatibilit

class ArtworkManager:
    def __init__(self, art_images_folder, used_images_file, processed_entries_file):
        self.art_images_folder = art_images_folder
        self.used_images_file = used_images_file
        self.processed_entries_file = processed_entries_file
        self.used_images = self.load_used_images()

    def load_used_images(self):
        try:
            with open(self.used_images_file, 'r') as file:
                used_images = json.load(file)
                # Filter out unwanted files
                return {image for image in used_images if not image.startswith(".") and image != ".processed_entries.JSON"}
        except (FileNotFoundError, json.JSONDecodeError):
            return set()

    def load_processed_entries(self):
        try:
            with open(self.processed_entries_file, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_used_images(self):
        with open(self.used_images_file, 'w') as file:
            json.dump(list(self.used_images), file, indent=4)

    def get_unused_artwork(self):
        all_images = set(os.listdir(self.art_images_folder))
        unused_images = [image for image in all_images if not image.startswith(".") and image != ".processed_entries.JSON" and image not in self.used_images]
        if unused_images:
            selected_image = random.choice(unused_images)
            self.used_images.add(selected_image)
            self.save_used_images()
            return selected_image
        else:
            print("No unused artwork available.")
            return None

def get_metadata(filename):
    # Ensure this path matches where your metadata file actually is
    processed_entries_path = os.path.join(art_images_folder, '.processed_entries.json')
    try:
        with open(processed_entries_path, 'r') as file:
            processed_entries = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading metadata file: {e}")
        return None

    metadata = processed_entries.get(filename)
    if metadata is None:
        print(f"Metadata not found for filename: {filename}")
        return None

    title = metadata.get('title')
    displaydate = metadata.get('displaydate')
    attribution = metadata.get('attribution')

    if not all((title, displaydate, attribution)):
        print(f"Incomplete metadata for filename: {filename}")
        return None

    return title, displaydate, attribution




def post_tweet_with_artwork(api_v1, api_v2, artwork_manager):
    selected_image_filename = artwork_manager.get_unused_artwork()
    if selected_image_filename:
        image_path = os.path.join(artwork_manager.art_images_folder, selected_image_filename)

        # Load the processed entries JSON
        try:
            with open(artwork_manager.processed_entries_file, 'r') as file:
                processed_entries = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading processed entries file: {e}")
            return

        # Retrieve metadata associated with the image filename
        metadata = processed_entries.get("filenames", {}).get(selected_image_filename, None)
        if metadata:
            title = metadata.get('title')
            displaydate = metadata.get('displaydate')
            attribution = metadata.get('attribution')
            
            if not all((title, displaydate, attribution)):
                print(f"Incomplete metadata for filename: {selected_image_filename}")
                return

            tweet_text = f'"{title}" by {attribution}'
            if displaydate:
                tweet_text += f", {displaydate}"
            
            # Post the tweet with the image using v1 and v2
            try:
                # Using v1 for media upload
                media_v1 = api_v1.media_upload(filename=image_path)
                media_id_v1 = media_v1.media_id_string  # Ensure correct attribute is used

                # Using v2 for posting tweet
                api_v2.create_tweet(text=tweet_text, media_ids=[media_id_v1])
                print("Tweet posted successfully.")
            except Exception as e:
                print(f"Error posting tweet: {e}")
        else:
            print(f"Metadata not found for filename: {selected_image_filename}")


def main():
    client_v1 = get_twitter_conn_v1(api_key, api_secret, access_token, access_token_secret)
    client_v2 = get_twitter_conn_v2(api_key, api_secret, access_token, access_token_secret)
    
    artwork_manager = ArtworkManager(art_images_folder, used_images_file, processed_entries_file)
    
    while True:
        post_tweet_with_artwork(client_v1, client_v2, artwork_manager)
        print("Sleeping for 20 minutes...")
        time.sleep(20 * 60)  # Sleep for 20 minutes

if __name__ == "__main__":
    main()