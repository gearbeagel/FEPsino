import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import DiceGame from '../components/games/DiceGame.jsx';
import { describe, it, vi, beforeEach, afterEach, expect } from 'vitest';

describe('DiceGame Component', () => {
    beforeEach(() => {
        vi.spyOn(Storage.prototype, 'getItem').mockReturnValue('mock-token');
    });

    afterEach(() => {
        vi.clearAllMocks();
    });

    it('renders initial balance, last win, and Roll Dice button', () => {
        render(<DiceGame />);
        expect(screen.getByText(/balance: \$1000/i)).toBeInTheDocument();
        expect(screen.getByText(/last win: \$0/i)).toBeInTheDocument();
        expect(screen.getByRole('button', { name: /roll dice/i })).toBeInTheDocument();
    });

    it('updates the “Select Number” options when dice types change', () => {
        render(<DiceGame />);
        const [selectNumber] = screen.getAllByRole('combobox');
        expect(selectNumber.children).toHaveLength(11);
        const allButtons = screen.getAllByRole('button');
        fireEvent.click(allButtons[1]);
        expect(selectNumber.children).toHaveLength(13);
        fireEvent.click(allButtons[5]);
        expect(selectNumber.children).toHaveLength(19);
    });

    it('shows a win message and updates balance when fetch returns a payout', async () => {
        const mockResult = { roll1: 4, roll2: 2, payout: 20, new_balance: 1020 };
        global.fetch = vi.fn(() =>
            Promise.resolve({
                ok: true,
                json: () => Promise.resolve(mockResult),
            })
        );

        render(<DiceGame />);
        fireEvent.click(screen.getByRole('button', { name: /roll dice/i }));

        await waitFor(() => {
            expect(screen.getByText(/you won \$20!/i)).toBeInTheDocument();
            expect(screen.getByText(/balance: \$1020/i)).toBeInTheDocument();
        });
    });

    it('shows a loss message when payout is zero', async () => {
        const mockResult = { roll1: 1, roll2: 3, payout: 0, new_balance: 990 };
        global.fetch = vi.fn(() =>
            Promise.resolve({
                ok: true,
                json: () => Promise.resolve(mockResult),
            })
        );

        render(<DiceGame />);
        fireEvent.click(screen.getByRole('button', { name: /roll dice/i }));

        await waitFor(() => {
            expect(screen.getByText(/you lost \$10!/i)).toBeInTheDocument();
            expect(screen.getByText(/balance: \$990/i)).toBeInTheDocument();
        });
    });
});
