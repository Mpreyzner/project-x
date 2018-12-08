import bs4
import requests
from urllib.parse import urlparse
from .models import Post, Author


# emit event https://github.com/transifex/django-events with post content and details

class PostScraper:
    url = 'https://teonite.com/blog'
    next_page_class = 'older-posts'

    def execute(self):
        parsed_url = urlparse(self.url)
        # https://teonite.com/blog/page/2/
        # or just change page parameter ??
        finished = False
        url = self.url
        while not finished:
            self.get_posts(url)
            next_page_path = self.get_elements_from_page(url, self.next_page_class)[0]['href']
            # check if given index exists, if it doesn't then we're finished
            url = parsed_url.scheme + '://' + parsed_url.netloc + next_page_path
            print("processing: " + url)
        return False

    def get_elements_from_page(self, url, css_class):
        response = requests.get(url)
        response.raise_for_status()
        soup = bs4.BeautifulSoup(response.text, 'lxml')
        elems = soup.select('.' + css_class)
        return elems

    def get_posts(self, url):
        # TODO consider separating data retrival and interaction with db
        # maybe it can be done as mass save in only 1 query instead
        title_class = 'post-title'
        parsed_url = urlparse(url)
        posts = self.get_elements_from_page(url, title_class)
        for a in posts:
            title = a.text.strip()

            post_exists = Post.objects.filter(title=title).exists()
            if post_exists:
                continue
            # print(title)
            post_url = a.find('a')['href']
            content, author = self.get_post_details(
                (parsed_url.scheme + '://' + parsed_url.netloc + post_url))  # use some function for url
            # print(content)
            # print(author)

            author_exists = Author.objects.filter(name=author).exists()
            if not author_exists:
                auth = Author(name=author, tokenized_name=author.lower().replace(" ", ""))
                auth.save()
            else:
                auth = Author.objects.get(name=author)

            # TODO add language recognition
            post = Post(title=title, author=auth, content=content, language='pl')
            post.save()
            # emit event here
        return posts

    def get_post_details(self, post_url):
        content_class = 'post-content'
        author_class = 'author-content'
        author = self.get_elements_from_page(post_url, author_class)[0].find('h4').text.strip()
        # what if there is no such element??
        # this could be optimized so we would fetch the site only once,
        # instead of requesting 1 time for author and another for content
        content = self.get_elements_from_page(post_url, content_class)[0].text.strip()
        # TODO make unpacking explicit
        return content, author
