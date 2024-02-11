import json
import glob
import requests
import re
import os

# Sanitize a string to create a valid filename
def sanitize_filename(filename):
    invalid_chars = "<>:\"/\\|?*"
    for char in invalid_chars:
        filename = filename.replace(char, "_")
    return filename

art_images = "art_images"
processed_log = os.path.join("art_images", ".processed_entries.json")

# Ensure the art_images directory exists
if not os.path.exists(art_images):
    os.makedirs(art_images)

# Initialize or load processed entries from the log
if not os.path.exists(processed_log):
    with open(processed_log, 'w') as log_file:
        json.dump({"filenames": [], "count": 0}, log_file)

with open(processed_log, 'r') as log_file:
    log_data = json.load(log_file)

processed_entries = set(log_data["filenames"])
file_count = log_data["count"] - 1

list_JSON_paths = glob.glob(os.path.join("work", '*.json'))

for file_path in list_JSON_paths:
    with open(file_path, encoding='utf-8') as f:
        openJSON = json.load(f)

    title = openJSON.get("title", "Unknown")
    date = openJSON.get("displaydate", "")
    artist = openJSON.get("attribution", "Unknown")

    # Generate the filename and sanitize it
    filename = sanitize_filename(f"{title}_{date}_{artist}.jpg").replace(' ', '_')
    filepath = os.path.join(art_images, filename)

    if filename not in processed_entries:
        print(f"Processing file #{file_count + 1}: {filename}")


        if not os.path.exists(filepath):
            URL_to_Image = openJSON.get("iiif", "")
            if URL_to_Image:
                response = requests.get(URL_to_Image)
                if response.status_code == 200:
                    with open(filepath, 'wb') as img:
                        img.write(response.content)
                    print(f"Downloaded {filename}")
                    processed_entries.add(filename)
                    file_count += 1
                    print(file_count)
                    log_data["filenames"] = list(processed_entries)
                    log_data["count"] = file_count
                    with open(processed_log, 'w') as log_file:
                        json.dump(log_data, log_file, indent=4)
                else:
                    print(f"Failed to download {filename}")
        else:
            print(f"{filename} already exists. Skipping download.")
    else:
        print(f"Skipping already processed entry: {filename}")

# Update the log file


print("Finished processing. Total files processed: {count}")
