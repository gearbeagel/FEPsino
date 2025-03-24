import React from 'react';
import { Link } from 'react-router-dom';
import { HomeIcon, User, InfoIcon } from 'lucide-react';

export default function Header() {
  return (
    <header className="bg-gray-900 p-4">
      <div className="container mx-auto flex items-center justify-between">
        <h1 className="text-2xl font-bold text-yellow-400">FEPSino</h1>
        <nav className="hidden md:block">
          <ul className="flex space-x-4">
            <li>
              <Link to="/" className="flex flex-col items-center space-y-1 hover:text-yellow-400">
                <HomeIcon className="h-6 w-6" />
                <span>Home</span>
              </Link>
            </li>
            <li>
              <Link to="/profile" className="flex flex-col items-center space-y-1 hover:text-yellow-400">
                <User className="h-6 w-6" />
                <span>Profile</span>
              </Link>
            </li>
            <li>
              <Link to="/about" className="flex flex-col items-center space-y-1 hover:text-yellow-400">
                <InfoIcon className="h-6 w-6" />
                <span>About</span>
              </Link>
            </li>
          </ul>
        </nav>
        <Link to="/signup"><button className="border border-yellow-400 bg-yellow-400 text-black px-4 py-2 rounded hover:bg-yellow-500 transition-colors">
          Login / Sign Up
        </button></Link>
      </div>
    </header>
  );
}