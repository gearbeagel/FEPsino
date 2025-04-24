import React, { useState } from "react";
import axios from "axios";
import { User } from "lucide-react";
import { AnimatePresence, motion } from "framer-motion";
import formVariants from "../animations/FormAnimations";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { useNavigate } from "react-router-dom";
import PropTypes from "prop-types";

const AuthButton = ({ onClick, children }) => (
    <button
        name="authButton"
        onClick={onClick}
        className="bg-yellow-400 text-black hover:bg-yellow-500 px-6 py-2 rounded mt-4 transition-colors w-100 flex items-center justify-center"
        data-testid="auth-submit"
    >
        {children}
    </button>
);

AuthButton.propTypes = {
    onClick: PropTypes.func.isRequired,
    children: PropTypes.node.isRequired,
};

const ConfirmPasswordField = ({ confirmPassword, setConfirmPassword }) => (
    <>
        <label htmlFor="confirmPassword" className="text-sm my-3">Confirm Password:</label>
        <input
            id="confirmPassword"
            name="confirmPassword"
            type="password"
            required
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
        />
    </>
);

ConfirmPasswordField.propTypes = {
    confirmPassword: PropTypes.string.isRequired,
    setConfirmPassword: PropTypes.func.isRequired,
}

export default function SignUpIn() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [isSignUp, setIsSignUp] = useState(true);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    const toggleForm = () => setIsSignUp(!isSignUp);
    const apiUrl = import.meta.env.VITE_API_URL;

    const handleAuth = async (e) => {
        e.preventDefault();
        setError(null);

        if (!email || !password || (isSignUp && !confirmPassword)) {
            toast.error("All fields are required!");
            return;
        }

        if (isSignUp && password !== confirmPassword) {
            toast.error("Passwords do not match!");
            return;
        }

        try {
            const endpoint = isSignUp ? "/user/create/" : "/user/token/";
            const payload = { email, password };
            const res = await axios.post(
                `${apiUrl}${endpoint}`,
                payload,
                { headers: { "Content-Type": "application/json" }, withCredentials: true }
            );

            if (!isSignUp && res.data.access && res.data.refresh) {
                localStorage.setItem("access_token", res.data.access);
                localStorage.setItem("refresh_token", res.data.refresh);
                axios.defaults.headers.common["Authorization"] = `Bearer ${res.data.access}`;
                window.location.reload();
                navigate("/");
            }

            toast.success(res.data.message);
            if (isSignUp) setTimeout(() => setIsSignUp(false), 500);
        } catch (err) {
            setError(err.response?.data?.detail || "Authentication failed");
            console.log(error);
        }
    };

    return (
        <div className="flex-grow flex flex-col items-center p-6">
            <motion.div
                className="container max-w-4xl bg-slate-900 border border-yellow-400 rounded-lg p-6 shadow-xl w-full overflow-hidden"
                initial={{ height: "auto" }}
                animate={{ height: "auto" }}
                transition={{ duration: 0.5, ease: "easeInOut" }}
            >
                <div className="flex items-center">
                    <User className="h-6 w-6 text-yellow-400 mr-2" />
                    <span className="text-xl text-yellow-400" data-testid="auth-title">
            {isSignUp ? "Sign up" : "Sign in"}
          </span>
                </div>

                <AnimatePresence mode="wait">
                    <motion.div
                        key={isSignUp ? "signup" : "signin"}
                        variants={formVariants}
                        initial="hidden"
                        animate="visible"
                        exit="hidden"
                    >
                        <label htmlFor="email" className="text-sm my-3">Email:</label>
                        <input
                            id="email"
                            name="email"
                            type="email"
                            required
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            className="w-full bg-gray-700 rounded p-2 text-white"
                            data-testid="email-input"
                        />
                        <label htmlFor="password" className="text-sm my-3">Password:</label>
                        <input
                            id="password"
                            name="password"
                            type="password"
                            required
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="w-full bg-gray-700 rounded p-2 text-white"
                            data-testid="password-input"
                        />

                        {isSignUp && <ConfirmPasswordField confirmPassword={confirmPassword} setConfirmPassword={setConfirmPassword}/>}

                        <div className="flex flex-col items-center">
                            <div className="text-sm text-gray-400 mt-4">
                                {isSignUp ? "Already have an account?" : "Don't have an account?"}{" "}
                                <button
                                    onClick={toggleForm}
                                    className="text-yellow-400"
                                    data-testid="toggle-auth-form"
                                >
                                    {isSignUp ? "Sign in" : "Sign up"}
                                </button>
                            </div>
                            <div className="grid grid-cols-1 gap-4">
                                <AuthButton onClick={handleAuth}>
                                    {isSignUp ? "Sign up" : "Sign in"}
                                </AuthButton>
                            </div>
                        </div>
                    </motion.div>
                </AnimatePresence>
            </motion.div>
            <ToastContainer
                position="top-right"
                autoClose={3000}
                hideProgressBar={false}
                newestOnTop
                closeOnClick
                rtl={false}
                pauseOnFocusLoss
                draggable
                pauseOnHover
                theme="dark"
            />
        </div>
    );
}
