import React from 'react';
import { render, screen, fireEvent, waitFor, act } from '@testing-library/react';
import BlackJackGame from '../components/games/BlackJackGame';
import { toast } from 'react-toastify';
import axios from 'axios';
import { vi, expect, describe, it, beforeEach, afterEach } from 'vitest';

vi.mock('react-toastify', () => ({
    toast: { error: vi.fn(), success: vi.fn() },
    ToastContainer: () => <div />
}));

vi.mock('axios');

beforeEach(() => {
    vi.clearAllMocks();
});

describe('BlackJackGame component', () => {
    it('fetches initial balance and game state on mount', async () => {
        const stateResp = {
            data: {
                balance: 200,
                game_state: null
            }
        };
        axios.get.mockResolvedValueOnce(stateResp);
        axios.get.mockResolvedValueOnce(stateResp);

        render(<BlackJackGame />);

        expect(axios.get).toHaveBeenCalledTimes(2);
        await waitFor(() => {
            expect(screen.getByText(/Balance: \$200/)).toBeInTheDocument();
            expect(screen.getByRole('button', { name: /Start Game/i })).toBeEnabled();
        });
    });

    it('starts a new game when Start Game is clicked', async () => {
        axios.get.mockResolvedValue({ data: { balance: 100, game_state: null } });
        render(<BlackJackGame />);
        await waitFor(() => screen.getByText(/Balance: \$100/));

        axios.post.mockResolvedValueOnce({ data: { message: 'Bet placed and game started' } });
        const gameState = {
            data: {
                balance: 90,
                game_state: {
                    player_hand: [ { rank: '10', suit: '♥' } ],
                    dealer_hand: [ { rank: 'K', suit: '♠' } ],
                    game_over: false
                }
            }
        };
        axios.get.mockResolvedValueOnce(gameState);

        const startButton = screen.getByRole('button', { name: /Start Game/i });
        fireEvent.click(startButton);

        expect(axios.post).toHaveBeenCalledWith(
            expect.stringContaining('/blackjack/bet/'),
            { amount: '10' },
            expect.any(Object)
        );
        expect(axios.get).toHaveBeenCalledWith(
            expect.stringContaining('/blackjack/state/'),
            expect.any(Object)
        );

        await waitFor(() => {
            expect(screen.getByText(/Balance: \$90/)).toBeInTheDocument();
            expect(screen.getByText('10')).toBeInTheDocument();
            expect(screen.getByText('K')).toBeInTheDocument();
            expect(screen.getByRole('button', { name: /Hit/i })).toBeEnabled();
            expect(screen.getByRole('button', { name: /Stand/i })).toBeEnabled();
        });

        vi.useRealTimers();
    });


    it('handles hit action and ends game on win', async () => {
        axios.get.mockResolvedValueOnce({ data: { balance: 90, game_state: null } });
        axios.get.mockResolvedValueOnce({ data: { balance: 90, game_state: null } });
        render(<BlackJackGame />);
        await waitFor(() => expect(screen.getByText(/Balance: \$90/)).toBeInTheDocument());

        axios.post.mockResolvedValueOnce({ data: { message: 'Bet placed and game started' } });
        axios.get.mockResolvedValueOnce({
            data: {
                balance: 90,
                game_state: {
                    player_hand: [{ rank: '10', suit: '♥' }],
                    dealer_hand: [{ rank: 'K', suit: '♠' }],
                    game_over: false
                }
            }
        });
        fireEvent.click(screen.getByRole('button', { name: /Start Game/i }));
        await waitFor(() => screen.getByRole('button', { name: /Hit/i }), { timeout: 1500 });

        axios.post.mockResolvedValueOnce({
            data: {
                balance: 150,
                game_state: { player_hand: [], dealer_hand: [], game_over: true },
                message: 'You win!'
            }
        });

        fireEvent.click(screen.getByRole('button', { name: /Hit/i }));

        await waitFor(
            () => expect(screen.getByText(/Balance: \$150/)).toBeInTheDocument(),
            { timeout: 500 }
        );

        const result = screen.getByText("You win!");
        expect(result).toHaveClass('text-green-400');
        expect(screen.getByRole('button', { name: /Start Game/i })).toBeEnabled();
    });
});
