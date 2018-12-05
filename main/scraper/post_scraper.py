import bs4
import requests

# check if post is already scraped (check by title in db)
# save in db
# emit event https://github.com/transifex/django-events

headers = {}
url = 'https://teonite.com/blog'
url_prefix = 'https://teonite.com'  # this can be solved cleaner because there is absolute url and relative url
title_class = 'post-title'

author_class = 'author-content'


def get_elements_from_page(url, css_class):
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = bs4.BeautifulSoup(response.text, 'lxml')
    elems = soup.select('.' + css_class)
    return elems


def get_posts(url, base_url, page=1):
    # todo please build urls in some legit way
    # return tuple name -> url
    posts = get_elements_from_page(url, title_class)
    for a in posts:
        title = a.text.strip()
        # at this point we could check is post saved in db
        print(title)
        post_url = a.find('a')['href']
        content = get_post_content(base_url + post_url)
        print(content)
    return posts


def get_post_content(post_url):
    content_class = 'post-content'
    return get_elements_from_page(post_url, content_class)[0].text.strip() #dokoptuj autora


get_posts(url, url_prefix)




# if no post left then go to class older-posts and follow link until there is no older post
