import React, { useState, useEffect } from 'react';
import axios from 'axios';

function QandA() {
    const [question, setQuestion] = useState('');
    const [answer, setAnswer] = useState('');
    const [loading, setLoading] = useState(false);
    const [history, setHistory] = useState([]);
    const [error, setError] = useState('');

    useEffect(() => {
        // Load chat history
        axios.get('http://127.0.0.1:8000/api/chat-history/')
            .then(response => {
                setHistory(response.data.history);
            })
            .catch(err => console.log(err));
    }, []);

    const handleAsk = async () => {
        if (!question.trim()) return;

        setLoading(true);
        setError('');
        setAnswer('');

        try {
            const response = await axios.post('http://127.0.0.1:8000/api/ask/', {
                question: question
            });

            setAnswer(response.data.answer);

            // Add to history
            setHistory(prev => [{
                question: question,
                answer: response.data.answer,
                asked_at: new Date().toISOString()
            }, ...prev]);

        } catch (err) {
            setError('Failed to get answer. Please try again.');
        }

        setLoading(false);
    };

    return (
        <div>
            {/* Header */}
            <div className="mb-8">
                <h1 className="text-4xl font-bold text-gray-800 mb-2">
                    🤖 Book Q&A
                </h1>
                <p className="text-gray-500">
                    Ask anything about the books in our collection!
                </p>
            </div>

            {/* Question Input */}
            <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
                <textarea
                    value={question}
                    onChange={e => setQuestion(e.target.value)}
                    placeholder="Ask a question about books... e.g. What are the best mystery books? Which books have positive sentiment?"
                    className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 text-lg resize-none"
                    rows={4}
                />

                <button
                    onClick={handleAsk}
                    disabled={loading || !question.trim()}
                    className="mt-4 bg-blue-600 text-white px-8 py-3 rounded-xl hover:bg-blue-700 transition duration-200 font-semibold disabled:opacity-50 disabled:cursor-not-allowed"
                >
                    {loading ? '⏳ Thinking...' : '🚀 Ask Question'}
                </button>
            </div>

            {/* Error */}
            {error && (
                <div className="bg-red-50 text-red-600 rounded-xl p-4 mb-6">
                    ❌ {error}
                </div>
            )}

            {/* Answer */}
            {answer && (
                <div className="bg-green-50 rounded-xl shadow-lg p-6 mb-8 border border-green-200">
                    <h2 className="text-lg font-bold text-green-800 mb-3">
                        🤖 Answer:
                    </h2>
                    <p className="text-gray-700 leading-relaxed whitespace-pre-wrap">
                        {answer}
                    </p>
                </div>
            )}

            {/* Chat History */}
            {history.length > 0 && (
                <div>
                    <h2 className="text-2xl font-bold text-gray-800 mb-4">
                        📜 Chat History
                    </h2>
                    <div className="space-y-4">
                        {history.map((item, index) => (
                            <div
                                key={index}
                                className="bg-white rounded-xl shadow-md p-5 border border-gray-100"
                            >
                                <div className="font-semibold text-blue-700 mb-2">
                                    ❓ {item.question}
                                </div>
                                <div className="text-gray-600 text-sm leading-relaxed">
                                    🤖 {item.answer}
                                </div>
                                <div className="text-gray-400 text-xs mt-2">
                                    {new Date(item.asked_at).toLocaleString()}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}

export default QandA;