import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import DiceGame from '../components/games/DiceGame.jsx';
import { vi, expect, it, beforeEach, describe } from 'vitest';

vi.mock('framer-motion', () => ({
    motion: { div: ({ children }) => <div>{children}</div> }
}));

vi.mock('react-toastify', () => ({
    toast: { error: vi.fn() },
    ToastContainer: () => <div data-testid="toast-container" />
}));

import { toast } from 'react-toastify';

vi.mock('../context/AuthContext', () => ({
    useAuth: vi.fn()
}));
import { useAuth } from '../context/AuthContext';

vi.mock('react-router-dom', async () => {
    const actual = await vi.importActual('react-router-dom');
    return {
        ...actual,
        useNavigate: () => vi.fn()
    };
});
import { useNavigate } from 'react-router-dom';

vi.mock('../components/games/GameApi.jsx', () => ({
    fetchBalance: vi.fn()
}));
import { fetchBalance } from '../components/games/GameApi.jsx';

describe('DiceGame Component', () => {
    let navigateMock;

    beforeEach(() => {
        vi.clearAllMocks();

        useAuth.mockReturnValue({ isAuthenticated: true, loading: false, user: {} });

        navigateMock = useNavigate();
    });

    it('fetches initial balance on mount when authenticated', async () => {
        fetchBalance.mockImplementationOnce((setBalance) => {
            setBalance(42);
            return Promise.resolve();
        });

        render(<DiceGame />);

        expect(await screen.findByText(/Balance: \$42/)).toBeInTheDocument();
        expect(fetchBalance).toHaveBeenCalled();
    });

    it('performs a successful roll', async () => {
        fetchBalance.mockImplementation((setBalance) => {
            setBalance(100);
            return Promise.resolve();
        });

        global.fetch = vi.fn().mockResolvedValue({
            ok: true,
            json: async () => ({
                roll1: 3,
                roll2: 5,
                payout: 20,
                new_balance: 120
            })
        });

        render(<DiceGame />);

        await screen.findByText(/Balance: \$100/);
        fireEvent.click(screen.getByRole('button', { name: /roll dice/i }));

        expect(await screen.findByText(/Balance: \$120/)).toBeInTheDocument();

        expect(
            screen.getByText(/You won \$20!/i)
        ).toBeInTheDocument();

    });

    it('shows error toast when insufficient balance on roll', async () => {
        fetchBalance.mockImplementation((setBalance) => {
            setBalance(10);
            return Promise.resolve();
        });

        global.fetch = vi.fn().mockResolvedValue({
            ok: false,
            json: async () => ({ error: 'Not enough coins!' })
        });

        render(<DiceGame />);

        await screen.findByText(/Balance: \$10/);

        fireEvent.click(screen.getByRole('button', { name: /roll dice/i }));

        await waitFor(() => {
            expect(toast.error).toHaveBeenCalledWith(
                'Insufficient balance for this bet.'
            );
        });
    });
});
