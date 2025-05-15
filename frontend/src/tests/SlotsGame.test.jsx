import React from 'react';
import { render, screen, fireEvent, waitFor, act } from '@testing-library/react';
import SlotsGame from '../components/games/SlotsGame.jsx';
import { vi, describe, expect, it } from 'vitest';

vi.mock('framer-motion', () => ({
    motion: {
        div: ({ children }) => <div>{children}</div>
    }
}));
vi.mock('react-toastify', () => ({
    toast: { error: vi.fn(), success: vi.fn() },
    ToastContainer: () => <div data-testid="toast-container" />
}));
import { toast } from 'react-toastify';

vi.mock('../context/AuthContext', () => ({
    useAuth: vi.fn()
}));
import { useAuth } from '../context/AuthContext';

const navigateMock = vi.fn();
vi.mock('react-router-dom', () => {
    const actual = require('react-router-dom');
    return {
        ...actual,
        useNavigate: () => navigateMock
    };
});

vi.mock('../components/games/GameApi', () => ({
    fetchBalance: vi.fn((setBalance, user) => {
        setBalance(77); // Set balance directly
        return Promise.resolve();
    }),
}));
import { fetchBalance } from '../components/games/GameApi';

beforeAll(() => {
    vi.useRealTimers();
});

describe('SlotsGame component', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        useAuth.mockReturnValue({ isAuthenticated: true, loading: false, user: {balance: 77} });
    });

    afterEach(() => {
        vi.clearAllTimers();
        vi.useRealTimers();
    });

    it('fetches initial balance on mount', async () => {
        fetchBalance.mockImplementation((setBalance) => {
            setBalance(77);
            return Promise.resolve();
        });
        render(<SlotsGame />);
        expect(await screen.findByText(/Balance: \$?77/)).toBeInTheDocument();
        expect(fetchBalance).toHaveBeenCalled();
    });

    it('shows error toast when spinning with insufficient balance', async () => {
        fetchBalance.mockImplementation((setBalance) => {
            setBalance(5);
            return Promise.resolve();
        });
        render(<SlotsGame />);
        await screen.findByText(/Balance: \$5/);
        fireEvent.click(screen.getByRole('button', { name: /spin/i }));
        expect(toast.error).toHaveBeenCalledWith('Insufficient balance for this bet.');
    });

    it('performs a successful spin', async () => {
        vi.useRealTimers();   // ← switch to real timers
        fetchBalance.mockImplementation((set) => { set(100); return Promise.resolve(); });

        global.fetch = vi.fn().mockResolvedValue({
            ok: true,
            json: async () => ({
                result: [[0, 1, 2], [1, 2, 0], [2, 0, 1], [0, 0, 0], [1, 1, 1]],
                payout: 50,
                current_balance: 150,
                win_data: { 1: ['star', [0, 1, 2]] }
            })
        });

        render(<SlotsGame />);
        await waitFor(() => expect(screen.getByText(/Balance: \$100/)).toBeInTheDocument());

        fireEvent.click(screen.getByRole('button', { name: /spin/i }));

        await waitFor(() => {
            expect(screen.getByText(/Balance: \$150/)).toBeInTheDocument();
            expect(screen.getByText(/You won \$50!/i)).toBeInTheDocument();
        }, { timeout: 3000 });

        await waitFor(() => {
            expect(screen.getByText(/Balance: \$150/)).toBeInTheDocument();
            expect(screen.getByText(/You won \$50!/i)).toBeInTheDocument();
        });
    });
});