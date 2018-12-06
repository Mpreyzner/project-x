from background_task import background
from .post_scraper import PostScraper


# python manage.py process_tasks <- add this to docker
# @background(schedule=15 * 60)
@background(schedule=1)
def scrape_blog():
    scraper = PostScraper
    scraper.execute()
