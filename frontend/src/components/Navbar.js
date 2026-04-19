import React from 'react';
import { Link } from 'react-router-dom';

function Navbar() {
    return (
        <nav className="bg-blue-800 text-white px-6 py-4 shadow-lg">
            <div className="max-w-7xl mx-auto flex justify-between items-center">
                {/* Logo */}
                <Link to="/" className="text-2xl font-bold tracking-wide">
                    📚 BookIQ
                </Link>

                {/* Navigation Links */}
                <div className="flex gap-6">
                    <Link
                        to="/"
                        className="hover:text-blue-300 transition duration-200 font-medium"
                    >
                        Dashboard
                    </Link>
                    <Link
                        to="/qa"
                        className="hover:text-blue-300 transition duration-200 font-medium"
                    >
                        Q&A
                    </Link>
                </div>
            </div>
        </nav>
    );
}

export default Navbar;