# Twitter Art Bot v1🖼️

Project is live on Twitter: 
</br>**[@x_art_bot🎨](https://twitter.com/x_art_bot)**

<img src = 'https://github.com/LimarAryan/x_art_bot/assets/110574851/7b08c739-30fc-430e-a9ac-4735ddb2e647' width = '250'>

# How to install and run in a local environment
1. Clone this repo to a local directory
```bash
git clone https://github.com/LimarAryan/x_art_bot.git
```
2. Switch to the cloned repository folder
```bash
cd path_to_directory/x_art_bot
```
3. Install tweepy, a python twitter package
```bash
pip install tweepy
```
4. Run **art_scraper.py** from inside the directory</br>
images downloaded will go into the `x_art_bot/art_images` folder.
```bash
python art_scraper.py
```
**WARNING**: if you leave this script running continuously it will download 100,000 image files. Close the terminal or Click `CTRL + C`
</br>to exit out of the **art_scraper.py** script when you are satisfied with the amount of images downloaded.</br></br>

6. Use a 3-legged OAuth API flow to get your `access_token` and `access_token_secret`
</br>Twitter's documentation for 3-legged OAuth flow can be found [HERE](https://developer.twitter.com/en/docs/authentication/oauth-1-0a/obtaining-user-access-tokens)
</br></br>Here is an example of python code needed for the 3-legged OAuth flow
</br>to get your `access_token` and `access_token_secret`, you can copy and paste the code below
</br>into **art_bot.py**, run the python program once and a print message on the terminal screen should pop up with your
</br> `access_token` and `access_token_secret` after these are obtained you can delete this code from the program entirely
```python
import requests
from urllib.parse import quote

# Your credentials
#The API Key and API Secret can be found in your twitter developer portal under 'Keys and Tokens'
#The CALLBACK_URL can be found in the User authentication settings in the twitter developer portal
api_key = 'YourAPIKey'
api_secret = 'YourAPISecret'
CALLBACK_URL = 'https://api.twitter.com/oauth/authorize?oauth_token={YOUR_OAUTH_TOKEN}' #example link


# Step 1: Encode callback URL and get request token
callback_encoded = quote(CALLBACK_URL, safe='')
response = requests.post(f"https://api.twitter.com/oauth/request_token?oauth_callback={callback_encoded}", auth=(api_key, api_secret))

if response.status_code == 200:
    # Extract token and secret from response
    oauth_token, oauth_token_secret = response.text.split('&')[0], response.text.split('&')[1]
    print("Request Token and Secret obtained.")

    # Step 2: Redirect user to Twitter for authorization
    # Direct the user to this URL
    print(f"https://api.twitter.com/oauth/authorize?oauth_token={oauth_token}")

    # Step 3 would occur after the user has authorized the app and you've received the oauth_verifier
    # This part would typically be handled by your web server handling the callback
else:
    print("Failed to obtain request token.")
```

6. On line 8-11 in art_bot.py fill in your API keys:
```python
api_key = "x"
api_secret = "x"
access_token = "x"
access_token_secret = "x"
```
7. Run art_bot.py to post a random artwork image from `x_art_bot/art_images`
```bash
python art_bot.py
```

# Work Folder
The 'work' folder containing JSON data</br>
which is provided by the amazing students at</br> 
Carnegie Mellon University</br>
with 100,000 already scraped / crawled image</br>
sites and metadata. You can download it</br>
from my repo, or from this link as a zipped</br>
file called "nearest_neighbors.tar.gz":</br>
[Download Link](https://kilthub.cmu.edu/articles/dataset/National_Gallery_of_Art_InceptionV3_Features/10061885)

# Version info
This version runs in a local environment,</br>
however I am running the actual</br>
x_art_bot account on an aws lambda function,</br>
using an s3 bucket, and dynamodb. A brief explanation</br>
will be given in the next section.</br>

# AWS
I am using all AWS free tier products to run this concurrently.</br>
I use AWS lambda function for the python script, DynamoDB to store </br>
used filenames, and an S3 Bucket for the img files.</br>

## Lambda
I have included the code that I'm using in lambda_function.py</br>
Basically, what is happening is that I check the local tmp folder of </br>
the lambda instance and if there any items I delete them through a shell subprocess </br>
(because this is where the bot places the tmp img file from the s3 bucket the moment before it posts). </br>
I establish a connection to my twitter API through the keys and define my twitter posting functions</br>
I grab an artwork filename, and check if the filename for the artwork is already used (on dynamodb) </br>
If it is not used, then it will post it to twitter. </br>
A cloudwatch event is used to create a cron job so the script only runs every hour </br>
(bot only posts every hour)</br>

## DynamoDB
I use AWS' DynamoDB to place a simple string of the filename that is already used, </br>
so the lambda function when checking if a file is already used goes to DynamoDB, </br>
and compares the current filename to all the filenames already used. </br>

## S3 Bucket
This is where the real magic happens, in the s3 bucket I place image files </br>
that I scraped with art_scraper.py. Currently there are 10,000 images in </br>
my s3 bucket but I can always manually add more by uploading them to the bucket through aws cli.</br>
