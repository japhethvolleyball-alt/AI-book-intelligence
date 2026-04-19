from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book, ChatHistory
from .serializers import BookSerializer, ChatHistorySerializer
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@api_view(['GET'])
def get_all_books(request):
    """
    Returns list of all books in database
    """
    try:
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response({
            'success': True,
            'count': books.count(),
            'books': serializer.data
        })
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_book_detail(request, pk):
    """
    Returns details of a single book
    """
    try:
        book = Book.objects.get(pk=pk)
        serializer = BookSerializer(book)
        return Response({
            'success': True,
            'book': serializer.data
        })
    except Book.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Book not found'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_recommendations(request, pk):
    """
    Recommends similar books based on genre
    """
    try:
        # Get the current book
        book = Book.objects.get(pk=pk)
        
        # Find books with same genre
        similar_books = Book.objects.filter(
            genre=book.genre
        ).exclude(pk=pk)[:5]
        
        # If not enough books found use ai_genre
        if similar_books.count() < 3:
            similar_books = Book.objects.filter(
                ai_genre=book.ai_genre
            ).exclude(pk=pk)[:5]

        serializer = BookSerializer(similar_books, many=True)
        return Response({
            'success': True,
            'book': book.title,
            'recommendations': serializer.data
        })
    except Book.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Book not found'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def ask_question(request):
    """
    RAG pipeline - answers questions about books
    """
    try:
        question = request.data.get('question', '')
        
        if not question:
            return Response({
                'success': False,
                'error': 'Please provide a question'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Get all books as context
        books = Book.objects.all()[:20]
        
        # Build context from books
        context = ""
        for book in books:
            context += f"""
            Title: {book.title}
            Genre: {book.genre}
            AI Genre: {book.ai_genre}
            Summary: {book.ai_summary}
            Sentiment: {book.ai_sentiment}
            Price: {book.price}
            Rating: {book.rating}
            ---
            """

        # Build prompt with context
        prompt = f"""
        You are a helpful book assistant. Use the following book data to answer the question.
        Always cite which books you are referencing in your answer.
        
        Book Data:
        {context}
        
        Question: {question}
        
        Provide a helpful, detailed answer based on the book data above.
        """

        # Call Groq API
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )

        answer = response.choices[0].message.content.strip()

        # Save to chat history
        ChatHistory.objects.create(
            question=question,
            answer=answer
        )

        return Response({
            'success': True,
            'question': question,
            'answer': answer
        })

    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def upload_book(request):
    """
    Manually upload a book
    """
    try:
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'book': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_chat_history(request):
    """
    Returns all chat history
    """
    try:
        history = ChatHistory.objects.all().order_by('-asked_at')
        serializer = ChatHistorySerializer(history, many=True)
        return Response({
            'success': True,
            'history': serializer.data
        })
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)