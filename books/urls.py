from django.urls import path
from . import views

urlpatterns = [
    # GET APIs
    path('books/', views.get_all_books, name='get_all_books'),
    path('books/<int:pk>/', views.get_book_detail, name='get_book_detail'),
    path('books/<int:pk>/recommendations/', views.get_recommendations, name='get_recommendations'),
    path('chat-history/', views.get_chat_history, name='get_chat_history'),

    # POST APIs
    path('books/upload/', views.upload_book, name='upload_book'),
    path('ask/', views.ask_question, name='ask_question'),
]