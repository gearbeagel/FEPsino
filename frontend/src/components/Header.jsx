import React, {useEffect, useState} from 'react';
import {Link} from 'react-router-dom';
import {HomeIcon, InfoIcon, User} from 'lucide-react';
import axios from 'axios';
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
        return null; // or a loading spinner
    }

    return (
        <header className="bg-gray-900 p-4">
            <div className="container mx-auto flex items-center justify-between">
                <h1 className="text-2xl font-bold text-yellow-400">FEPSino</h1>
                <nav className="hidden md:block">
                    <ul className="flex gap-4 items-center justify-center">
                        <li>
                            <Link to="/" className="flex flex-col items-center space-y-1 hover:text-yellow-400">
                                <HomeIcon className="h-6 w-6"/>
                                <span>Home</span>
                            </Link>
                        </li>
                        <li>
                            <Link to="/about" className="flex flex-col items-center space-y-1 hover:text-yellow-400">
                                <InfoIcon className="h-6 w-6"/>
                                <span>About</span>
                            </Link>
                        </li>
                    </ul>
                </nav>
                <div className="flex items-center space-x-4">
                    {user ? (
                        <>
                            <User className="h-6 w-6 text-yellow-400"/>
                            <div className="text-yellow-400">{user.email}</div>
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