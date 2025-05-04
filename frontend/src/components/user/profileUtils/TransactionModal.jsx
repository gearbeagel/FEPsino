import React, { useState } from "react";
import { DollarSign, X } from "lucide-react";

export default function TransactionModal({ show, onClose, onSubmit }) {
    const [amount, setAmount] = useState("");
    const [txnType, setTxnType] = useState("DEPOSIT");

    const handleSubmit = (e) => {
        e.preventDefault();
        onSubmit(amount, txnType);
        setAmount("");
        setTxnType("DEPOSIT");
    };

    if (!show) return null;

    return (
        <div
            className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50"
            onClick={onClose}
        >
            <div
                className="bg-slate-900 rounded-lg p-6 w-[36rem] shadow-2xl border border-yellow-400 relative"
                onClick={(e) => e.stopPropagation()}
            >
                <button
                    onClick={onClose}
                    className="absolute top-2 right-2 text-gray-400 hover:text-white"
                >
                    <X className="h-6 w-6" />
                </button>
                <div className="flex items-center mb-4">
                    <DollarSign className="h-6 w-6 text-yellow-400 mr-2" />
                    <span className="text-xl text-yellow-400">New Transaction</span>
                </div>
                <form onSubmit={handleSubmit} className="flex flex-col gap-4">
                    <input
                        type="number"
                        step="0.01"
                        required
                        placeholder="Amount"
                        value={amount}
                        onChange={(e) => setAmount(e.target.value)}
                        className="bg-gray-700 text-white rounded p-2"
                    />
                    <select
                        value={txnType}
                        onChange={(e) => setTxnType(e.target.value)}
                        className="bg-gray-700 text-white rounded p-2"
                    >
                        <option value="DEPOSIT">Top Up</option>
                        <option value="WITHDRAWAL">Withdraw</option>
                    </select>
                    <div className="flex justify-end space-x-2">
                        <button
                            type="submit"
                            className="flex-1 flex items-center justify-center bg-yellow-400 text-black px-4 py-2 rounded hover:bg-yellow-500"
                        >
                            Submit
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}