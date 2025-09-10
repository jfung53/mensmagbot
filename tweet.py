import tweepy
import requests
# allows us to use the operating system and load environment variables 
import os
from dotenv import load_dotenv
import json
import random
import csv
import drawBot as db
from PIL import Image as PILImage, ImageFilter as PILImageFilter

# pulling the keys and secrets from our .env file
load_dotenv()
# unsplash
APP_ID = os.getenv("APP_ID")
ACCESS_KEY = os.getenv("ACCESS_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
# twitter
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

# handles twitter authentication
client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

# also handles twitter authentication 
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# debugging statement: making sure we have loaded the variables
print('we loaded the auth variables')

def tweet_a_man(tweepy_client):
    # debugging: checking to see that the function is running
    print('creating a man...')

    # ------------------------------------
    # get a random image from unsplash api
    # ------------------------------------

    # define keyword search query
    SEARCH_QUERY = 'man in nature'

    # unsplash API random image URL
    url = 'https://api.unsplash.com/photos/random'

    params = {
        'query': SEARCH_QUERY,
        'client_id': ACCESS_KEY,
        'orientation': 'portrait', # optional. landscape, portrait, squarish
        'dummy': random.randint(0, 999999) # supposed to break cache-like behaviour
    }

    # download a random image and save attribution data
    response = requests.get(url, params=params)
    print(response)

    if response.status_code == 200:
        data = response.json()

        image_url = data['urls']['full']

        # metadata for attribution
        photographer_name = data['user']['name']
        photographer_profile = data['user']['links']['html']
        unsplash_link = data['links']['html']
        photo_id = data['id']
        #filename = f"{photo_id}.jpg"

        filename = 'random_unsplash_image.jpg'
        
        # download image
        image_response = requests.get(image_url)
        if image_response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(image_response.content)
            print(f"Image {photo_id} downloaded and saved as {filename}")

            metadata = {
                "photo_id": photo_id,
                "photographer": photographer_name,
                "photographer_profile": photographer_profile,
                "unsplash_link": unsplash_link,
                "filename": filename
            }

            # save credits to json
            json_path = "credits.json"
            if os.path.exists(json_path):
                with open(json_path, 'r', encoding='utf-8') as f:
                    credits = json.load(f)
            else:
                credits = []
            
            credits.append(metadata)
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(credits, f, indent=2)
            print("Metadata saved")

        else:
            print("Download failed")
    else:
        print("Failed to fetch image from Unsplash")


    # ------------------
    # get generated text
    # ------------------
    csv_path = "drawbot/unique_text_to_post.csv"

    # read into a list
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        #skip header
        next(reader)
        entries = [row[0] for row in reader if row]

    # this is where the generated text is grabbed from
    text_obj = random.choice(entries)
    print(f'Random text chosen: {text_obj}')

    # manually enter strings of different lengths
    #text_obj = 'Masculinity is not simply the physical and emotional dominance of a man it is also the physical and emotional vulnerability and dignity of a woman.'
    #text_obj = 'A manly man'


    # -----------
    # photo setup
    # -----------

    # source image path
    img_source = 'random_unsplash_image.jpg'

    # variables for output image
    # ideal instagram sizes for posts
    # square              1080 x 1080
    # 4:5 (vertical)      1080 x 1350
    # 1.91:1 (landscape)  1080 x 566
    output_png = "output.png"
    output_x, output_y = 1080, 1080

    # calculate height needed to maintain aspect ratio
    imgPIL = PILImage.open(img_source)
    w_percent = output_x / float(imgPIL.width)
    target_height = int(float(imgPIL.height) * w_percent)

    # resize image to be smaller
    img_resized = imgPIL.resize((output_x, target_height), PILImage.LANCZOS)
    print("Image resized")

    # crop to center
    top = (target_height - output_y) // 2
    bottom = top + output_y
    # crop arguments: left, top, right, bottom
    img_cropped = img_resized.crop((0, top, output_x, bottom))
    print("Image cropped")

    # display(img_cropped)

    # save to a temporary file to use with db.imagePixelColor() below
    temp_path = 'temp_img.png'
    img_cropped.save(temp_path)

    # prepare blurred image for later (overlay to help text legibility)
    img_blurred = img_cropped.filter(PILImageFilter.GaussianBlur(radius=10))
    temp_path_blurred = 'temp_img_blurred.png'
    img_blurred.save(temp_path_blurred)
    print("Saved temporary files")


    # --------------------
    # drawing instructions
    # --------------------

    print("Drawing started")
    with db.drawing():    
        # define canvas size
        db.newPage(output_x, output_y)

        # set background colour
        db.fill(0, 0, 0)
        #db.fill(db.random(), db.random(), db.random())
        db.rect(0, 0, db.width(), db.height())

        # ASCII art effect
        print('Generating ASCII pixels')
        pixel_size = 16
        #db.font('CourierNewPS-BoldMT')
        #db.font('CourierNewPSMT')
        db.font('drawbot/fonts/CourierPrime/CourierPrime-Bold.ttf')
        db.fontSize(pixel_size)

        for x in range(0, output_x, 12):
            for y in range(0, output_y, pixel_size):
                color = db.imagePixelColor(temp_path, (x, y))
                if color:
                    r, g, b, a = color
                    db.fill(r, g, b, a)
                    db.text("#", (x, y))

        # add blurred image
        print("Blurring the photo")
        blurred_img_obj = db.ImageObject()
        with blurred_img_obj:
            db.newPage(output_x, output_y)
            db.image(temp_path_blurred, (0, 0))
        db.image(blurred_img_obj, (0, 0), 0.5)

        # add text on top
        print("Adding styled text")

        bx, by, bw, bh = 64, 64, 960, 960
        db.fill(0, 0, 0, 0)
        db.rect(bx, by, bw, bh)

        #db.font('AkzidenzGroteskPro-Bold')
        db.font('drawbot/fonts/Bowlby_One_SC/BowlbyOneSC-Regular.ttf')
        db.fontSize(104)
        db.lineHeight(104)
        db.tracking(-2)

        chrom = 4

        # teal (r, g, b, alpha)
        db.fill(0, 255, 255, 0.8)
        db.textBox(text_obj, (bx+chrom, by+chrom, bw, bh))

        # red (r, g, b, alpha)
        db.fill(255, 0, 0, 0.8)
        db.textBox(text_obj, (bx-chrom, by-chrom, bw, bh))

        # # random colour
        # db.fill(db.random(), db.random(), db.random(), 0.5)
        # db.textBox(text_obj, (bx+chrom, by+chrom, bw, bh))

        # # random colour
        # db.fill(db.random(), db.random(), db.random(), 0.5)
        # db.textBox(text_obj, (bx-chrom, by-chrom, bw, bh))

        # white
        db.fill(255, 255, 255)
        db.textBox(text_obj, (bx, by, bw, bh))

        print(f"Saving to {output_png}")
        db.saveImage(output_png, imageResolution=300)

    # clean up
    os.remove(temp_path)
    os.remove(temp_path_blurred)
    os.remove(filename)
    #os.remove(output_png)

    ##################

    r1 = requests.get("https://collectionapi.metmuseum.org/public/collection/v1/search?q=nature")
    parsed = r1.json()

    # grabbing a random work from the top 6000
    # change this to something smaller if you get index error
    # or use notebook to find total number of objects in parsed
    number = randint(1, 10131)

    # grabbing data about the individual work
    obj_id = parsed['objectIDs'][number]
    r2 = requests.get(f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{obj_id}")
    parsed = r2.json()

    # getting title, artist, gender, url
    if parsed['title'] != '':
       title = f"Title: {parsed['title']}"
    else:
        title = f"Title: Unknown"
    if parsed['artistDisplayName'] != '':
       artist = f"Artist: {parsed['artistDisplayName']}"
    else:
       artist = 'Artist: Unknown'
    if parsed['artistGender'] != '':
        gender = parsed['artistGender']
    else:
        gender = 'Artist Gender: Not marked'
    url = parsed['objectURL']

    ##################

    # getting image (have to use the other auth)
    image_url = parsed['primaryImage']
    img = requests.get(image_url)
    img_content = img.content
    with open('image.jpg', 'wb') as handler:
        handler.write(img_content)
    media = api.media_upload(filename='image.jpg')
    media_id = media.media_id

    # setting up the tweet text
    tweet_text = f"{title}, {artist}, {gender}. See more: {url}"
    print('tweeting nature from the MET...')
    tweepy_client.create_tweet(text=tweet_text, media_ids=[media_id])
 
# calling the function with the auth data as parameter
tweet_a_man(client)