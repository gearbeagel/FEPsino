import React, {useEffect, useState} from 'react';
import {Link} from 'react-router-dom';
import {HomeIcon, InfoIcon, User} from 'lucide-react';
import fetchUser from "./user/UserApi.jsx";

export default function Header() {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const getUser = async () => {
            try {
                const res = await fetchUser()
                setUser(res);
            } catch (err) {
                console.error('Error fetching user:', err);
            } finally {
                setLoading(false);
            }
        };

        getUser();
    }, []);

    if (loading) {
        return null;
    }

    return (
        <header className="bg-gray-900 p-4">
            <div className="container mx-auto flex items-center justify-between">
                <Link to="/"><h1 className="text-2xl font-bold text-yellow-400">FEPSino</h1></Link>
                <nav className="hidden md:block ml-40">
                            <Link to="/about" className="flex flex-col items-center space-y-1 hover:text-yellow-400">
                                <InfoIcon className="h-6 w-6"/>
                                <span>About</span>
                            </Link>
                </nav>
                <div className="flex items-center space-x-4">
                    {user ? (
                        <>
                            <Link to="/profile" className="flex row items-center space-x-2">
                                <User className="h-6 w-6 text-yellow-400"/>
                                <div className="text-yellow-400">{user.email}</div>
                            </Link>
                        </>
                    ) : (
                        <Link to="/signup">
                            <button
                                className="flex row border border-yellow-400 bg-yellow-400 text-black px-4 py-2 rounded hover:bg-yellow-500 transition-colors">
                                <User className="h-6 w-6 text-black"/> Login / Sign Up
                            </button>
                        </Link>
                    )}
                </div>
            </div>
        </header>
    );
}