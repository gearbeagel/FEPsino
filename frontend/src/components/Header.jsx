import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { InfoIcon, User, LogOut, Menu, X } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export default function Header() {
    const { isAuthenticated, user, loading, logout } = useAuth();
    const [isMenuOpen, setIsMenuOpen] = useState(false);

    if (loading) return null;

    return (
        <header className="bg-gray-900 p-4">
            <div className="container mx-auto">
                <div className="hidden md:grid grid-cols-3 items-center">
                    <div className="justify-self-start">
                        <Link to="/">
                            <h1 className="text-2xl font-bold text-yellow-400">FEPSino</h1>
                        </Link>
                    </div>
                    <nav className="justify-self-center">
                        <Link to="/about" className="flex flex-col items-center space-y-1 hover:text-yellow-400">
                            <InfoIcon className="h-6 w-6" />
                            <span>About</span>
                        </Link>
                    </nav>
                    <div className="flex items-center space-x-4 justify-self-end">
                        {isAuthenticated ? (
                            <div className="flex items-center space-x-4">
                                <Link to="/profile" className="flex items-center space-x-2 hover:text-yellow-400">
                                    <User className="h-6 w-6 text-yellow-400" />
                                </Link>
                            </div>
                        ) : (
                            <Link to="/signup">
                                <button className="flex items-center space-x-2 text-yellow-400 px-4 py-2 rounded hover:text-yellow-500 transition-colors">
                                    <User className="h-6 w-6 text-yellow-400" />
                                    <span>Login / Sign Up</span>
                                </button>
                            </Link>
                        )}
                    </div>
                </div>

                <div className="md:hidden sticky top-0 z-10 flex justify-between items-center">
                    <Link to="/">
                        <h1 className="text-xl font-bold text-yellow-400">FEPSino</h1>
                    </Link>
                    <button 
                        onClick={() => setIsMenuOpen(!isMenuOpen)}
                        className="text-white p-2"
                    >
                        {isMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
                    </button>
                </div>

                {/* Mobile Menu */}
                {isMenuOpen && (
                    <div className="md:hidden absolute top-16 left-0 right-0 bg-gray-900 border-t border-gray-800 p-4">
                        <nav className="flex flex-col space-y-4">
                            <Link 
                                to="/about" 
                                className="flex items-center space-x-2 text-white hover:text-yellow-400"
                                onClick={() => setIsMenuOpen(false)}
                            >
                                <InfoIcon className="h-6 w-6" />
                                <span>About</span>
                            </Link>
                            {isAuthenticated ? (
                                <>
                                    <Link 
                                        to="/profile" 
                                        className="flex items-center space-x-2 text-white hover:text-yellow-400"
                                        onClick={() => setIsMenuOpen(false)}
                                    >
                                        <User className="h-6 w-6" />
                                        <span>Profile</span>
                                    </Link>
                                </>
                            ) : (
                                <Link 
                                    to="/signup" 
                                    className="flex items-center space-x-2 text-white hover:text-yellow-400"
                                    onClick={() => setIsMenuOpen(false)}
                                >
                                    <User className="h-6 w-6" />
                                    <span>Login / Sign Up</span>
                                </Link>
                            )}
                        </nav>
                    </div>
                )}
            </div>
        </header>
    );
}
