# Twitter Art Bot v1🖼️ @x_art_bot🎨

Project is live: **[Click here](https://twitter.com/x_art_bot)**
to check it out

<img src = 'https://github.com/LimarAryan/x_art_bot/assets/110574851/7b08c739-30fc-430e-a9ac-4735ddb2e647' width = '250'>

# How to install and run in a local environment
1. Clone this repo to a local directory
   ```bash
   git clone https://github.com/LimarAryan/x_art_bot.git
   ```
2. Switch to repository folder
```bash
cd x_art_bot
```
3. Run art_scraper.py until you are satisfied with amount of downloaded images
**Warning: if you leave it running you will continuously download files**
```bash
python art_bot.py
```

# Work Folder
The 'work' folder containing JSON data</br>
is provided by Carnegie Mellon University</br>
with 100,000 already scraped / crawled image</br>
sites and metadata. You can download it</br>
from my repo, or from this link as a zipped</br>
file called "nearest_neighbors.tar.gz":</br>
[Download Link](https://kilthub.cmu.edu/articles/dataset/National_Gallery_of_Art_InceptionV3_Features/10061885)

# Version info
This version runs in a local environment,</br>
however I am running the real</br>
version on an aws lambda function,</br>
using an s3 bucket, and dynamodb.

I will do an in-depth write up soon 😏🤩
