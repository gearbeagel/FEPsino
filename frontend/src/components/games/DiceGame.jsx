import { useState } from "react";
import { Dice5, RotateCcw } from "lucide-react";

export default function DiceGame() {
    const [balance, setBalance] = useState(1000);
    const [bet, setBet] = useState(10);
    const [lastWin, setLastWin] = useState(0);
    const [diceType1, setDiceType1] = useState('d6');
    const [diceType2, setDiceType2] = useState('d6');
    const [diceValue1, setDiceValue1] = useState(1);
    const [diceValue2, setDiceValue2] = useState(1);
    const [selectedNumber, setSelectedNumber] = useState(1);
    const [gameInitialized, setGameInitialized] = useState(false);

    const diceSides = {
        d6: 6,
        d8: 8,
        d12: 12
    };

    const totalSides = diceSides[diceType1] + diceSides[diceType2];

    const rollDice = () => {
        const max1 = diceType1 === 'd8' ? 8 : diceType1 === 'd12' ? 12 : 6;
        const max2 = diceType2 === 'd8' ? 8 : diceType2 === 'd12' ? 12 : 6;
        const newValue1 = Math.floor(Math.random() * max1) + 1;
        const newValue2 = Math.floor(Math.random() * max2) + 1;
        setDiceValue1(newValue1);
        setDiceValue2(newValue2);

        const sum = newValue1 + newValue2;
        let winAmount = 0;
        if (sum === selectedNumber) {
            winAmount = 40;
        } else if (sum === selectedNumber - 1 || sum === selectedNumber + 1) {
            winAmount = 30;
        }
        setBalance(prev => prev + winAmount - bet);
        setLastWin(winAmount);
        setGameInitialized(true);
    };

    const diceSVG = (diceValue, points) => (
        <svg width="75" height="75" viewBox="0 0 100 100">
            <polygon points={points} fill="#fcc800" />
            <text x="50" y="60" textAnchor="middle" fill="black" fontSize="36">{diceValue}</text>
        </svg>
    );

    const diceD6 = (value) => diceSVG(value, "10,10 90,10 90,90 10,90");
    const diceD8 = (value) => diceSVG(value, "50,10 90,50 50,90 10,50");
    const diceD12 = (value) => diceSVG(value, "50,10 90,30 90,70 50,90 10,70 10,30");

    return (
        <div className="flex flex-col bg-gradient-to-b from-gray-900 to-black text-white">
            <main className="flex-grow flex flex-col items-center p-6">
                <div className="container max-w-4xl bg-slate-900 border border-yellow-400 rounded-lg p-6 shadow-xl w-full">
                    <div className="flex justify-between items-center mb-4">
                        <div className="flex items-center">
                            <Dice5 className="h-6 w-6 text-yellow-400 mr-2" />
                            <span className="text-xl">Balance: ${balance}</span>
                        </div>
                        <span className="text-xl text-yellow-400">Last Win: ${lastWin}</span>
                    </div>

                    <h2 className="text-2xl text-center mb-4">Choose Your Dice</h2>
                    <div className="grid grid-cols-2 gap-2 mb-4">
                        <div className="flex flex-col items-center">
                            <label className="text-sm">Dice 1</label>
                            <div className="flex gap-2">
                                <button onClick={() => setDiceType1('d6')}>{diceD6(6)}</button>
                                <button onClick={() => setDiceType1('d8')}>{diceD8(8)}</button>
                                <button onClick={() => setDiceType1('d12')}>{diceD12(12)}</button>
                            </div>
                        </div>
                        <div className="flex flex-col items-center">
                            <label className="text-sm">Dice 2</label>
                            <div className="flex gap-2">
                                <button onClick={() => setDiceType2('d6')}>{diceD6(6)}</button>
                                <button onClick={() => setDiceType2('d8')}>{diceD8(8)}</button>
                                <button onClick={() => setDiceType2('d12')}>{diceD12(12)}</button>
                            </div>
                        </div>
                    </div>
                    <div className="flex gap-4 items-center mt-6">
                        <div className="flex-1">
                            <label className="block text-sm mb-1">Bet Amount</label>
                            <select
                                value={bet}
                                onChange={(e) => setBet(Number(e.target.value))}
                                className="w-full bg-gray-700 rounded p-2 text-white "
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

                    <div className="flex flex-col gap-4 mt-2">
                        <div className="flex flex-col">
                            <label className="text-sm">Select Number</label>
                            <select
                                value={selectedNumber}
                                onChange={(e) => setSelectedNumber(Number(e.target.value))}
                                className="bg-gray-700 rounded p-2 text-white"
                            >
                                {[...Array(totalSides).keys()].map(n => (
                                    <option key={n + 1} value={n + 1}>{n + 1}</option>
                                ))}
                            </select>
                        </div>

                        <button
                            onClick={rollDice}
                            className="w-full px-4 py-2 bg-yellow-400 rounded-lg hover:bg-yellow-500 text-black text-xl font-bold shadow-md"
                        >
                            Roll Dice
                        </button>
                    </div>
                </div>

                <div className="container max-w-4xl bg-slate-900 border border-yellow-400 rounded-lg p-8 shadow-xl w-full mt-8">
                    <h2 className="text-2xl text-center mb-4">Results</h2>
                    {gameInitialized ? (
                        <div className="flex justify-center gap-4 mb-4">
                            {diceType1 === 'd6' ? diceD6(diceValue1) : diceType1 === 'd8' ? diceD8(diceValue1) : diceD12(diceValue1)}
                            {diceType2 === 'd6' ? diceD6(diceValue2) : diceType2 === 'd8' ? diceD8(diceValue2) : diceD12(diceValue2)}
                        </div>
                    ) : (
                        <div className="flex justify-center gap-4 mb-4">
                            {diceType1 === 'd6' ? diceD6(6) : diceType1 === 'd8' ? diceD8(8) : diceD12(12)}
                            {diceType2 === 'd6' ? diceD6(6) : diceType2 === 'd8' ? diceD8(8) : diceD12(12)}
                        </div>
                    )}
                    {gameInitialized && (
                        lastWin > 0 ? (
                            <div className="text-center text-xl text-yellow-400">You won ${lastWin}</div>
                        ) : (
                            <div className="text-center text-xl text-red-400">You lost ${bet}</div>
                        )
                    )}
                </div>

            </main>
        </div>
    );
}