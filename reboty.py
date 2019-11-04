# Scrapper for YouTube videos. Gets title, description, url, thumbnail, translates the content with Google Translate and store results in a CSV file.
# This was made for Wordpress Theme Upvote with its Story post format to work with an CSV importer. 
from bs4 import BeautifulSoup
import requests
import csv

from googletrans import Translator
translator = Translator()

source = requests.get("https://www.youtube.com/results?search_query=desired+youtube+query+here").text
soup = BeautifulSoup(source, 'lxml')

csv_file = open('rebotytext.csv','w', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['_story_url','post_title', 'post_content', 'featured_image', 'post_status', 'post_author', 'post_name', 'story_tag', 'story_category', 'post_type'])

for content in soup.find_all('div', class_= "yt-lockup-content"):
    try:
        linktr = content.h3.a.get('href')
        linkid = linktr.replace('watch?v=','')
        link = 'https://youtu.be' + linkid

        titletr = content.h3.a.text
        titletd = translator.translate(titletr, dest='es')
        title = titletd.text

        descriptiontr = content.find('div', class_="yt-lockup-description yt-ui-ellipsis yt-ui-ellipsis-2").text
        descriptiontd = translator.translate(descriptiontr, dest='es')
        description = descriptiontd.text

        thumbnail = 'http://img.youtube.com/vi'+ linkid + '/0.jpg'

        status = 'draft'
        author = 'Donovan'
        slug = title
        tag = 'tag1, tag2, tag3'
        cat = 'category-slug'
        posttype ='story'



    except Exception as e:
        description = None

    csv_writer.writerow([link, title, description, thumbnail, status, author, slug, tag, cat, posttype ])

csv_file.close()
