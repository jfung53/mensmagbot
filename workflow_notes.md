## Workflow Notes to Self

1. conda install scrapy

2. create project folder
scrapy startproject <projectname>

3. get selectors
scrapy shell 'url.com' or use notebook

4. create script.py file in /spider folder
touch script.py

5. crawl
scrapy crawl spidername -o output.json -s CLOSESPIDER_PAGECOUNT=8000

6. clean up, analyze data (e.g. gq_analysis.ipynb)

7. train language model (huggingface trl)

8. generate text (randomize sentence starters)

9. create virtual environment
python -m venv .venv
source .venv/bin/activate
pip install python-dotenv instabot pillow git+https://github.com/typemytype/drawbot
pip freeze > requirements.txt

10. run [drawbot](https://github.com/typemytype/drawbot)/create_image.py to create image

11. TBD: post on instagram with [instabot](https://github.com/ohld/igbot/blob/master/examples/autopost/README.md), or use meta api, or maybe twitter