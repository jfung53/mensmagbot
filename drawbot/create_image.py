import requests
import os
from dotenv import load_dotenv
import json
import random
import csv
import drawBot as db
from IPython.display import Image, display, IFrame
from PIL import Image as PILImage, ImageFilter as PILImageFilter

load_dotenv()
ACCESS_KEY = os.getenv("ACCESS_KEY")



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
    filename = f"{photo_id}.jpg"
    
    # download image
    image_response = requests.get(image_url)
    if image_response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(image_response.content)
        print(f"Image downloaded: {filename}")

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
csv_path = "unique_text_to_post.csv"

# read into a list
with open(csv_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    #skip header
    next(reader)
    entries = [row[0] for row in reader if row]

text_obj = random.choice(entries)
print(f'random string: {text_obj}')


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
output_png = "test.png"
output_x, output_y = 1080, 1080

# calculate height needed to maintain aspect ratio
imgPIL = PILImage.open(img_source)
w_percent = output_x / float(imgPIL.width)
target_height = int(float(imgPIL.height) * w_percent)

# resize image to be smaller
img_resized = imgPIL.resize((output_x, target_height), PILImage.LANCZOS)

# crop to center
top = (target_height - output_y) // 2
bottom = top + output_y
# crop arguments: left, top, right, bottom
img_cropped = img_resized.crop((0, top, output_x, bottom))

# display(img_cropped)

# save to a temporary file to use with db.imagePixelColor() below
temp_path = 'temp_img.png'
img_cropped.save(temp_path)

# prepare blurred image for later (overlay to help text legibility)
img_blurred = img_cropped.filter(PILImageFilter.GaussianBlur(radius=10))
temp_path_blurred = 'temp_img_blurred.png'
img_blurred.save(temp_path_blurred)



# --------------------
# drawing instructions
# --------------------

with db.drawing():    
    # define canvas size
    db.newPage(output_x, output_y)

    # set background colour
    db.fill(0, 0, 0)
    #db.fill(db.random(), db.random(), db.random())
    db.rect(0, 0, db.width(), db.height())

    # ASCII art effect
    pixel_size = 16
    db.font('CourierNewPS-BoldMT')
    #db.font('CourierNewPSMT')
    db.fontSize(pixel_size)

    for x in range(0, output_x, 12):
        for y in range(0, output_y, pixel_size):
            color = db.imagePixelColor(temp_path, (x, y))
            if color:
                r, g, b, a = color
                db.fill(r, g, b, a)
                db.text("#", (x, y))

    # add blurred image
    blurred_img_obj = db.ImageObject()
    with blurred_img_obj:
        db.newPage(output_x, output_y)
        db.image(temp_path_blurred, (0, 0))
    db.image(blurred_img_obj, (0, 0), 0.5)

    # add text on top
    # test strings of different lengths
    #text_obj = 'Masculinity is not simply the physical and emotional dominance of a man it is also the physical and emotional vulnerability and dignity of a woman.'
    #text_obj = 'A manly man'

    bx, by, bw, bh = 64, 64, 960, 960
    db.fill(0, 0, 0, 0)
    db.rect(bx, by, bw, bh)

    db.font('AkzidenzGroteskPro-Bold')
    db.fontSize(104)
    db.lineHeight(104)
    db.tracking(-4)

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
    
    db.saveImage(output_png, imageResolution=300)
    display(Image(output_png))


# clean up
os.remove(temp_path) 