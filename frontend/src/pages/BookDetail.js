import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';

function BookDetail() {
    const { id } = useParams();
    const [book, setBook] = useState(null);
    const [recommendations, setRecommendations] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Fetch book details
        axios.get(`http://127.0.0.1:8000/api/books/${id}/`)
            .then(response => {
                setBook(response.data.book);
                setLoading(false);
            })
            .catch(err => {
                setLoading(false);
            });

        // Fetch recommendations
        axios.get(`http://127.0.0.1:8000/api/books/${id}/recommendations/`)
            .then(response => {
                setRecommendations(response.data.recommendations);
            })
            .catch(err => console.log(err));
    }, [id]);

    if (loading) return (
        <div className="flex justify-center items-center h-64">
            <div className="text-2xl text-blue-600 font-semibold">
                ⏳ Loading book details...
            </div>
        </div>
    );

    if (!book) return (
        <div className="text-red-500 text-center text-xl mt-10">
            ❌ Book not found
        </div>
    );

    return (
        <div>
            {/* Back Button */}
            <Link
                to="/"
                className="inline-block mb-6 text-blue-600 hover:text-blue-800 font-medium"
            >
                ← Back to Dashboard
            </Link>

            {/* Book Details Card */}
            <div className="bg-white rounded-xl shadow-lg p-8 mb-8">
                {/* Genre Badge */}
                <span className="inline-block bg-blue-100 text-blue-800 text-sm font-semibold px-3 py-1 rounded-full mb-4">
                    {book.ai_genre || book.genre || 'Unknown Genre'}
                </span>

                {/* Title */}
                <h1 className="text-4xl font-bold text-gray-800 mb-4">
                    {book.title}
                </h1>

                {/* Info Row */}
                <div className="flex flex-wrap gap-6 mb-6">
                    <div className="flex items-center gap-2">
                        <span className="text-yellow-400 text-xl">⭐</span>
                        <span className="text-gray-700 font-medium">
                            Rating: {book.rating} / 5
                        </span>
                    </div>
                    <div className="text-green-600 font-bold text-xl">
                        {book.price}
                    </div>
                    {book.ai_sentiment && (
                        <span className="inline-block bg-green-100 text-green-700 px-3 py-1 rounded-full">
                            Tone: {book.ai_sentiment}
                        </span>
                    )}
                </div>

                {/* AI Summary */}
                {book.ai_summary && (
                    <div className="bg-blue-50 rounded-xl p-5 mb-6">
                        <h2 className="text-lg font-bold text-blue-800 mb-2">
                            🤖 AI Summary
                        </h2>
                        <p className="text-gray-700 leading-relaxed">
                            {book.ai_summary}
                        </p>
                    </div>
                )}

                {/* Description */}
                {book.description && (
                    <div className="mb-6">
                        <h2 className="text-lg font-bold text-gray-800 mb-2">
                            📖 Description
                        </h2>
                        <p className="text-gray-600 leading-relaxed">
                            {book.description}
                        </p>
                    </div>
                )}

                {/* Book URL */}
                {book.book_url && (
                    <a
                        href={book.book_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-block bg-blue-600 text-white px-6 py-3 rounded-xl hover:bg-blue-700 transition duration-200 font-medium"
                    >
                        🔗 View Original Book
                    </a>
                )}
            </div>

            {/* Recommendations */}
            {recommendations.length > 0 && (
                <div>
                    <h2 className="text-2xl font-bold text-gray-800 mb-4">
                        📚 You Might Also Like
                    </h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {recommendations.map(rec => (
                            <Link to={`/book/${rec.id}`} key={rec.id}>
                                <div className="bg-white rounded-xl shadow-md hover:shadow-xl transition duration-300 p-5 border border-gray-100 hover:border-blue-300">
                                    <span className="inline-block bg-blue-100 text-blue-800 text-xs font-semibold px-2 py-1 rounded-full mb-2">
                                        {rec.ai_genre || rec.genre}
                                    </span>
                                    <h3 className="font-bold text-gray-800 mb-2">
                                        {rec.title}
                                    </h3>
                                    <div className="text-yellow-400">
                                        ⭐ {rec.rating} / 5
                                    </div>
                                    <div className="text-green-600 font-semibold">
                                        {rec.price}
                                    </div>
                                </div>
                            </Link>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}

export default BookDetail;