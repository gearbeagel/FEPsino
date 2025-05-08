import React from 'react';
import { Link } from 'react-router-dom';
import { InfoIcon, User, LogOut } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export default function Header() {
    const { isAuthenticated, user, loading, logout } = useAuth();

    if (loading) return null;

    return (
        <header className="bg-gray-900 p-4">
            <div className="container mx-auto grid grid-cols-3 items-center">
                <div className="justify-self-start">
                    <Link to="/">
                        <h1 className="text-2xl font-bold text-yellow-400">FEPSino</h1>
                    </Link>
                </div>
                <nav className="hidden md:block justify-self-center">
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
        </header>
    );
}
