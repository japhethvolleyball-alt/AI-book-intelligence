import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

function Dashboard() {
    const [books, setBooks] = useState([]);
    const [loading, setLoading] = useState(true);
    const [search, setSearch] = useState('');
    const [error, setError] = useState('');

    useEffect(() => {
        // Fetch all books from Django API
        axios.get('http://127.0.0.1:8000/api/books/')
            .then(response => {
                setBooks(response.data.books);
                setLoading(false);
            })
            .catch(err => {
                setError('Failed to load books');
                setLoading(false);
            });
    }, []);

    // Filter books based on search
    const filteredBooks = books.filter(book =>
        book.title.toLowerCase().includes(search.toLowerCase()) ||
        book.genre.toLowerCase().includes(search.toLowerCase())
    );

    if (loading) return (
        <div className="flex justify-center items-center h-64">
            <div className="text-2xl text-blue-600 font-semibold">
                ⏳ Loading books...
            </div>
        </div>
    );

    if (error) return (
        <div className="text-red-500 text-center text-xl mt-10">
            ❌ {error}
        </div>
    );

    return (
        <div>
            {/* Header */}
            <div className="mb-8">
                <h1 className="text-4xl font-bold text-gray-800 mb-2">
                    📚 Book Dashboard
                </h1>
                <p className="text-gray-500">
                    {books.length} books available
                </p>
            </div>

            {/* Search Bar */}
            <div className="mb-6">
                <input
                    type="text"
                    placeholder="🔍 Search by title or genre..."
                    value={search}
                    onChange={e => setSearch(e.target.value)}
                    className="w-full px-4 py-3 rounded-xl border border-gray-300 shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 text-lg"
                />
            </div>

            {/* Books Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                {filteredBooks.map(book => (
                    <Link to={`/book/${book.id}`} key={book.id}>
                        <div className="bg-white rounded-xl shadow-md hover:shadow-xl transition duration-300 p-5 h-full border border-gray-100 hover:border-blue-300">
                            {/* Genre Badge */}
                            <span className="inline-block bg-blue-100 text-blue-800 text-xs font-semibold px-2 py-1 rounded-full mb-3">
                                {book.ai_genre || book.genre || 'Unknown'}
                            </span>

                            {/* Title */}
                            <h2 className="text-lg font-bold text-gray-800 mb-2 line-clamp-2">
                                {book.title}
                            </h2>

                            {/* Rating */}
                            <div className="flex items-center gap-1 mb-2">
                                <span className="text-yellow-400">⭐</span>
                                <span className="text-gray-600 text-sm">
                                    {book.rating} / 5
                                </span>
                            </div>

                            {/* Price */}
                            <div className="text-green-600 font-semibold mb-3">
                                {book.price}
                            </div>

                            {/* Summary */}
                            <p className="text-gray-500 text-sm line-clamp-3">
                                {book.ai_summary || book.description || 'No description available'}
                            </p>

                            {/* Sentiment */}
                            {book.ai_sentiment && (
                                <div className="mt-3">
                                    <span className="inline-block bg-green-100 text-green-700 text-xs px-2 py-1 rounded-full">
                                        {book.ai_sentiment}
                                    </span>
                                </div>
                            )}
                        </div>
                    </Link>
                ))}
            </div>

            {/* No Results */}
            {filteredBooks.length === 0 && (
                <div className="text-center text-gray-500 text-xl mt-20">
                    No books found for "{search}"
                </div>
            )}
        </div>
    );
}

export default Dashboard;