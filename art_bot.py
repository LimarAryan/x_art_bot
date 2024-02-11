import psycopg2 #database adapter for python + postgresql
import tweepy #Twitter API

import json
import requests

import random
import time
import datetime

# PostgreSQL database configuration
DB_NAME = "your_db_name"
DB_USER = "your_db_user"
DB_PASSWORD = "your_db_password"
DB_HOST = "your_db_host"
DB_PORT = "your_db_port"

# Twitter API keys
CONSUMER_KEY = "your_consumer_key"
CONSUMER_SECRET = "your_consumer_secret"
ACCESS_TOKEN = "your_access_token"
ACCESS_TOKEN_SECRET = "your_access_token_secret"



# TODO: Create a DatabaseManager class
def connect_to_database():
    """Connects to the PostgreSQL database."""
    try:
        connection = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        print("Connected to the database.")
        return connection
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None
    
def import_csv_published_images(connection):
    """Imports CSV of published_images from National Art Gallery data into postgreSQL tables."""
    try:
        # Opens CSV file, saves into a variable, creates a cursor(executor) to copy from the csv into the table in the sql file
        with open(r'x_art_bot\opendata\data\published_images.csv', 'r') as csv_file:
            cursor = connection.cursor()
            cursor.copy_from(csv_file, 'published_images', sep=',')
            connection.commit()  # Commit the transaction to make the changes persistent
            cursor.close()  # Close the cursor
            print("Successfully imported data")
    except Exception as e:
        print(f"An error occurred: {e}")
        #rollback the transaction if an error occurs
        connection.rollback()
    finally:
        # If cursor is defined, close it. Safety measure in case the error occurred before cursor.close() was reached.
        if 'cursor' in locals():
            cursor.close()

def import_csv_objects(connection):
    """Imports objects.csv into the 'objects' table in a PostgreSQL database."""
    try:
        # Open the CSV file and create a cursor to execute the copy command
        with open('/mnt/data/objects.csv', 'r') as csv_file:
            cursor = connection.cursor()
            # Assuming the table and CSV column headers match exactly and are in the same order
            cursor.copy_from(csv_file, 'objects', sep=',')
            connection.commit()  # Commit the changes to the database
            print("Successfully imported data into the objects table.")
    except Exception as e:
        print(f"An error occurred while importing data: {e}")
        connection.rollback()  # Roll back the transaction on error
    finally:
        # Ensure the cursor is closed properly
        if 'cursor' in locals():
            cursor.close()

# Example usage
# You would need a connection object here. Below is a placeholder for where you would create or obtain your database connection.
# connection = <your_database_connection_method_here>()
# import_csv_to_objects_table(connection)




class ArtworkManager: #Manages getting artwork from the database,
    def __init__(self, uuid_file = "used_uuids.json"):
        self.uuid_file = uuid_file
        self.used_uuids = self.load_used_uuids()

    def get_random_artwork(self, connection):
            """Retrieve a random artwork UUID along with its title, displaydate, and artist info from the artwork_details view."""
            try:
                cursor = connection.cursor()
                query = """
                SELECT uuid, title, displaydate, artist
                FROM artwork_details
                WHERE uuid NOT IN %s
                ORDER BY RANDOM() LIMIT 1;
                """
                cursor.execute(query, (tuple(self.used_uuids),))
                row = cursor.fetchone()
                cursor.close()
                if row:
                    artwork_info = {
                        'uuid': row[0],
                        'title': row[1],
                        'displaydate': row[2],  # Directly using displaydate
                        'artist': row[3]
                    }
                    return artwork_info  # Return a dictionary with the artwork details
                else:
                    print("No new artwork found.")
                    return None
            except Exception as e:
                print(f"Error retrieving artwork from the database: {e}")
                return None


    def add_used_artwork(self, uuid):
        """Add the posted artwork UUID to the JSON file"""
        self.used_uuids.add(uuid)
        self.save_used_uuids()

    def load_used_uuids(self):
        """Load posted artwork UUIDs from a JSON file."""
        try:
            with open(self.uuid_file, 'r') as file:
                used_uuids = set(json.load(file))
            return used_uuids
        except (FileNotFoundError, json.JSONDecodeError):
            return set() #Returns an empty set if the file does not exist

    def save_used_uuids(self):
        """Save the posted artwork UUIDs to a JSON file"""
        with open(self.uuid_file, 'w') as file:
            json.dump(list(self.used_uuids),)
    


#TODO: Create a Tweet manager class
def download_image(iiifurl, filename):
    """Grabs iiifurl from random artwork, adds ending string and downloads image
        as 'art' variable"""
    url = iiifurl + "/full/pct:100/0/default.jpg"
    response = requests.get(url)  # Corrected from 'request.get' to 'requests.get'
    if response.status_code == 200:
        filepath = f'/x_art_bot/images/{filename}'  # Specify the directory to save images
        with open(filepath, 'wb') as art:
            art.write(response.content)
            print("Image downloaded successfully.")
        return filepath  # Return the path to the downloaded image
    else:
        print("Failed to download image. Status code:", response.status_code)
        return None



def post_tweet(api, artwork, image_path):
    """Post a tweet with the artwork title, artist, year, and image."""
    try:
        # Construct the tweet text
        title = artwork.get('title', 'Unknown Title')
        artist = artwork.get('artist', 'Unknown Artist')
        year = artwork.get('displaydate', 'Unknown Year')
        tweet_text = f'"{title}" by {artist}, ({year})'
        
        # Upload the image and get the media ID
        media = api.media_upload(image_path)
        media_ids = [media.media_id_string]
        
        # Post the tweet with the image
        api.update_status(status=tweet_text, media_ids=media_ids)
        print("Tweet posted successfully.")
    except Exception as e:
        print(f"Error posting tweet: {e}")


def task():
    True
    #TODO: create controller task organize functions

def main():
    True

if __name__ == "__main__":
    main()