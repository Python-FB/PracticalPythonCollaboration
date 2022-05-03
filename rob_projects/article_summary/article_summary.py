from wand.image import Image
from wand.color import Color
# from wand.drawing import Drawing
# from wand.display import display
from wand.font import Font
import requests
# from sumy.parsers.plaintext import PlaintextParser
# from sumy.nlp.tokenizers import Tokenizer
# from sumy.summarizers.luhn import LuhnSummarizer as Summarizer
# from sumy.nlp.stemmers import Stemmer
from newspaper import Article
from random import choice
from transformers import pipeline
import os

# 2 types of summarizing: extractive and abstractive

os.environ["CUDA_VISIBLE_DEVICES"] = "0"

url = "https://arstechnica.com/science/2018/06/first-space-then-auto-now-elon-musk-quietly-tinkers-with-education/"
# url = 'https://www.technologyreview.com/2022/04/22/1050394/artificial-intelligence-for-the-people/'

article  =  Article(url)
article.download()
article.parse()

try:
    image_url = choice(list(article.images))
except Exception as ex:
    print(ex)
    image_url = 'https://i.imgur.com/YobrZ8r.png'

image_blob = requests.get(image_url)
    
dims = (1080, 1920)
ideal_width = dims[0]
ideal_height = dims[1]
ideal_aspect = ideal_width / ideal_height

with Image(blob=image_blob.content) as img:
    size = img.size

width = size[0]
height = size[1]
aspect = width/height

LANGUAGE = "english"
SENTENCES_COUNT = 10

# parser = PlaintextParser.from_string(article.text, Tokenizer(LANGUAGE))
# stemmer = Stemmer(LANGUAGE)
# summarizer = Summarizer(stemmer)
# sentences = [str(sentence) for sentence in summarizer(parser.document, SENTENCES_COUNT) if len(str(sentence)) <= 128]
# CAPTION = ' '.join(sentences)

# summarizer = pipeline("summarization")
#     # "summarization",
#     # model="t5-base",
#     # tokenizer="t5-base", 
#     # framework="tf")
# article_lines = article.doc.body.text_content().split('\n')
# text = article.text

# print(article.text)

summarizer = pipeline('summarization')
# text = ' '.join([line.strip() for line in article_lines if len(line.strip()) > 50])

subsection = article.text[:2048]

CAPTION = summarizer(subsection, max_length=1024)[0]['summary_text']


if aspect > ideal_aspect:
    new_width = int(ideal_aspect * height)
    resize = (
        (0, 0, int(new_width), int(height)),
        (int(width-new_width), 0, int(width), int(height))
    )
else:
    new_height = int(width / ideal_aspect)
    resize = (
        (0, 0, int(width), int(new_height)), 
        (0, int(height-new_height), int(width), int(height))
    )

FONT_SIZE = int(resize[0][3]/(25))

with Image(blob=image_blob.content) as canvas:
    print(canvas.width)
    canvas.crop(*resize[0])
    print(canvas.width)
    canvas.font = Font("SanFranciscoDisplay-Bold.otf", 
                        size=FONT_SIZE, 
                        color=Color('black'),
                        # stroke_color=Color('white'))
    caption_width = int(canvas.width/1.2)
    margin_left = int((canvas.width-caption_width)/2)
    margin_top = int(canvas.height/2)
    canvas.caption(CAPTION, gravity='center', 
                   width=caption_width, left=margin_left,
                   top=margin_top)
    canvas.format = "jpg"
    canvas.save(filename='text_overlayed_1.jpg')

with Image(blob=image_blob.content) as canvas:
    canvas.crop(*resize[1])
    canvas.font = Font("SanFranciscoDisplay-Bold.otf", 
                        size=FONT_SIZE, 
                        color=Color('black'),
                        # stroke_color=Color('white'))
    caption_width = int(canvas.width/1.2)
    margin_left = int((canvas.width-caption_width)/2)
    margin_top = 30
    canvas.caption(CAPTION, gravity='north', 
                   width=caption_width, left=margin_left,
                   top=margin_top)
    canvas.format = "jpg"
    canvas.save(filename='text_overlayed_2.jpg')