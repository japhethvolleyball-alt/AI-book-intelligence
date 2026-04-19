import os
import django
import sys
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
django.setup()

from books.models import Book

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_summary(title, description, genre):
    """
    Generate a short AI summary for a book
    """
    try:
        prompt = f"""
        Generate a short 2-3 sentence summary for this book:
        Title: {title}
        Genre: {genre}
        Description: {description}
        
        Keep it concise and engaging.
        """
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating summary: {e}")
        return ""

def classify_genre(title, description):
    """
    Use AI to classify the genre of a book
    """
    try:
        prompt = f"""
        Classify this book into ONE genre from this list:
        Fiction, Non-Fiction, Mystery, Romance, Science Fiction, 
        Fantasy, Horror, Biography, History, Self-Help, Children, Poetry
        
        Title: {title}
        Description: {description}
        
        Reply with ONLY the genre name, nothing else.
        """
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=10
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error classifying genre: {e}")
        return ""

def analyze_sentiment(description):
    """
    Analyze the sentiment/tone of a book description
    """
    try:
        prompt = f"""
        Analyze the sentiment of this book description in ONE word.
        Choose from: Positive, Negative, Neutral, Dark, Uplifting, Mysterious, Romantic
        
        Description: {description}
        
        Reply with ONLY one word, nothing else.
        """
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=10
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error analyzing sentiment: {e}")
        return ""

def generate_insights_for_all_books():
    """
    Generate AI insights for all books in database
    """
    # Get all books that don't have AI summary yet
    books = Book.objects.filter(ai_summary="")
    total = books.count()
    
    print(f"🤖 Generating AI insights for {total} books...")
    
    for index, book in enumerate(books, 1):
        print(f"📖 Processing {index}/{total}: {book.title}")
        
        # Generate all 3 insights
        summary = generate_summary(book.title, book.description, book.genre)
        ai_genre = classify_genre(book.title, book.description)
        sentiment = analyze_sentiment(book.description)
        
        # Save to database
        book.ai_summary = summary
        book.ai_genre = ai_genre
        book.ai_sentiment = sentiment
        book.save()
        
        print(f"   ✅ Summary: {summary[:50]}...")
        print(f"   ✅ Genre: {ai_genre}")
        print(f"   ✅ Sentiment: {sentiment}")

# Run the insight generation
if __name__ == "__main__":
    generate_insights_for_all_books()