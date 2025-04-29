// BlackJackGame.jsx
import React, { useState } from "react";
import { Club, Play, RotateCcw, Heart, Diamond, Spade } from "lucide-react";
import { Deck } from "./GameApi.jsx";

const suits = {
    hearts: <Heart className="text-red-500" />,
    diamonds: <Diamond className="text-red-500" />,
    clubs: <Club className="text-black" />,
    spades: <Spade className="text-black" />,
};

function getResultColor(result) {
    if (!result) return "text-gray-500";
    if (result.includes("won")) {
        return "text-green-400";
    } else if (result.includes("lost")) {
        return "text-red-400";
    } else {
        return "text-yellow-400";
    }
}

function calculateHandValue(hand) {
    let value = hand.reduce((sum, card) => sum + card.value, 0);
    let aces = hand.filter(card => card.name === "A").length;
    while (value > 21 && aces > 0) {
        value -= 10;
        aces -= 1;
    }
    return value;
}

export default function BlackJackGame() {
    const [balance, setBalance] = useState(1000);
    const [bet, setBet] = useState(10);
    const [lastWin, setLastWin] = useState(0);
    const [gameInitialized, setGameInitialized] = useState(false);
    const [deck] = useState(new Deck());
    const [playerHand, setPlayerHand] = useState([]);
    const [dealerHand, setDealerHand] = useState([]);
    const [gameResult, setGameResult] = useState(null);

    const startGame = () => {
        setPlayerHand([deck.drawCard(), deck.drawCard()]);
        setDealerHand([deck.drawCard(), deck.drawCard()]);
        setGameResult(null);
        setGameInitialized(true);
    };

    const hit = () => {
        const newHand = [...playerHand, deck.drawCard()];
        setPlayerHand(newHand);
        if (calculateHandValue(newHand) > 21) {
            setGameResult("You busted!");
            setBalance(balance - bet);
            setGameInitialized(false);
        }
    };

    const stand = () => {
        const playerValue = calculateHandValue(playerHand);
        let dealerCards = [...dealerHand];
        let dealerValue = calculateHandValue(dealerCards);

        while (dealerValue < 17) {
            dealerCards.push(deck.drawCard());
            dealerValue = calculateHandValue(dealerCards);
        }

        setDealerHand(dealerCards);

        if (playerValue > 21 || (dealerValue <= 21 && dealerValue >= playerValue)) {
            setGameResult(`You lost $${bet}!`);
            setLastWin(bet);
            setBalance(balance - bet);
        } else {
            setGameResult(`You won $${bet}!`);
            setLastWin(bet);
            setBalance(balance + bet);
        }
        setGameInitialized(false);
    };

    return (
        <div className="flex-grow flex flex-col items-center p-6">
            <div className="container max-w-4xl bg-slate-900 border border-yellow-400 rounded-lg p-6 shadow-xl w-full">
                <div className="flex justify-between items-center mb-4">
                    <div className="flex items-center">
                        <Club className="h-6 w-6 text-yellow-400 mr-2" />
                        <span className="text-xl">Balance: ${balance}</span>
                    </div>
                    <span className="text-xl text-yellow-400">Last Win: ${lastWin}</span>
                </div>
                <div className="flex gap-4 items-center mt-6">
                    <div className="flex-1">
                        <label className="block text-sm mb-1">Bet Amount</label>
                        <select
                            value={bet}
                            onChange={(e) => setBet(Number(e.target.value))}
                            className="w-full bg-gray-700 rounded p-2 text-white"
                        >
                            <option value="10">$10</option>
                            <option value="20">$20</option>
                            <option value="50">$50</option>
                            <option value="100">$100</option>
                        </select>
                    </div>
                    <button
                        onClick={() => setBet(prev => Math.min(prev * 2, 100))}
                        className="px-4 py-2 bg-gray-700 rounded-lg hover:bg-gray-600"
                    >
                        2x
                    </button>
                    <button
                        onClick={() => setBet(10)}
                        className="px-4 py-2 bg-gray-700 rounded-lg hover:bg-gray-600"
                    >
                        <RotateCcw className="h-5 w-5 text-yellow-400" />
                    </button>
                </div>
                <button
                    onClick={startGame}
                    className="w-full px-4 py-2 bg-yellow-400 rounded-lg hover:bg-yellow-500 text-black flex items-center justify-center text-xl font-bold transition-colors mt-5"
                >
                    <Play className="h-6 w-6 mr-2" />
                    Start Game
                </button>
            </div>

            {(gameInitialized || gameResult) && (
                <div className="container max-w-4xl bg-slate-900 border border-yellow-400 rounded-lg p-8 shadow-xl w-full mt-8">
                    <div className="flex gap-4">
                        <div className="flex-1">
                            <h2 className="text-2xl text-start mb-4">Dealer's Hand</h2>
                            <div className="flex justify-center mb-4">
                                <div className="grid grid-cols-5 gap-4">
                                    {dealerHand.slice(0, 5).map((card, index) => (
                                        <div key={index} className="w-16 h-24 p-4 bg-white rounded-lg shadow text-black flex flex-col items-center">
                                            {index === 0 || gameResult ? (
                                                <>
                                                    <span className="text-lg font-bold">{card.name}</span>
                                                    {suits[card.suit]}
                                                </>
                                            ) : (
                                                <div className="w-12 h-16 rounded-lg" />
                                            )}
                                        </div>
                                    ))}
                                </div>
                            </div>
                            <h2 className="text-2xl text-start mb-4">Your Hand</h2>
                            <div className="flex justify-center mb-8">
                                <div className="grid grid-cols-5 gap-4">
                                    {playerHand.slice(0, 5).map((card, index) => (
                                        <div key={index} className="w-16 h-24 p-4 bg-white rounded-lg shadow text-black flex flex-col items-center">
                                            <span className="text-lg font-bold">{card.name}</span>
                                            {suits[card.suit]}
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </div>
                        <div className="flex-1 flex flex-col justify-center gap-4 mt-6">
                            {gameInitialized && (
                                <>
                                    <button onClick={hit} className="px-6 py-3 bg-yellow-400 rounded-lg text-black text-lg">Hit</button>
                                    <button onClick={stand} className="px-6 py-3 bg-yellow-400 rounded-lg text-black text-lg">Stand</button>
                                </>
                            )}
                            <h2 className={`text-2xl text-center mb-4 ${getResultColor(gameResult)}`}>{gameResult}</h2>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}