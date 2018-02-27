"""Pull articles from el tiempo site

The idea behind this script is to make my life easier when uploading
news to the corriente site.

TODO List
0. Get the url from params (DONE)
1. Get the site. (DONE)
2. Use beautiful soup. (DONE)
3. ¿Get the OG Image? (DONE)
4. Upload to site. (DONE)

New things:

1. Include tags from args.
2. Include categoría adecuada desde args.
3. Crear como borrador desde args.
4. Adicionar imagen a media manager.
5. Incluir og_image adecuada desde url externa.


"""

import argparse
import datetime as dt
import pprint
import requests
from bs4 import BeautifulSoup
from mezzanine_client import Mezzanine
from mezzanine_client.utils import str_header, str_green

# Initialise Mezzanine API client
api = Mezzanine()
published_posts = api.get_posts(offset=0, limit=10)

print(published_posts[0]['categories'])
print(published_posts[0]['tags'])
print(published_posts[0]['slug'])

# dict_keys(['id', 'user', 'publish_date', 'updated', 'title',
# 'content', 'excerpt', 'slug', 'url', 'short_url', 'categories',
# 'allow_comments', 'comments_count', 'comments', 'tags',
# 'featured_image', 'description'])
# the title and content are required
# the except is an abstract of the article.

# end mezzanine code

parser = argparse.ArgumentParser(description='Upload articule from "el tiempo".')
parser.add_argument('link', nargs=1, help='The El Tiempo link')

args = parser.parse_args()

link = args.link[0]

result = requests.get(link)

content = result.content

soup = BeautifulSoup(content, 'html.parser')

title = soup.find('div', 'node-title').find('h1').contents[0]
lead = soup.find('div', 'node-teaser').contents[0]

the_og_image = soup.find('meta', property='og:image')

the_content = soup.find('div', 'node-body')

new_post = {}
new_post['title'] = title
new_post['content'] = f"{lead}\n\n{the_content}\n\nFuente: {link}"
if the_og_image:
    new_post['featured_image'] = the_og_image['content']

new_post['categories'] = "Artículo, Noticia"
new_post['tags'] = 'Ciencia, Colciencias, imposturas'
new_post['publish_date'] = (dt.datetime.utcnow() + dt.timedelta(hours=18)).isoformat()
new_post['allow_comments'] = True

response = api.create_post(new_post)
pprint.pprint(response)

if 'id' in response:
    print(str_green('Blog post successfully published with ID #{}'.format(response['id'])))
