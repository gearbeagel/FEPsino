import React, { useState, useEffect } from 'react';
import { Coins, RotateCcw, Play, Star, Heart, Cherry, GemIcon, CitrusIcon, InfoIcon } from 'lucide-react';
import { toast, ToastContainer } from "react-toastify";
import { useAuth } from "../../context/AuthContext";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { fetchBalance } from "./GameApi";

const SYMBOLS = [
  { id: 'star', component: <Star className="h-10 w-10 md:h-12 md:w-12 text-yellow-400" /> },
  { id: 'heart', component: <Heart className="h-10 w-10 md:h-12 md:w-12 text-red-400" /> },
  { id: 'cherry', component: <Cherry className="h-10 w-10 md:h-12 md:w-12 text-red-400" /> },
  { id: 'gem', component: <GemIcon className="h-10 w-10 md:h-12 md:w-12 text-blue-400" /> },
  { id: 'citrus', component: <CitrusIcon className="h-10 w-10 md:h-12 md:w-12 text-yellow-400" /> },
];

const NUM_COLUMNS = 5;
const NUM_ROWS = 3;

export default function SlotsGame() {
  const [reels, setReels] = useState(Array(5).fill(Array(3).fill(SYMBOLS[0])));
  const [isSpinning, setIsSpinning] = useState(false);
  const [balance, setBalance] = useState(0);
  const [bet, setBet] = useState(10);
  const [lastWin, setLastWin] = useState(0);
  const [winData, setWinData] = useState(null);
  const [gameResult, setGameResult] = useState(null);
  const spinIntervalRef = React.useRef(null);

  const { isAuthenticated, loading, user } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
      if (!loading && !isAuthenticated) {
          navigate('/signup');
      }
  }, [isAuthenticated, loading, navigate]);

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

    useEffect(() => {
    return () => {
      if (spinIntervalRef.current) {
        spinIntervalRef.current.forEach(interval => clearInterval(interval));
        spinIntervalRef.current = null;
      }
    };
  }, []);

  const convertBackendResultToReels = (result) => {
    const newReels = [];

    for (let i = 0; i < NUM_COLUMNS; i++) {
      const reelSymbols = result[i].map(symbolIndex => SYMBOLS[symbolIndex]);
      newReels.push(reelSymbols);
    }

    return newReels;
  };

  const generateRandomReels = () => {
    return Array(NUM_COLUMNS).fill().map(() =>
      Array(NUM_ROWS).fill().map(() => SYMBOLS[Math.floor(Math.random() * SYMBOLS.length)])
    );
  };

  const handleSpinEnd = (finalReels, payout, newBalance, winData) => {
    if (spinIntervalRef.current) {
      spinIntervalRef.current.forEach(interval => clearInterval(interval));
      spinIntervalRef.current = null;
    }

    setReels(finalReels);
    setIsSpinning(false);
    setLastWin(payout);
    setBalance(newBalance);
    setWinData(winData);
    setGameResult(payout > 0 ? `You won $${payout}!` : `You lost $${bet}!`);
  };

  const spin = async () => {
    if (balance < bet) {
      toast.error("Insufficient balance for this bet.");
      return;
    }

    setIsSpinning(true);
    setWinData(null);
    setGameResult(null);
    setBalance(prevBalance => prevBalance - bet);

    if (spinIntervalRef.current) {
      spinIntervalRef.current.forEach(interval => clearInterval(interval));
    }

    spinIntervalRef.current = [];

    let tempReels = [...reels];

    for (let colIndex = 0; colIndex < NUM_COLUMNS; colIndex++) {
      const initialInterval = setInterval(() => {
        const randomReel = Array(NUM_ROWS).fill().map(() => 
          SYMBOLS[Math.floor(Math.random() * SYMBOLS.length)]
        );

        tempReels = tempReels.map((col, i) => 
          i === colIndex ? randomReel : col
        );

        setReels([...tempReels]);
      }, 100);

      spinIntervalRef.current.push(initialInterval);
    }

    try {
      const response = await fetch(
        `${import.meta.env.VITE_API_URL}/slots/spins/spin/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
          body: JSON.stringify({
            bet_amount: bet,
          }),
        }
      );

      const result = await response.json();

      if (!response.ok) {
        throw new Error(result.message || "Unexpected error");
      }

      const finalReels = convertBackendResultToReels(result.result);

      for (let colIndex = 0; colIndex < NUM_COLUMNS; colIndex++) {
        ((col) => {
          setTimeout(() => {
            if (spinIntervalRef.current && spinIntervalRef.current[col]) {
              clearInterval(spinIntervalRef.current[col]);

              tempReels = tempReels.map((reelCol, i) => 
                i === col ? finalReels[col] : reelCol
              );

              setReels([...tempReels]);

              if (col === NUM_COLUMNS - 1) {
                setTimeout(() => {
                  setBalance(parseFloat(result.current_balance));
                  handleSpinEnd(
                    finalReels, 
                    parseFloat(result.payout), 
                    parseFloat(result.current_balance), 
                    result.win_data
                  );
                }, 500);
              }
            }
          }, 300 * (col + 1));
        })(colIndex);
      }

    } catch (error) {
      if (spinIntervalRef.current) {
        spinIntervalRef.current.forEach(interval => clearInterval(interval));
      }
      spinIntervalRef.current = null;

      setIsSpinning(false);
      try {
        await fetchBalance(setBalance, user);
      } catch (fetchError) {
        toast.error(fetchError.message);
      }
      toast.error("Error spinning: " + error.message);
    }
  };

  const isWinningSymbol = (colIndex, rowIndex) => {
    if (!winData) return false;

    const backendRowIndex = rowIndex + 1;

    if (winData[backendRowIndex]) {
      const [symbolName, indices] = winData[backendRowIndex];
      return indices.includes(colIndex);
    }

    return false;
  };

  return (
      <div className="flex-grow flex flex-col items-center p-6">
        <div className="container max-w-4xl bg-slate-900 border border-yellow-400 rounded-lg p-6 shadow-xl w-full mb-8">
          <div className="flex justify-between items-center mb-4">
            <div className="flex items-center">
              <Coins className="h-6 w-6 text-yellow-400 mr-2" />
              <span className="text-xl">Balance: ${balance}</span>
            </div>
            <span className="text-xl text-yellow-400 group relative">
              <InfoIcon className="h-6 w-6 mr-2" />
              <span
                className="absolute top-full right-1/2 transform translate-x-6 mt-2 w-max px-2 py-1 text-sm text-yellow-400 bg-slate-950 rounded opacity-0 group-hover:opacity-100 transition-opacity"
              >
                Match 3 or more symbols in a row to win!
              </span>
            </span>
          </div>

            <div className="flex gap-4 items-center">
                <div className="flex-1">
                    <label className="block text-sm mb-1">Bet Amount</label>
                    <select
                        value={bet}
                        onChange={(e) => setBet(Number(e.target.value))}
                        className="w-full bg-gray-700 rounded p-2 text-white"
                        disabled={isSpinning}
                    >
                        <option value="10">$10</option>
                        <option value="20">$20</option>
                        <option value="50">$50</option>
                        <option value="100">$100</option>
                    </select>
                </div>
            </div>

            <button
                onClick={spin}
                disabled={isSpinning}
                className={`w-full px-4 py-2 mt-5 bg-yellow-400 rounded-lg hover:bg-yellow-500 disabled:bg-slate-600 text-black text-xl font-bold shadow-md flex items-center justify-center ${
                    isSpinning
                        ? 'bg-gray-600 cursor-not-allowed'
                        : 'bg-yellow-400 hover:bg-yellow-500 text-black'
                }`}
            >
                <Play className="h-6 w-6 mr-2" />
                {isSpinning ? 'Spinning...' : 'Spin'}
            </button>
        </div>

        <div className="container max-w-4xl bg-slate-900 rounded-lg border border-yellow-400 p-4 sm:p-8 shadow-xl w-full mb-8">
            <div className="flex justify-center mb-8">
                <div className="grid grid-cols-5 gap-2 sm:gap-4">
                    {reels.map((column, colIndex) => (
                        <div key={`column-${colIndex}`} className="flex flex-col gap-2 sm:gap-4 overflow-hidden">
                            {column.map((symbol, rowIndex) => (
                                <div key={`symbol-container-${symbol.id}-${rowIndex}`} className="relative">
                                    {isWinningSymbol(colIndex, rowIndex) && (
                                        <motion.div 
                                            className="absolute inset-0 border-2 bg-green-500 border-green-500 rounded-lg z-20"
                                            animate={{ opacity: [0.5, 0.3, 0.5] }}
                                            transition={{ 
                                                repeat: Infinity, 
                                                duration: 1,
                                                ease: "easeInOut"
                                            }}
                                        />
                                    )}
                                    <motion.div
                                        key={`symbol-${symbol.id}-${rowIndex}`}
                                        className="w-12 h-12 md:w-24 md:h-24 bg-gray-700 rounded-lg flex items-center justify-center text-xl sm:text-4xl overflow-hidden
                                                transition-colors duration-300 relative z-10"
                                    >
                                        {symbol.component}
                                    </motion.div>
                                </div>
                            ))}
                        </div>
                    ))}
                </div>
            </div>

            {gameResult && (
                <h2 className={`text-xl sm:text-2xl text-center ${
                    lastWin > 0 ? "text-green-400" : "text-red-400"
                }`}>
                    {gameResult}
                </h2>
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
