import React, { useState, useEffect } from "react";
import {Dice5, InfoIcon, Play} from "lucide-react";
import { motion } from "framer-motion";
import diceVariants from "../animations/DiceSpinningAnimation.jsx";
import { toast, ToastContainer } from "react-toastify";
import { useAuth } from "../../context/AuthContext";
import { useNavigate } from "react-router-dom";
import {fetchBalance} from "./GameApi.jsx";

export default function DiceGame() {
    const [bet, setBet] = useState(10);
    const [balance, setBalance] = useState(0);
    const [lastWin, setLastWin] = useState(0);
    const [diceType1, setDiceType1] = useState("d6");
    const [diceType2, setDiceType2] = useState("d6");
    const [diceValue1, setDiceValue1] = useState(1);
    const [diceValue2, setDiceValue2] = useState(1);
    const [selectedNumber, setSelectedNumber] = useState(2);
    const [gameInitialized, setGameInitialized] = useState(false);
    const [rolling, setRolling] = useState(false);
    const [gameResult, setGameResult] = useState(null);

    const { isAuthenticated, loading } = useAuth();
    const navigate = useNavigate();

    useEffect(() => {
        if (!loading && !isAuthenticated) {
            navigate('/signup');
        }
    }, [isAuthenticated, loading, navigate]);

    const diceSides = { d6: 6, d8: 8, d12: 12 };

    const { user } = useAuth();

    useEffect(() => {
        const getInitialBalance = async () => {
            try {
                await fetchBalance(setBalance, null);
            } catch (error) {
                toast.error(error.message);
            }
        };

        if (!loading && isAuthenticated) {
            getInitialBalance();
        }
    }, [loading, isAuthenticated]);

    const totalSides = diceSides[diceType1] + diceSides[diceType2];

    const DICE_SHAPES = {
        d6:  "10,10 90,10 90,90 10,90",
        d8:  "50,10 90,50 50,90 10,50",
        d12: "50,10 90,30 90,70 50,90 10,70 10,30",
    };

    const renderDice = (type, value) => {
        const points = DICE_SHAPES[type] || DICE_SHAPES.d6;
        return (
            <svg width="75" height="75" viewBox="0 0 100 100">
                <polygon points={points} fill="#fcc800" />
                <text
                    x="50"
                    y="60"
                    textAnchor="middle"
                    fill="black"
                    fontSize="36"
                >
                    {value}
                </text>
            </svg>
        );
    };

    const rollDice = async () => {
        setRolling(true);
        setGameResult(null);
        try {
            const response = await fetch(
                `${import.meta.env.VITE_API_URL}/dice/start/`,
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${localStorage.getItem(
                            "access_token"
                        )}`,
                    },
                    body: JSON.stringify({
                        choice1: diceSides[diceType1],
                        choice2: diceSides[diceType2],
                        bet,
                        guessed_number: selectedNumber,
                    }),
                }
            );
            const result = await response.json();
            if (!response.ok) throw new Error(result.error || "Unexpected error");
            setDiceValue1(result.roll1);
            setDiceValue2(result.roll2);
            setLastWin(result.payout);
            setBalance(result.new_balance);
            setGameInitialized(true);
            setGameResult(result.payout > 0 ? `You won $${result.payout}!` : `You lost $${bet}!`);
        } catch (error) {
            if (error.message === "Not enough coins!") {
                error.message = "Insufficient balance for this bet.";
            }
            toast.error(error.message);
        } finally {
            setRolling(false);
        }
    };

    const DICE_TYPES = ["d6", "d8", "d12"];

    return (
        <div className="flex-grow flex flex-col items-center p-6 overflow-y-auto">
            <div className="container max-w-4xl bg-slate-900 border border-yellow-400 rounded-lg p-6 shadow-xl w-full">
                <div className="flex justify-between items-center mb-4">
                    <div className="flex items-center">
                        <Dice5 className="h-6 w-6 text-yellow-400 mr-2" />
                        <span className="text-xl">Balance: ${balance}</span>
                    </div>
                    <span className="text-xl text-yellow-400 group relative">
                    <InfoIcon className="h-6 w-6 mr-2" />
                    <span
                        className="absolute top-full right-1/2 transform translate-x-6 mt-2 w-max px-2 py-1 text-sm text-yellow-400 bg-slate-950 rounded opacity-0 group-hover:opacity-100 transition-opacity"
                    >
                        Choose your dice,
                        <br/>
                        bet on a number and roll to win!
                    </span>
                </span>
                </div>

                <h2 className="text-2xl text-center mb-4">Choose Your Dice</h2>
                <div className="grid md:grid-cols-2 grid-cols-1 gap-2 mb-4">
                    {[1, 2].map((idx) => (
                        <div key={idx} className="flex flex-col items-center">
                            <label className="text-sm">Dice {idx}</label>
                            <div className="flex gap-2">
                                {DICE_TYPES.map((type) => (
                                    <button
                                        key={type}
                                        onClick={() =>
                                            idx === 1
                                                ? setDiceType1(type)
                                                : setDiceType2(type)
                                        }
                                    >
                                        {renderDice(type, diceSides[type])}
                                    </button>
                                ))}
                            </div>
                        </div>
                    ))}
                </div>

                <div className="flex flex-col gap-4 mt-2">
                    <div className="flex flex-col">
                        <label htmlFor="selectedNumber" className="text-sm">Select Number</label>
                        <select
                            id="selectedNumber"
                            value={selectedNumber}
                            onChange={(e) =>
                                setSelectedNumber(Number(e.target.value))
                            }
                            className="bg-gray-700 rounded p-2 text-white"
                        >
                            {[...Array(totalSides - 1).keys()].map((n) => {
                                const val = n + 2;
                                return (
                                    <option key={val} value={val}>
                                        {val}
                                    </option>
                                );
                            })}
                        </select>
                    </div>

                    <div className="flex-1">
                        <label htmlFor="betAmount" className="block text-sm mb-1">Bet Amount</label>
                        <select
                            id="betAmount"
                            value={bet}
                            onChange={(e) => setBet(Number(e.target.value))}
                            className="w-full bg-gray-700 rounded p-2 text-white"
                        >
                            {[10, 20, 50, 100].map((amt) => (
                                <option key={amt} value={amt}>
                                    ${amt}
                                </option>
                            ))}
                        </select>
                    </div>

                    <button
                        onClick={rollDice}
                        disabled={rolling}
                        className="w-full px-4 py-2 bg-yellow-400 rounded-lg hover:bg-yellow-500 disabled:bg-slate-600 text-black text-xl font-bold shadow-md flex items-center justify-center"
                    >
                        <Play className="h-6 w-6 mr-2" />
                        {rolling ? "Rolling..." : "Roll Dice"}
                    </button>
                </div>
            </div>

            <div className="container max-w-4xl bg-slate-900 border border-yellow-400 rounded-lg p-8 shadow-xl w-full mt-8">
                <h2 className="text-2xl text-center mb-4">Results</h2>
                <div className="flex justify-center gap-4 mb-4">
                    <motion.div
                        variants={diceVariants}
                        initial="initial"
                        animate={rolling ? "animate" : "initial"}
                    >
                        {renderDice(diceType1, diceValue1)}
                    </motion.div>
                    <motion.div
                        variants={diceVariants}
                        initial="initial"
                        animate={rolling ? "animate" : "initial"}
                    >
                        {renderDice(diceType2, diceValue2)}
                    </motion.div>
                </div>
                {gameResult && (
                    <div className={`text-center text-xl ${
                        lastWin > 0 ? "text-green-400" : "text-red-400"
                    }`}>
                        {gameResult}
                    </div>
                )}
            </div>

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
