import React, { useState, useEffect } from "react";
import { Pencil, X } from "lucide-react";
import {toast, ToastContainer} from "react-toastify";
import PropTypes from "prop-types";

export default function EditProfileModal({ show, onClose, onSubmit, userData }) {
    const [editSection, setEditSection] = useState("email");
    const [editData, setEditData] = useState({
        email: "",
        username: "",
        old_password: "",
        password: "",
        confirm_password: ""
    });

    useEffect(() => {
        if (userData) {
            setEditData(prevData => ({
                ...prevData,
                email: userData.user?.email || "",
                username: userData.username || ""
            }));
        }
    }, [userData]);

    const handleSubmit = (e) => {
        e.preventDefault();
        
        if (editSection === "password") {
            if (editData.old_password === editData.password) {
                toast.error("New password must be different from the current password");
                return;
            }
            if (editData.password !== editData.confirm_password) {
                toast.error("New passwords do not match");
                return;
            }
        }
        
        onSubmit(editData);
        setEditData(prevData => ({
            ...prevData,
            old_password: "",
            password: "",
            confirm_password: ""
        }));
    };

    if (!show) return null;

    return (
        <div
            className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50"
            onClick={onClose}
        >
            <div
                className="bg-slate-900 rounded-lg p-6 w-[48rem] h-[20rem] shadow-2xl border border-yellow-400 grid grid-cols-[1fr_auto_2fr] gap-6 relative"
                onClick={(e) => e.stopPropagation()}
            >
                <button
                    onClick={onClose}
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
                    <form onSubmit={handleSubmit} className="flex flex-col gap-4">
                        {editSection === "email" && (
                            <input
                                type="email"
                                required
                                placeholder="New Email"
                                value={editData.email}
                                onChange={(e) => setEditData({ ...editData, email: e.target.value })}
                                className="bg-gray-700 text-white rounded p-2"
                            />
                        )}
                        {editSection === "username" && (
                            <input
                                type="text"
                                required
                                placeholder="New Username"
                                value={editData.username}
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
            <ToastContainer
                theme="dark"
                position="top-right"
                autoClose={3000}
                hideProgressBar={false}
                newestOnTop={false}
                closeOnClick
                rtl={false}
            />
        </div>
    );
}

EditProfileModal.propTypes = {
    show: PropTypes.bool.isRequired,
    onClose: PropTypes.func.isRequired,
    onSubmit: PropTypes.func.isRequired,
    userData: PropTypes.shape({
        user: PropTypes.shape({
            email: PropTypes.string,
        }),
        username: PropTypes.string,
    }).isRequired,
}