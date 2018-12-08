from background_task import background
from .post_scraper import PostScraper


# python manage.py process_tasks <- add this to docker
# https://django-background-tasks.readthedocs.io/en/latest/
@background(schedule=60)
def scrape_blog():
    scraper = PostScraper()
    scraper.execute()
