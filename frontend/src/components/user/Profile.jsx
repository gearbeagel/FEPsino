import React, { useEffect, useState } from "react";
import {
    Banknote,
    DollarSign,
    Mail,
    Pencil,
    User2,
    User,
    Wallet,
    X
} from "lucide-react";
import axios from "axios";
import DisplayDate from "./DateApi.jsx";

const apiUrl = import.meta.env.VITE_API_URL;

export default function Profile() {
    const [user, setUser] = useState(null);
    const [transactions, setTransactions] = useState([]);
    const [showTxnModal, setShowTxnModal] = useState(false);
    const [showEditModal, setShowEditModal] = useState(false);
    const [amount, setAmount] = useState("");
    const [txnType, setTxnType] = useState("DEPOSIT");
    const [editSection, setEditSection] = useState("email");
    const [editData, setEditData] = useState({
        email: user?.user.email || "",
        username: user?.user.username || "",
        old_password: "",
        password: "",
        confirm_password: ""
    });


    useEffect(() => {
        (async () => {
            try {
                const profileRes = await axios.get(`${apiUrl}/user/profile/`, {
                    headers: { Authorization: `Bearer ${localStorage.getItem("access_token")}` }
                });
                setUser(profileRes.data);

                const txnRes = await axios.get(`${apiUrl}/user/transaction/`, {
                    headers: { Authorization: `Bearer ${localStorage.getItem("access_token")}` }
                });
                setTransactions(txnRes.data);
            } catch (err) {
                console.error(err);
            }
        })();
    }, []);

    const handleLogout = async () => {
        try {
            await axios.post(`${apiUrl}/user/logout/`, {
                refresh_token: localStorage.getItem("refresh_token")
            }, {
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${localStorage.getItem("access_token")}`
                }
            });
        } catch {}
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        window.location.href = "/";
    };

    const handleTransaction = async e => {
        e.preventDefault();
        try {
            const res = await axios.post(`${apiUrl}/user/transaction/`, {
                amount: parseFloat(amount),
                transaction_type: txnType
            }, {
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${localStorage.getItem("access_token")}`
                }
            });
            setTransactions(prev => [...prev, res.data]);
            setAmount("");
            setTxnType("DEPOSIT");
            setShowTxnModal(false);
        } catch (err) {
            console.error(err);
        }
    };

    const handleProfileSave = async e => {
        e.preventDefault();
        try {
            await axios.put(`${apiUrl}/user/update/`, editData, {
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${localStorage.getItem("access_token")}`
                }
            });
            setShowEditModal(false);
            setEditData({ old_password: "", password: "", confirm_password: "" });
        } catch (err) {
            console.error(err);
        }
    };

    if (!user) return <div>Loading…</div>;

    return (
        <div className="flex-grow flex flex-col items-center p-6">
            <div className="container max-w-4xl bg-slate-900 border border-yellow-400 rounded-lg p-6 shadow-xl w-full">
                <div className="flex justify-between items-center mb-4">
                    <div className="flex items-center">
                        <User className="h-6 w-6 text-yellow-400 mr-2" />
                        <span className="text-xl text-yellow-400">{user.username}'s profile</span>
                    </div>
                </div>
                <div className="flex flex-col items-start gap-2">
                    <div className="flex items-center">
                        <Mail className="h-6 w-6 text-yellow-400 mr-2" />
                        <span className="text-xl">{user.user.email}</span>
                    </div>
                    <div className="flex items-center">
                        <Banknote className="h-6 w-6 text-yellow-400 mr-2" />
                        <span className="text-xl">${parseFloat(user.balance || 0).toFixed(2)}</span>
                    </div>
                </div>
                <div className="flex flex-row w-full space-x-2 mt-4">
                    <button
                        onClick={() => setShowEditModal(true)}
                        className="flex-1 flex items-center justify-center bg-yellow-400 text-black px-4 py-2 rounded hover:bg-yellow-500"
                    >
                        <Pencil className="h-6 w-6 text-black mr-2" />
                        Edit Profile
                    </button>
                    <button
                        onClick={() => setShowTxnModal(true)}
                        className="flex-1 flex items-center justify-center bg-yellow-400 text-black px-4 py-2 rounded hover:bg-yellow-500"
                    >
                        <DollarSign className="h-6 w-6 text-black mr-2" />
                        New Transaction
                    </button>
                    <button
                        onClick={handleLogout}
                        className="flex-1 flex items-center justify-center bg-yellow-400 text-black px-4 py-2 rounded hover:bg-yellow-500"
                    >
                        <User2 className="h-6 w-6 text-black mr-2" />
                        Log out
                    </button>
                </div>
                <div className="mt-6">
                    <div className="flex items-center mb-4">
                        <Wallet className="h-6 w-6 text-yellow-400 mr-2" />
                        <span className="text-xl text-yellow-400">Transactions</span>
                    </div>
                    <div className="overflow-auto max-h-60">
                        <table className="table-auto w-full text-left border-collapse border border-gray-700">
                            <thead className="bg-gray-800 text-yellow-400">
                            <tr>
                                <th className="px-4 py-2 border border-gray-700">Date</th>
                                <th className="px-4 py-2 border border-gray-700">Type</th>
                                <th className="px-4 py-2 border border-gray-700">Amount</th>
                            </tr>
                            </thead>
                            <tbody>
                            {transactions.map((t, i) => (
                                <tr key={i} className="odd:bg-gray-700 even:bg-gray-800 hover:bg-gray-600">
                                    <td className="px-4 py-2 border border-gray-700">
                                        <DisplayDate dateString={t.date} />
                                    </td>
                                    <td className="px-4 py-2 border border-gray-700">
                                        {t.transaction_type}
                                    </td>
                                    <td className="px-4 py-2 border border-gray-700">
                                        {parseFloat(t.amount).toFixed(2)}
                                    </td>
                                </tr>
                            ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            {showTxnModal && (
                <div
                    className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50"
                    onClick={() => setShowTxnModal(false)}
                >
                    <div
                        className="bg-slate-900 rounded-lg p-6 w-[36rem] shadow-2xl border border-yellow-400 relative"
                        onClick={(e) => e.stopPropagation()}
                    >
                        <button
                            onClick={() => setShowTxnModal(false)}
                            className="absolute top-2 right-2 text-gray-400 hover:text-white"
                        >
                            <X className="h-6 w-6" />
                        </button>
                        <div className="flex items-center mb-4">
                            <DollarSign className="h-6 w-6 text-yellow-400 mr-2" />
                            <span className="text-xl text-yellow-400">New Transaction</span>
                        </div>
                        <form onSubmit={handleTransaction} className="flex flex-col gap-4">
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
            )}

            {showEditModal && (
                <div
                    className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50"
                    onClick={() => setShowEditModal(false)}
                >
                    <div
                        className="bg-slate-900 rounded-lg p-6 w-[48rem] h-[20rem] shadow-2xl border border-yellow-400 grid grid-cols-[1fr_auto_2fr] gap-6 relative"
                        onClick={(e) => e.stopPropagation()}
                    >
                        <button
                            onClick={() => setShowEditModal(false)}
                            className="absolute top-2 right-2 text-gray-400 hover:text-white"
                        >
                            <X className="h-6 w-6" />
                        </button>
                        <div className="space-y-3">
                            <div className="flex items-center text-yellow-400 mb-4">
                                <Pencil className="h-6 w-6 mr-2" />
                                <span className="text-xl">Edit Profile</span>
                            </div>
                            <button
                                onClick={() => setEditSection("email")}
                                className={`block w-full text-left px-4 py-2 rounded ${
                                    editSection === "email" ? "bg-yellow-400 text-black" : "bg-gray-700 text-white"
                                }`}
                            >
                                Email
                            </button>
                            <button
                                onClick={() => setEditSection("username")}
                                className={`block w-full text-left px-4 py-2 rounded ${
                                    editSection === "username" ? "bg-yellow-400 text-black" : "bg-gray-700 text-white"
                                }`}
                            >
                                Username
                            </button>
                            <button
                                onClick={() => setEditSection("password")}
                                className={`block w-full text-left px-4 py-2 rounded ${
                                    editSection === "password" ? "bg-yellow-400 text-black" : "bg-gray-700 text-white"
                                }`}
                            >
                                Password
                            </button>
                        </div>
                        <div className="border-l-2 border-yellow-400" />
                        <div className="mt-7">
                            <form onSubmit={handleProfileSave} className="flex flex-col gap-4">
                                {editSection === "email" && (
                                    <input
                                        type="email"
                                        required
                                        placeholder="New Email"
                                        value={editData.email || ""}
                                        onChange={(e) => setEditData({ ...editData, email: e.target.value })}
                                        className="bg-gray-700 text-white rounded p-2"
                                    />
                                )}
                                {editSection === "username" && (
                                    <input
                                        type="text"
                                        required
                                        placeholder="New Username"
                                        value={editData.username || ""}
                                        onChange={(e) => setEditData({ ...editData, username: e.target.value })}
                                        className="bg-gray-700 text-white rounded p-2"
                                    />
                                )}
                                {editSection === "password" && (
                                    <>
                                        <input
                                            type="password"
                                            required
                                            placeholder="Old Password"
                                            value={editData.old_password}
                                            onChange={(e) => setEditData({ ...editData, old_password: e.target.value })}
                                            className="bg-gray-700 text-white rounded p-2"
                                        />
                                        <input
                                            type="password"
                                            required
                                            placeholder="New Password"
                                            value={editData.password}
                                            onChange={(e) => setEditData({ ...editData, password: e.target.value })}
                                            className="bg-gray-700 text-white rounded p-2"
                                        />
                                        <input
                                            type="password"
                                            required
                                            placeholder="Confirm Password"
                                            value={editData.confirm_password}
                                            onChange={(e) => setEditData({ ...editData, confirm_password: e.target.value })}
                                            className="bg-gray-700 text-white rounded p-2"
                                        />
                                    </>
                                )}
                                <div className="flex justify-end space-x-2 mt-4">
                                    <button
                                        type="submit"
                                        className="flex-1 flex items-center justify-center bg-yellow-400 text-black px-4 py-2 rounded hover:bg-yellow-500"
                                    >
                                        Save
                                    </button>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}
