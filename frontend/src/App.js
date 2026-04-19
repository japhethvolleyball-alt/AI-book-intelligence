import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import BookDetail from './pages/BookDetail';
import QandA from './pages/QandA';

function App() {
    return (
        <Router>
            <div className="min-h-screen bg-gray-100">
                <Navbar />
                <div className="max-w-7xl mx-auto px-4 py-8">
                    <Routes>
                        <Route path="/" element={<Dashboard />} />
                        <Route path="/book/:id" element={<BookDetail />} />
                        <Route path="/qa" element={<QandA />} />
                    </Routes>
                </div>
            </div>
        </Router>
    );
}

export default App;