import os
import sys
import django
import requests
from bs4 import BeautifulSoup

# Setup Django so we can use our models
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
django.setup()

from books.models import Book

# Base URL of the website we are scraping
BASE_URL = "http://books.toscrape.com/"

# This dictionary converts word ratings to numbers
RATING_MAP = {
    "One": "1",
    "Two": "2",
    "Three": "3",
    "Four": "4",
    "Five": "5"
}

def get_book_description(book_url):
    """
    Visit individual book page and get its description
    """
    try:
        response = requests.get(book_url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find description on the book's own page
        description = soup.find('article', class_='product_page')
        if description:
            desc_text = description.find('p', recursive=False)
            if desc_text:
                return desc_text.text.strip()
        return ""
    except:
        return ""

def get_book_genre(book_url):
    """
    Get the genre/category of the book from its page
    """
    try:
        response = requests.get(book_url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Genre is in the breadcrumb navigation
        breadcrumb = soup.find('ul', class_='breadcrumb')
        if breadcrumb:
            items = breadcrumb.find_all('li')
            if len(items) >= 3:
                return items[2].text.strip()
        return ""
    except:
        return ""

def scrape_books(max_pages=5):
    """
    Main scraping function
    Scrapes books from multiple pages and saves to database
    """
    print("🚀 Starting scraper...")
    books_saved = 0
    page = 1

    while page <= max_pages:
        # Build the URL for each page
        if page == 1:
            url = BASE_URL
        else:
            url = f"{BASE_URL}catalogue/page-{page}.html"

        print(f"📄 Scraping page {page}...")

        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all books on this page
            book_list = soup.find_all('article', class_='product_pod')

            if not book_list:
                print("No more books found, stopping.")
                break

            for book in book_list:
                try:
                    # Get title
                    title = book.find('h3').find('a')['title']

                    # Get price
                    price = book.find('p', class_='price_color').text.strip()

                    # Get rating (comes as a word like "Three")
                    rating_class = book.find('p', class_='star-rating')['class'][1]
                    rating = RATING_MAP.get(rating_class, "0")

                    # Build full URL for this book
                    relative_url = book.find('h3').find('a')['href']
                    if '../' in relative_url:
                        relative_url = relative_url.replace('../', '')
                    book_url = f"{BASE_URL}catalogue/{relative_url}"

                    # Get description and genre from book's own page
                    print(f"   📖 Getting details for: {title}")
                    description = get_book_description(book_url)
                    genre = get_book_genre(book_url)

                    # Check if book already exists in database
                    if not Book.objects.filter(title=title).exists():
                        # Save to database
                        Book.objects.create(
                            title=title,
                            price=price,
                            rating=rating,
                            description=description,
                            book_url=book_url,
                            genre=genre,
                        )
                        books_saved += 1
                        print(f"   ✅ Saved: {title}")
                    else:
                        print(f"   ⏭️ Already exists: {title}")

                except Exception as e:
                    print(f"   ❌ Error scraping book: {e}")
                    continue

        except Exception as e:
            print(f"❌ Error on page {page}: {e}")
            break

        page += 1

    print(f"\n🎉 Scraping complete! {books_saved} books saved to database.")

# Run the scraper
if __name__ == "__main__":
    scrape_books(max_pages=5)  # Scrapes 5 pages = ~100 books