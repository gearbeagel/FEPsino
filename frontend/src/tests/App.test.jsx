import React from 'react';
import { render, screen } from '@testing-library/react';
import App from '../App.jsx';
import { vi, beforeEach, it, describe, expect } from 'vitest';

vi.mock('framer-motion', () => ({
    motion: { div: ({ children }) => <div>{children}</div> },
    AnimatePresence: ({ children }) => <div>{children}</div>
}));

vi.mock('../context/AuthContext.jsx', () => ({
    AuthProvider: ({ children }) => <>{children}</>,
    useAuth: vi.fn()
}));
import { useAuth } from '../context/AuthContext.jsx';

describe('App routing (public pages)', () => {
    beforeEach(() => {
        useAuth.mockReturnValue({ isAuthenticated: false, loading: false });
    });

    it('renders Home at root path', () => {
        window.history.pushState({}, 'Home page', '/');
        render(<App />);
        expect(
            screen.getByText(/Experience the thrill of our exclusive games\./i)
        ).toBeInTheDocument();
    });

    it('renders About at /about', () => {
        window.history.pushState({}, 'About page', '/about');
        render(<App />);
        expect(screen.getByText(/about fepsino/i)).toBeInTheDocument();
    });

    it('renders SignUpIn at /signup', () => {
        window.history.pushState({}, 'SignUp page', '/signup');
        render(<App />);
        expect(screen.getByTestId("auth-submit")).toBeInTheDocument();
    });
});

describe('App routing (auth-protected pages)', () => {
    it('redirects unauthenticated user from /profile to /signup', () => {
        useAuth.mockReturnValue({ isAuthenticated: false, loading: false });
        window.history.pushState({}, 'Profile page', '/profile');
        render(<App />);
        expect(screen.getByRole('button', { name: /sign up/i })).toBeInTheDocument();
    });

});
