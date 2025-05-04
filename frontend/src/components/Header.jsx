import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { InfoIcon, User } from 'lucide-react';
import fetchUser from "./user/UserApi.jsx";

export default function Header() {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const getUser = async () => {
            try {
                const res = await fetchUser();
                setUser(res);
            } catch (err) {
                console.error('Error fetching user:', err);
            } finally {
                setLoading(false);
            }
        };
        getUser();
    }, []);

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
                    {user ? (
                        <Link to="/profile" className="flex items-center space-x-2 hover:text-yellow-400">
                            <User className="h-6 w-6 text-yellow-400" />
                        </Link>
                    ) : (
                        <Link to="/signup">
                            <button className="flex items-center space-x-2 border border-yellow-400 bg-yellow-400 text-black px-4 py-2 rounded hover:bg-yellow-500 transition-colors">
                                <User className="h-6 w-6 text-black" />
                                <span>Login / Sign Up</span>
                            </button>
                        </Link>
                    )}
                </div>
            </div>
        </header>
    );
}
