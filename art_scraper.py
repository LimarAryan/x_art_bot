#ONLY NEEDS TO BE RUN ONCE FULLY!
#Scrapes image URL from JSON info in work folder (provided by Carnegie Mellon)
#Uses this URL to download and place in art_images folder

import json
import glob
import codecs
import io
import requests
import urllib
import re
import os
import lxml.html

art_images = r"art_images"

def return_list_of_JSON_paths(dirPath):
    """JSON Paths provided by Carnegie Mellon"""
    json_pattern = os.path.join(dirPath, '*.json')
    file_list = glob.glob(json_pattern)
    return file_list

list_JSON_paths = return_list_of_JSON_paths(r"work")

def read_html(url):
    source_code = requests.get(url) 
    html_elements = lxml.html.fromstring(source_code.content) 
    return html_elements

count = 0
for file in list_JSON_paths:
    count+=1
    print(count)
    openJSON = json.load(open(file, encoding='utf-8'))

    title = openJSON["title"]
    if title != None:
        title_cleaned = " ".join(re.sub(r'[^a-zA-Z]', ' ', title).split())
    else:
        title_cleaned = "Unknown"

    date = openJSON["displaydate"]
    if date != None:
        date_cleaned = " ".join(re.sub(r'[^a-zA-Z0-9]', ' ', date).split())
        #print(date_cleaned)
    else:
        date_cleaned = ""

    artist = openJSON["attribution"]
    if artist != None:
        artist_cleaned = " ".join(re.sub(r'[^a-zA-Z0-9]', ' ', artist).split())
        #print(artist_cleaned)
    else:
        artist_cleaned = "Unknown"

    URL_to_Image = openJSON["iiif"]

    read_art_html = read_html(URL_to_Image) 
    path_to_image = "//img[@style]/@src"

    urllib.request.urlretrieve(URL_to_Image, 'art_images' + "\\" + artist_cleaned + "_" + date_cleaned + "_" + artist_cleaned + ".jpg")
print("Finished")