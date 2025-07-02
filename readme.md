# Men's Mag Bot

A twitter bot that posts hallucinations about masculinity using GPT-2 trained on articles from men's magazines.
This is a school project and for educational use only. 

## Workflow

conda install scrapy
or
pip install scrapy

1. create project folder
scrapy startproject <yourproject>

2. get selectors
scrapy shell 'url.com'

3. create script.py file in /spider folder
touch script.py

4. crawl
scrapy crawl yourspider -o output.json -s CLOSESPIDER_PAGECOUNT=8000
