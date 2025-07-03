# Men's Mag Bot

A twitter bot that posts hallucinations about masculinity using GPT-2 trained on articles from men's magazines.
This is a school project and for educational use only. 

## Proposal

I'm interested in exploring how masculinity is defined in popular culture.  I plan to scrape articles from men's magazines to create a dataset which I will use to train a language model to generate text about masculinity to post daily on social media.  I'm hoping to use the drawbot python module to style the generated text and post it as an image on instagram.  The tutorial presentation will cover how to create this image and maybe maybe also how to post it on instagram using instabot.  

## Workflow Notes

1. conda install scrapy

2. create project folder
scrapy startproject <yourproject>

3. get selectors
scrapy shell 'url.com'

4. create script.py file in /spider folder
touch script.py

5. crawl
scrapy crawl yourspider -o output.json -s CLOSESPIDER_PAGECOUNT=8000

6. clean up, analyze data

7. train language model (huggingface trl)

8. generate text (randomize sentence starters)

9. create image with drawbot to post on instagram or twitter