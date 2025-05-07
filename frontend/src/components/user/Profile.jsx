import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import UserProfileInfo from "./profileUtils/UserProfileInfo.jsx";
import TransactionTable from "./profileUtils/TransactionTable.jsx";
import TransactionModal from "./profileUtils/TransactionModal.jsx";
import EditProfileModal from "./profileUtils/EditProfileModal.jsx";
import { useAuth } from "../../context/AuthContext.jsx";

const apiUrl = import.meta.env.VITE_API_URL;

export default function Profile() {
    const navigate = useNavigate();
    const { logout } = useAuth();
    const [user, setUser] = useState(null);
    const [transactions, setTransactions] = useState([]);
    const [showTxnModal, setShowTxnModal] = useState(false);
    const [showEditModal, setShowEditModal] = useState(false);

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
            await logout();
        } catch {}
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
    };

    const handleTransaction = async (amount, txnType) => {
        try {
            await axios.post(`${apiUrl}/user/transaction/`, {
                amount: parseFloat(amount),
                transaction_type: txnType
            }, {
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${localStorage.getItem("access_token")}`
                }
            });

            const txnRes = await axios.get(`${apiUrl}/user/transaction/`, {
                headers: { Authorization: `Bearer ${localStorage.getItem("access_token")}` }
            });
            setTransactions(txnRes.data);

            const profileRes = await axios.get(`${apiUrl}/user/profile/`, {
                headers: { Authorization: `Bearer ${localStorage.getItem("access_token")}` }
            });
            setUser(profileRes.data);

            setShowTxnModal(false);
        } catch (err) {
            console.error(err);
        }
    };

    const handleProfileSave = async (editData) => {
        try {
            await axios.patch(`${apiUrl}/user/profile/`, editData, {
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${localStorage.getItem("access_token")}`
                }
            });
            setShowEditModal(false);
            const profileRes = await axios.get(`${apiUrl}/user/profile/`, {
                headers: { Authorization: `Bearer ${localStorage.getItem("access_token")}` }
            });
            setUser(profileRes.data);
        } catch (err) {
            console.error(err);
        }
    };

    if (!user) return <div>Loading…</div>;

    return (
        <div className="flex-grow flex flex-col items-center p-6">
            <div className="container max-w-4xl bg-slate-900 border border-yellow-400 rounded-lg p-6 shadow-xl w-full">
                <UserProfileInfo 
                    user={user} 
                    onEditProfile={() => setShowEditModal(true)} 
                    onNewTransaction={() => setShowTxnModal(true)} 
                    onLogout={handleLogout} 
                />
                <TransactionTable transactions={transactions} />
            </div>

            <TransactionModal 
                show={showTxnModal} 
                onClose={() => setShowTxnModal(false)} 
                onSubmit={handleTransaction} 
            />

            <EditProfileModal 
                show={showEditModal} 
                onClose={() => setShowEditModal(false)} 
                onSubmit={handleProfileSave} 
                userData={user} 
            />
        </div>
    );
}
