import os
from dotenv import load_dotenv

from instabot import Bot


# pulling login credentials from .env file
load_dotenv()
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")


# from https://medium.com/@rajdattkokate/automate-instagram-posts-with-python-a-step-by-step-guide-4b055f356b31
# and https://github.com/Jacob-Mellichamp/Instagram-bot/blob/main/src/instaPublisher.py

def upload_image(username, password, image_path, caption):
    bot = Bot()
    bot.login(username=USERNAME, password=PASSWORD)
    
    # Upload the image with the caption
    bot.upload_photo(image_path, caption=caption)
    
    # Logout after uploading
    bot.logout()

image_path = ""

caption = ""

upload_image(username, password, image_path, caption)

'''
# alternatively, input arguments directly

# input your instagram credentials
username = input("Enter your Instagram username: ")
password = input("Enter your Instagram password: ")

# input the path to the image you want to upload
image_path = input("Enter the path to your image file: ")

# input the caption for your post
caption = input("Enter your caption: ")
'''