# Men's Mag Bot

A bot that posts hallucinations about masculinity using GPT-2 trained on articles from men's magazines.  

Created for a school project. 

# In-class Tutorial

I've already generated about 1000 lines of text about what masculinity means. This text will be used when we run the create_image.py script.  

This tutorial goes through how to:
- configure the python environment
- download a random image from Unsplash based on a keyword search
- grab a random line of text, and
- generate a stylized image to post on social media

## 1. :file_folder: Download Folders

1. On the [main repository page](https://github.com/jfung53/mensmagbot) click on the green Code button to "Download ZIP"
2. We won't need the 'mensmags' folder, just ignore it.

## 2. :earth_asia: Configure a Virtual Environment

I did this in the VS Code terminal.  

1. Open VS Code
2. File - New Window - and open the downloaded `/mensmagsbot/` folder
3. In the console, either set up a .venv or install the packages.  
This is not expert advice. 
```console
    python -m venv .venv
    source .venv/bin/activate
    pip install python-dotenv instabot pillow git+https://github.com/typemytype/drawbot
    pip freeze > requirements.txt
```
4. Alternatively, I think you can just `pip install` the packages in your base python but maybe that's not the best idea in the world.  

## 3. :camera: Set Up the Unsplash API

1. Create (or log into) an account on [Unsplash](https://unsplash.com)
2. Go to the [Unsplash Developers](https://unsplash.com/developers) page
3. Click on **Your Apps**
4. Make a new application, I named mine "man-o-matic"
5. You should end up on the app page for your new app. If not, click on it from the **Your Apps** page.
6. Scroll down to the **Keys** section
7. We'll need the **ACCESS KEY**

## 4. :snake: Configure the Script

1. Open VS Code
2. File - New Window - and open the downloaded `/mensmagsbot/` folder
3. In the `/drawbot/` folder open up `create_image.py`
4. For the purposes of this tutorial, we can delete or comment out the following lines:
```python
# hide or delete this line
from dotenv import load_dotenv
```
```python
# hide or delete this line, too
load_dotenv()
ACCESS_KEY = os.getenv("ACCESS_KEY")
```
5. Under `params` replace `ACCESS KEY` with your own Unsplash key
```python
params = {
    'query': SEARCH_QUERY,
    'client_id': ACCESS_KEY, # replace ACCESS_KEY with your own Unsplash key
    'orientation': 'portrait', 
    'dummy': random.randint(0, 999999) 
}
```
6. We should now be able to run the script, but first we'll configure it some more.

## 5. :fireworks: Configure the image parameters

First, we'll configure the search query to get a photo from Unsplash.  
We're using the `random photo endpoint` from the API that can be narrowed with a few parameters.  

1. Above `params` find the `SEARCH_QUERY` variable.  
Replace my keywords, `'man in nature'`, with your own
```python
# define keyword search query
SEARCH_QUERY = 'man in nature'
```
2. Back in `params` you can also choose the orientation of the photo. For this script, `portrait` works best, so just leave it as is.
3. The script is ready to run. 

## 6. :crystal_ball: Run the script to create an image and find out what it means to be a man

Open the VS Code terminal to run the script.
```console
python create_image.py
```

That's it! `output.png` should appear in the `/drawbot/` folder.  

**Note**: Every time you run the script, `output.png` gets overwritten.  

## 7. :fireworks: Customize the drawing further

Here are some ways you can play around with the image and text.

### :point_right: Enter your own text

Scroll to the `get generated text` section of the script.  
Look for the `text_obj` variable.  
Instead of a random choice, enter your own.  
Fewer than 140 characters works best. 
```python
text_obj = random.choice(entries)
print(f'Random text chosen: {text_obj}')
# text_obj = 'A manly man'
```

### :point_right: Change the background colour

Scroll to the `drawing instructions` section.  
The background is a rectangle that is set to the width and height of the canvas.  
DrawBot's `fill` function takes 3 arguments: values `(0-255)` for red, green, and blue, and an optional alpha `(0-1)` value for transparency.  
Enter your own values or exchange my black `(0, 0, 0)` line with the one underneath that uses DrawBot's `random()` colour function.  
```python
# set background colour (r, g, b, alpha)
db.fill(0, 0, 0)
#db.fill(db.random(), db.random(), db.random())
db.rect(0, 0, db.width(), db.height())
```

### :point_right: Change the font of the quote

To change the typeface you'll need to add this chunk of code somewhere.  
It uses DrawBot's `installedFonts()` function to print a list of all the fonts installed on your computer.  Maybe you have a very masculine font that would work well here.  
```python
# get list of font names
fonts_list = db.installedFonts()
for font in fonts_list:
    print(font)
```
In the same `drawing instructions` section look for the code below.  
Paste your font name here in the `db.font()` function.   
```python
    db.font('AkzidenzGroteskPro-Bold')
    db.fontSize(104)
    db.lineHeight(104) # line spacing
    db.tracking(-4) # distance between characters
```

### :point_right: Change the ASCII art style pixelated characters

Modify the `ASCII art effect` which is found in the same `drawing instructions` section under the background colour.  

Change the font (see instructions above) here in `db.font()`:
```python
# ASCII art effect
    print('Generating ASCII pixels')
    pixel_size = 16
    db.font('CourierNewPS-BoldMT')
    db.fontSize(pixel_size)
```
`pixel_size` refers to the size of the cell that each character (I chose `#`) sits in.  
Change that character here in `db.text()`:
```python
    for x in range(0, output_x, 12): # 12 is the pixel spacing between each cell
        for y in range(0, output_y, pixel_size):
            color = db.imagePixelColor(temp_path, (x, y))
            if color:
                r, g, b, a = color
                db.fill(r, g, b, a)
                db.text("#", (x, y))
```
I know that there is some way to vary the `db.text()` character according to colour but I haven't figured it out yet.  

### :point_right: Change the colour of the chromatic aberration effect

Change the colours of the teal and red colour fringing around the white text.  
I've included the code to use a `random()` colour, or you can set your own RGB values with an optional alpha.  
```python
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
```

## 8. :ghost: What's Next

I still need to get the instagram automation working.  


