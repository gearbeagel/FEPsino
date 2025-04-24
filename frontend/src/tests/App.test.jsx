// src/tests/App.test.jsx
import React from 'react';
import { render, screen } from '@testing-library/react';
import App from '../App';
import { describe, it, expect } from 'vitest';

describe('App routing and layout', () => {
    it('always renders the header (site title)', () => {
        render(<App />);
        expect(screen.getByText(/FEPsino/i)).toBeInTheDocument();
    });

    it('shows Home on the "/" route', () => {
        window.history.pushState({}, 'Home page', '/');
        render(<App />);
        expect(screen.getByText(/welcome to fepsino/i)).toBeInTheDocument();
    });

    it('shows About on the "/about" route', () => {
        window.history.pushState({}, 'About page', '/about');
        render(<App />);
        expect(screen.getByText(/about/i)).toBeInTheDocument();
    });

    it('shows DiceGame on the "/dice" route', () => {
        window.history.pushState({}, 'Dice page', '/dice');
        render(<App />);
        expect(screen.getByText(/balance: \$/i)).toBeInTheDocument();
        expect(screen.getByText(/last win: \$/i)).toBeInTheDocument();
    });

    it('shows BlackjackGame on the "/blackjack" route', () => {
        window.history.pushState({}, 'Blackjack page', '/blackjack');
        render(<App />);
        expect(screen.getByRole('button', { name: /start game/i })).toBeInTheDocument();
    });
});
