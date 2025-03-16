import React, { useState } from 'react';
import { Coins, RotateCcw, Play, Star, Heart, Cherry, GemIcon, CitrusIcon } from 'lucide-react';

const SYMBOLS = [
  <Star className="h-12 w-12 text-yellow-400" />,
  <Heart className="h-12 w-12 text-red-400" />,
  <Cherry className="h-12 w-12 text-red-400" />,
  <GemIcon className="h-12 w-12 text-blue-400" />,
  <CitrusIcon className="h-12 w-12 text-yellow-400" />,
];

export default function SlotsGame() {
  const [reels, setReels] = useState([SYMBOLS[0], SYMBOLS[0], SYMBOLS[0]]);
  const [isSpinning, setIsSpinning] = useState(false);
  const [balance, setBalance] = useState(1000);
  const [bet, setBet] = useState(10);
  const [lastWin, setLastWin] = useState(0);

  const spin = () => {
    if (balance < bet) return;
    setIsSpinning(true);
    setBalance(prev => prev - bet);

    let shuffleCount = 0;
    const maxShuffles = 20; // How many times the symbols should change before stopping

    const spinInterval = setInterval(() => {
      setReels([
        SYMBOLS[Math.floor(Math.random() * SYMBOLS.length)],
        SYMBOLS[Math.floor(Math.random() * SYMBOLS.length)],
        SYMBOLS[Math.floor(Math.random() * SYMBOLS.length)],
      ]);

      shuffleCount++;
      if (shuffleCount >= maxShuffles) {
        clearInterval(spinInterval);

        // Set final results
        const finalReels = [
          SYMBOLS[Math.floor(Math.random() * SYMBOLS.length)],
          SYMBOLS[Math.floor(Math.random() * SYMBOLS.length)],
          SYMBOLS[Math.floor(Math.random() * SYMBOLS.length)],
        ];
        setReels(finalReels);
        setIsSpinning(false);

        // Calculate winnings
        if (finalReels[0] === finalReels[1] && finalReels[1] === finalReels[2]) {
          const winAmount = bet * 10;
          setBalance(prev => prev + winAmount);
          setLastWin(winAmount);
        } else if (finalReels[0] === finalReels[1] || finalReels[1] === finalReels[2]) {
          const winAmount = bet * 2;
          setBalance(prev => prev + winAmount);
          setLastWin(winAmount);
        } else {
          setLastWin(0);
        }
      }
    }, 100);
  };

  return (
    <div className="bg-black text-white">
      <main className="flex-grow flex flex-col overflow-hidden bg-gradient-to-b from-gray-900 to-black pt-5">
        <div className="container max-w-4xl mx-auto">
          <div className="bg-gray-800 border border-yellow-400 rounded-lg p-6 mb-8">
            <div className="flex justify-between items-center mb-4">
              <div className="flex items-center">
                <Coins className="h-6 w-6 text-yellow-400 mr-2" />
                <span className="text-xl">Balance: ${balance}</span>
              </div>
              <div className="flex items-center">
                <span className="text-xl text-yellow-400">Last Win: ${lastWin}</span>
              </div>
            </div>

            <div className="flex gap-4 items-center">
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
                className="px-4 py-2 bg-gray-700 rounded hover:bg-gray-600"
              >
                2x
              </button>

              <button
                onClick={() => setBet(10)}
                className="px-4 py-2 bg-gray-700 rounded hover:bg-gray-600"
              >
                <RotateCcw className="h-5 w-5" />
              </button>
            </div>
          </div>

          <div className="bg-gray-800 rounded-lg border border-yellow-400 p-8 mb-8">
            <div className="flex justify-center mb-8">
              <div className="grid grid-cols-3 gap-4">
                {reels.map((symbol, index) => (
                  <div
                    key={index}
                    className="w-24 h-24 bg-gray-700 rounded-lg flex items-center justify-center text-4xl overflow-hidden"
                  >
                    {symbol}
                  </div>
                ))}
              </div>
            </div>

            <button
              onClick={spin}
              disabled={isSpinning || balance < bet}
              className={`w-full py-4 rounded-lg flex items-center justify-center text-xl font-bold transition-colors ${
                isSpinning || balance < bet
                  ? 'bg-gray-600 cursor-not-allowed'
                  : 'bg-yellow-400 hover:bg-yellow-500 text-black'
              }`}
            >
              <Play className="h-6 w-6 mr-2" />
              {isSpinning ? 'Spinning...' : 'Spin'}
            </button>
          </div>
        </div>
      </main>
    </div>
  );
}
