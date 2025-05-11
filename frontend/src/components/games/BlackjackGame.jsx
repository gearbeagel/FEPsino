import React, { useState, useEffect } from "react";
import { Club, Play, Heart, Diamond, Spade, InfoIcon } from "lucide-react";
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
    const [gameInitialized, setGameInitialized] = useState(false);
    const [gameActive, setGameActive] = useState(false);
    const [playerHand, setPlayerHand] = useState([]);
    const [dealerHand, setDealerHand] = useState([]);
    const [gameResult, setGameResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetchGameState();
    }, []);

    const handleApiError = (error, operation = "operation", customMessage = null) => {
        setLoading(false);
        const message = customMessage || error.response?.data?.message || `Failed to ${operation}`;
        setError(message);
        toast.error(message);
        console.error(`Error during ${operation}:`, error);
    };

    const fetchGameState = async () => {
        setLoading(true);
        setError(null);
        try {
            console.log('Fetching game state...');
            const response = await axios.get(
                `${import.meta.env.VITE_API_URL}/blackjack/state/`,
                {
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${localStorage.getItem("access_token")}`,
                    },
                    timeout: 10000,
                    withCredentials: true
                }
            );

            console.log('Game state response:', response.data);
            const data = response.data;

            if (data.game_state) {
                // Check for invalid game states
                const isInvalidState = (
                    // Dealer has cards but player doesn't
                    (data.game_state.dealer_hand?.length > 0 && (!data.game_state.player_hand || data.game_state.player_hand.length === 0)) ||
                    // Bet is 0 but game is not over
                    (data.bet === 0 && !data.game_state.game_over) ||
                    // Player has no cards but game is not over
                    (!data.game_state.player_hand?.length && !data.game_state.game_over)
                );

                if (isInvalidState) {
                    console.log('Detected invalid game state, resetting game');
                    setPlayerHand([]);
                    setDealerHand([]);
                    setGameInitialized(false);
                    setGameActive(false);
                    setGameResult(null);
                    // Don't reset the bet value here
                } else if (data.game_state.game_over) {
                    setPlayerHand([]);
                    setDealerHand([]);
                    setGameInitialized(false);
                    setGameActive(false);
                    setGameResult(null);
                } else {
                    setPlayerHand(data.game_state.player_hand || []);
                    setDealerHand(data.game_state.dealer_hand || []);
                    setGameInitialized(true);
                    if ((data.game_state.player_hand && data.game_state.player_hand.length > 0) ||
                        (data.game_state.dealer_hand && data.game_state.dealer_hand.length > 0)) {
                        setGameActive(true);
                    }
                    if (data.message) {
                        setGameResult(data.message);
                    }
                }

                // Only update balance and bet if they are valid
                if (typeof data.balance === 'number' && data.balance >= 0) {
                    setBalance(data.balance);
                }
                if (typeof data.bet === 'number' && data.bet > 0) {
                    setBet(data.bet);
                }
            }
            setLoading(false);
        } catch (error) {
            const message = error.response?.data?.message || "Failed to fetch game state";
            console.log(message);
            handleApiError(error, "fetch game state", message);
        }
    };

    const startGame = async () => {
        setLoading(true);
        setError(null);
        console.log('Starting new game with bet:', bet);

        try {
            // Reset game state before starting a new one
            setPlayerHand([]);
            setDealerHand([]);
            setGameResult(null);
            
            // Important: ensure the bet value is properly converted to string
            const betAmount = bet.toString();
            console.log('Making bet request with amount:', betAmount);
            
            const response = await axios.post(
                `${import.meta.env.VITE_API_URL}/blackjack/bet/`,
                { amount: betAmount },
                {
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${localStorage.getItem("access_token")}`,
                    },
                    timeout: 10000,
                    withCredentials: true
                }
            );
            console.log('Bet response:', response.data);

            // Process the response immediately
            if (response.data.game_state) {
                setPlayerHand(response.data.game_state.player_hand || []);
                setDealerHand(response.data.game_state.dealer_hand || []);
                setGameInitialized(true);
                setGameActive(true);
                
                if (response.data.message) {
                    setGameResult(response.data.message);
                }
                
                if (typeof response.data.balance === 'number' && response.data.balance >= 0) {
                    setBalance(response.data.balance);
                }
            } else {
                // Fallback to fetching game state if the response doesn't include it
                await fetchGameState();
            }
        } catch (error) {
            console.error('Error starting game:', error);
            handleApiError(error, "start game");
        } finally {
            setLoading(false);
        }
    };

    const handleAction = async (action) => {
        setLoading(true);
        setError(null);
        console.log(`Handling ${action} action...`);
        try {
            const response = await axios.post(
                `${import.meta.env.VITE_API_URL}/blackjack/${action}/`,
                {},
                {
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${localStorage.getItem("access_token")}`,
                    },
                    timeout: 10000,
                    withCredentials: true
                }
            );
            console.log(`${action} response:`, response.data);

            const data = response.data;

            if (data.game_state) {
                setPlayerHand(data.game_state.player_hand || []);
                setDealerHand(data.game_state.dealer_hand || []);
                
                if (typeof data.balance === 'number' && data.balance >= 0) {
                    setBalance(data.balance);
                }
                
                if (typeof data.bet === 'number') {
                    setBet(data.bet);
                }

                if (data.game_state.game_over) {
                    setGameInitialized(false);
                }
            }

            if (data.message) {
                setGameResult(data.message);
                if (data.game_state?.game_over) {
                    setGameInitialized(false);
                }
            }
        } catch (error) {
            handleApiError(error, action);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex-grow flex flex-col items-center p-4 sm:p-6">
            <div className="container max-w-4xl bg-slate-900 border border-yellow-400 rounded-lg p-6 shadow-xl w-full">
                <div className="flex justify-between items-center mb-4">
                    <div className="flex items-center">
                        <Club className="h-6 w-6 text-yellow-400 mr-2" />
                        <span className="text-xl">Balance: ${balance}</span>
                    </div>
                    <span className="text-xl text-yellow-400 group relative">
                        <InfoIcon className="h-6 w-6 mr-2" />
                        <span
                            className="absolute bottom-full right-1/2 transform translate-x-6 mb-2 w-max px-2 py-1 text-sm text-yellow-400 bg-slate-950 rounded opacity-0 group-hover:opacity-100 transition-opacity"
                        >
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
                            onChange={(e) => setBet(Number(e.target.value))}
                            disabled={gameInitialized || loading}
                            className={`w-full bg-gray-700 rounded p-2 text-white ${(gameInitialized || loading) ? 'opacity-50 cursor-not-allowed' : ''}`}
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
                    disabled={loading || gameInitialized}
                    className={`w-full px-4 py-2 ${loading || gameInitialized ? 'bg-gray-400' : 'bg-yellow-400 hover:bg-yellow-500'} rounded-lg text-black flex items-center justify-center text-xl font-bold transition-colors mt-5`}
                >
                    <Play className="h-6 w-6 mr-2" />
                    {loading ? 'Loading...' : gameInitialized ? 'Game in Progress' : 'Start Game'}
                </button>
            </div>

            {gameActive && (
                <div className="container max-w-4xl bg-slate-900 border border-yellow-400 rounded-lg p-8 shadow-xl w-full mt-8">
                    <div className="flex flex-col lg:flex-row gap-8">
                        <div className="flex-1">
                            <h2 className="text-2xl text-start mb-4">Dealer's Hand</h2>
                            <div className="flex mb-4">
                                <div className="grid grid-cols-5 md:gap-4 gap-16">
                                    {dealerHand.slice(0, 5).map((card, index) => (
                                        <div key={index} className="w-16 h-24 p-4 bg-white rounded-lg shadow text-black flex flex-col items-center">
                                            <span className="text-lg font-bold">{card.rank}</span>
                                            {suits[card.suit]}
                                        </div>
                                    ))}
                                    {dealerHand.length < 2 && (
                                        <div className="w-16 h-24 p-4 bg-white rounded-lg shadow text-black flex flex-col items-center">
                                        </div>
                                    )}
                                </div>
                            </div>
                            <h2 className="text-2xl text-start mb-4">Your Hand</h2>
                            <div className="flex mb-8">
                                <div className="grid grid-cols-5 md:gap-4 gap-16">
                                    {playerHand.slice(0, 5).map((card, index) => (
                                        <div key={index} className="w-16 h-24 p-6 bg-white rounded-lg shadow text-black flex flex-col items-center">
                                            <span className="text-lg font-bold">{card.rank}</span>
                                            {suits[card.suit]}
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </div>
                        <div className="flex flex-row lg:flex-col justify-center gap-4 lg:mt-0">
                            {gameInitialized && (
                                <>
                                    <button
                                        onClick={() => handleAction('hit')}
                                        disabled={loading}
                                        className={`px-6 py-3 ${loading ? 'bg-gray-400' : 'bg-yellow-400'} rounded-lg text-black text-lg w-75`}
                                    >
                                        {loading ? 'Loading...' : 'Hit'}
                                    </button>
                                    <button 
                                        onClick={() => handleAction('stay')}
                                        disabled={loading}
                                        className={`px-6 py-3 ${loading ? 'bg-gray-400' : 'bg-yellow-400'} rounded-lg text-black text-lg w-75`}
                                    >
                                        {loading ? 'Loading...' : 'Stand'}
                                    </button>
                                </>
                            )}
                            {gameResult && <h2 className={`text-2xl text-center mb-4 ${getResultColor(gameResult)}`}>{gameResult}</h2>}
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