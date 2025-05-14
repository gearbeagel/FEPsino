import React, { useState, useEffect } from "react";
import {Club, Play, Heart, Diamond, Spade, InfoIcon} from "lucide-react";
import { toast, ToastContainer } from "react-toastify";
import axios from "axios";

const suits = {
    '♥': <Heart className="text-red-500" />,
    '♦': <Diamond className="text-red-500" />,
    '♣': <Club className="text-black" />,
    '♠': <Spade className="text-black" />,
};

function getResultColor(result) {
    if (!result) return "text-gray-500";
    if (result.includes("won") || result.includes("You win!") || result.includes("Blackjack!")) {
        return "text-green-400";
    } else if (result.includes("lose") || result.includes("Dealer wins!")) {
        return "text-red-400";
    } else {
        return "text-yellow-400";
    }
}

export default function BlackJackGame() {
    const [balance, setBalance] = useState(0);
    const [bet, setBet] = useState(10);
    const [playerHand, setPlayerHand] = useState([]);
    const [dealerHand, setDealerHand] = useState([]);
    const [gameResult, setGameResult] = useState(null);
    
    const [isLoading, setIsLoading] = useState(false);
    const [canPlay, setCanPlay] = useState(true);
    const [isGameActive, setIsGameActive] = useState(false);

    useEffect(() => {
        fetchBalance();
        fetchGameState();
    }, []);

    const fetchBalance = async () => {
        try {
            const response = await axios.get(
                `${import.meta.env.VITE_API_URL}/blackjack/state/`,
                {
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${localStorage.getItem("access_token")}`,
                    },
                    withCredentials: true
                }
            );
            if (response.data.balance !== undefined) {
                setBalance(response.data.balance);
            }
        } catch (error) {
            console.error('Failed to fetch balance:', error);
            toast.error('Failed to fetch balance');
        }
    };

    const fetchGameState = async () => {
        try {
            const response = await axios.get(
                `${import.meta.env.VITE_API_URL}/blackjack/state/`,
                {
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${localStorage.getItem("access_token")}`,
                    },
                    withCredentials: true
                }
            );
            
            const { game_state, balance: newBalance } = response.data;
            
            setBalance(newBalance);
            
            if (game_state && !game_state.game_over && (game_state.player_hand?.length > 0 || game_state.dealer_hand?.length > 0)) {
                setPlayerHand(game_state.player_hand || []);
                setDealerHand(game_state.dealer_hand || []);
                setIsGameActive(true);
                setCanPlay(false);
            } else {
                resetGame();
            }
        } catch (error) {
            console.error('Failed to fetch game state:', error);
            toast.error('Failed to fetch game state');
            resetGame();
        }
    };

    const resetGame = () => {
        setPlayerHand([]);
        setDealerHand([]);
        setGameResult(null);
        setCanPlay(true);
        setIsGameActive(false);
        setBet(10);
    };

    const startGame = async () => {
        if (!canPlay || isLoading) return;

        setIsLoading(true);
        const currentBet = bet;
        resetGame();
        setBet(currentBet);

        try {
            const betResponse = await axios.post(
                `${import.meta.env.VITE_API_URL}/blackjack/bet/`,
                { amount: bet.toString() },
                {
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${localStorage.getItem("access_token")}`,
                    },
                    withCredentials: true
                }
            );

            if (betResponse.data.message !== 'Bet placed and game started') {
                throw new Error(betResponse.data.message || 'Failed to start game');
            }

            await new Promise(resolve => setTimeout(resolve, 500));

            const stateResponse = await axios.get(
                `${import.meta.env.VITE_API_URL}/blackjack/state/`,
                {
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${localStorage.getItem("access_token")}`,
                    },
                    withCredentials: true
                }
            );

            const { game_state, balance: newBalance } = stateResponse.data;

            if (!game_state) {
                throw new Error('No game state received');
            }

            setPlayerHand(game_state.player_hand || []);
            setDealerHand(game_state.dealer_hand || []);
            setBalance(newBalance);
            setIsGameActive(true);
            setCanPlay(false);

            if (game_state.dealer_hand?.length > 0 && (!game_state.player_hand || game_state.player_hand.length === 0)) {
                await handleAction('hit');
            }

        } catch (error) {
            console.error('Game start error:', error);
            toast.error(error.message || 'Failed to start game');
            resetGame();
        } finally {
            setIsLoading(false);
        }
    };

    const handleAction = async (action) => {
        if (!isGameActive || isLoading) return;

        setIsLoading(true);

        try {
            const response = await axios.post(
                `${import.meta.env.VITE_API_URL}/blackjack/${action}/`,
                {},
                {
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${localStorage.getItem("access_token")}`,
                    },
                    withCredentials: true
                }
            );

            const { game_state, balance: newBalance, message } = response.data;

            if (!game_state) {
                throw new Error('No game state received');
            }

            setPlayerHand(game_state.player_hand || []);
            setDealerHand(game_state.dealer_hand || []);
            setBalance(newBalance);

            if (game_state.game_over || message?.includes('win') || message?.includes('lose') || message?.includes('tie')) {
                setGameResult(message);
                setIsGameActive(false);
                setCanPlay(true);
            }

        } catch (error) {
            console.error(`${action} action error:`, error);
            toast.error(`Failed to ${action}`);
        } finally {
            setIsLoading(false);
        }
    };

    const handleBetChange = (e) => {
        setBet(Number(e.target.value));
    };

    return (
        <div className="flex-grow flex flex-col items-center p-6">
            <div className="container max-w-4xl bg-slate-900 border border-yellow-400 rounded-lg p-6 shadow-xl w-full">
                <div className="flex justify-between items-center mb-4">
                    <div className="flex items-center">
                        <Club className="h-6 w-6 text-yellow-400 mr-2" />
                        <span className="text-xl">Balance: ${balance}</span>
                    </div>
                    <span className="text-xl text-yellow-400 group relative">
                        <InfoIcon className="h-6 w-6 mr-2" />
                        <span className="absolute bottom-full right-1/2 transform translate-x-6 mb-2 w-max px-2 py-1 text-sm text-yellow-400 bg-slate-950 rounded opacity-0 group-hover:opacity-100 transition-opacity">
                            Place your bet and start the game. You can hit or stand during your turn, and the dealer will play after you.
                            <br/>
                            The goal is to get as close to 21 as possible without going over. If you go over, you lose.
                            <br/>
                            If the dealer goes over, you win! If you both have the same score, it's a tie.
                        </span>
                    </span>
                </div>

                <div className="flex gap-4 items-center mt-6">
                    <div className="flex-1">
                        <label className="block text-sm mb-1">Bet Amount</label>
                        <select
                            value={bet}
                            onChange={handleBetChange}
                            disabled={!canPlay || isLoading}
                            className={`w-full bg-gray-700 rounded p-2 text-white ${(!canPlay || isLoading) ? 'opacity-50 cursor-not-allowed' : ''}`}
                        >
                            <option value="10">$10</option>
                            <option value="20">$20</option>
                            <option value="50">$50</option>
                            <option value="100">$100</option>
                        </select>
                    </div>
                </div>

                <button
                    onClick={startGame}
                    disabled={isLoading || !canPlay}
                    className={`w-full px-4 py-2 ${isLoading || !canPlay ? 'bg-gray-400' : 'bg-yellow-400 hover:bg-yellow-500'} rounded-lg text-black flex items-center justify-center text-xl font-bold transition-colors mt-5`}
                >
                    <Play className="h-6 w-6 mr-2" />
                    {isLoading ? 'Loading...' : !canPlay ? 'Game in Progress' : 'Start Game'}
                </button>
            </div>

            {(isGameActive || gameResult) && (
                <div className="container max-w-4xl bg-slate-900 border border-yellow-400 rounded-lg p-8 shadow-xl w-full mt-8">
                    <div className="flex gap-4">
                        <div className="flex-1">
                            <h2 className="text-2xl text-start mb-4">Dealer's Hand</h2>
                            <div className="flex justify-center mb-4">
                                <div className="grid grid-cols-5 md:gap-4 gap-20">
                                    {(dealerHand.length === 1)
                                        ? (
                                            <>
                                                <div className="w-16 h-24 p-4 bg-white rounded-lg shadow text-black flex flex-col items-center">
                                                    <span className="text-lg font-bold">{dealerHand[0].rank}</span>
                                                    {suits[dealerHand[0].suit]}
                                                </div>
                                                <div className="w-16 h-24 p-4 bg-white rounded-lg shadow flex flex-col items-center justify-center">
                                                </div>
                                            </>
                                        )
                                        : dealerHand.map((card, index) => (
                                            <div key={index} className="w-16 h-24 p-4 bg-white rounded-lg shadow text-black flex flex-col items-center">
                                                <span className="text-lg font-bold">{card.rank}</span>
                                                {suits[card.suit]}
                                            </div>
                                        ))
                                    }
                                </div>
                            </div>
                            <h2 className="text-2xl text-start mb-4">Your Hand</h2>
                            <div className="flex justify-center mb-8">
                                <div className="grid grid-cols-5 md:gap-4 gap-20">
                                    {playerHand.map((card, index) => (
                                        <div key={index} className="w-16 h-24 p-4 bg-white rounded-lg shadow text-black flex flex-col items-center">
                                            <span className="text-lg font-bold">{card.rank}</span>
                                            {suits[card.suit]}
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </div>
                        <div className="flex-1 flex flex-col justify-center gap-4 mt-6">
                            {isGameActive && (
                                <>
                                    <button
                                        onClick={() => handleAction('hit')}
                                        disabled={isLoading}
                                        className={`px-6 py-3 ${isLoading ? 'bg-gray-400' : 'bg-yellow-400'} rounded-lg text-black text-lg`}
                                    >
                                        {isLoading ? 'Loading...' : 'Hit'}
                                    </button>
                                    <button 
                                        onClick={() => handleAction('stay')}
                                        disabled={isLoading}
                                        className={`px-6 py-3 ${isLoading ? 'bg-gray-400' : 'bg-yellow-400'} rounded-lg text-black text-lg`}
                                    >
                                        {isLoading ? 'Loading...' : 'Stand'}
                                    </button>
                                </>
                            )}
                            {gameResult && (
                                <div className="mt-4 p-4">
                                    <h2 className={`text-2xl text-center ${getResultColor(gameResult)}`}>{gameResult}</h2>
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            )}

            <ToastContainer
                position="top-right"
                autoClose={3000}
                hideProgressBar={false}
                newestOnTop
                closeOnClick
                pauseOnHover
                theme="dark"
            />
        </div>
    );
}