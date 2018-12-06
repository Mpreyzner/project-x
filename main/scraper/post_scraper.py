import bs4
import requests
from urllib.parse import urlparse, urlunparse

# check if post is already scraped (check by title in db)
# save in db -> author as well as post
# emit event https://github.com/transifex/django-events with post content and details

url = 'https://teonite.com/blog'
title_class = 'post-title'
next_page_class = 'older-posts'


class PostScraper():
    def execute():
        print('Working wooohoo')
        return False


def get_elements_from_page(url, css_class):
    response = requests.get(url)
    response.raise_for_status()
    soup = bs4.BeautifulSoup(response.text, 'lxml')
    elems = soup.select('.' + css_class)
    return elems


def get_posts(url, page=1):
    parsed_url = urlparse(url)
    posts = get_elements_from_page(url, title_class)
    for a in posts:
        title = a.text.strip()
        # at this point we could check is post saved in db
        # print(title)
        post_url = a.find('a')['href']
        content, author = get_post_details(
            (parsed_url.scheme + '://' + parsed_url.netloc + post_url))  # use some function for url
        # print(content)
        # print(author)
        # emit event here
    return posts


def get_post_details(post_url):
    content_class = 'post-content'
    author_class = 'author-content'
    author = get_elements_from_page(post_url, author_class)[0].find('h4').text.strip()
    content = get_elements_from_page(post_url, content_class)[0].text.strip()
    return content, author
#
#
# parsed_url = urlparse(url)
# # https://teonite.com/blog/page/2/
# # or just change page parameter ??
# finished = False
# while not finished:
#     # get_posts(url)
#     next_page_path = get_elements_from_page(url, next_page_class)[0]['href']
#     # check if given index exists, if it doesn't then we're finished
#     url = parsed_url.scheme + '://' + parsed_url.netloc + next_page_path
#     print(url)
