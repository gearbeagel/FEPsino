import React from "react";
import { Banknote, Mail, Pencil, User2, User, DollarSign } from "lucide-react";

export default function UserProfileInfo({ user, onEditProfile, onNewTransaction, onLogout }) {
    return (
        <>
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
            <div className="flex md:flex-row flex-col w-full space-x-2 mt-4">
                <button
                    onClick={onEditProfile}
                    className="flex-1 flex items-center justify-center bg-yellow-400 text-black px-4 py-2 rounded hover:bg-yellow-500"
                >
                    <Pencil className="h-6 w-6 text-black mr-2" />
                    Edit Profile
                </button>
                <button
                    onClick={onNewTransaction}
                    className="flex-1 flex items-center justify-center bg-yellow-400 text-black px-4 py-2 rounded hover:bg-yellow-500"
                >
                    <DollarSign className="h-6 w-6 text-black mr-2" />
                    New Transaction
                </button>
                <button
                    onClick={onLogout}
                    className="flex-1 flex items-center justify-center bg-yellow-400 text-black px-4 py-2 rounded hover:bg-yellow-500"
                >
                    <User2 className="h-6 w-6 text-black mr-2" />
                    Log out
                </button>
            </div>
        </>
    );
}