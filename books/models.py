from django.db import models

class Book(models.Model):
    # Basic book information scraped from website
    title = models.CharField(max_length=500)
    author = models.CharField(max_length=300, default='Unknown')
    price = models.CharField(max_length=50, blank=True)
    rating = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    book_url = models.URLField(max_length=1000, blank=True)
    genre = models.CharField(max_length=200, blank=True)
    
    # AI generated fields
    ai_summary = models.TextField(blank=True)
    ai_genre = models.CharField(max_length=200, blank=True)
    ai_sentiment = models.CharField(max_length=100, blank=True)
    
    # When was this book added
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class BookChunk(models.Model):
    # This stores pieces of book text for RAG pipeline
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='chunks')
    chunk_text = models.TextField()
    chunk_index = models.IntegerField(default=0)

    def __str__(self):
        return f"Chunk {self.chunk_index} of {self.book.title}"


class ChatHistory(models.Model):
    # Saves every question and answer for chat history bonus
    question = models.TextField()
    answer = models.TextField()
    asked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question[:50]