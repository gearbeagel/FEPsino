import React, { useState, useEffect } from "react";
import axios from "axios";
import { User, Eye, EyeOff, Check } from "lucide-react";
import { AnimatePresence, motion } from "framer-motion";
import formVariants from "../animations/FormAnimations";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { useNavigate } from "react-router-dom";
import PropTypes from "prop-types";
import { useAuth } from "../../context/AuthContext";

const AuthButton = ({ onClick, children }) => (
    <button
        name="authButton"
        onClick={onClick}
        className="bg-yellow-400 text-black hover:bg-yellow-500 px-6 py-2 rounded mt-4 transition-colors md:w-75 flex items-center justify-center"
        data-testid="auth-submit"
    >
        {children}
    </button>
);

AuthButton.propTypes = {
    onClick: PropTypes.func.isRequired,
    children: PropTypes.node.isRequired,
};

const PasswordField = ({ password, setPassword, label, id, name }) => {
    const [showPassword, setShowPassword] = useState(false);

    return (
        <>
            <label htmlFor={id} className="text-sm my-3">{label}:</label>
            <div className="relative">
                <input
                    id={id}
                    name={name}
                    type={showPassword ? "text" : "password"}
                    required
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="w-full bg-gray-700 rounded p-2 text-white my-2 pr-10"
                    data-testid={`${id}-input`}
                />
                <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-white"
                >
                    {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                </button>
            </div>
        </>
    );
};

PasswordField.propTypes = {
    password: PropTypes.string.isRequired,
    setPassword: PropTypes.func.isRequired,
    label: PropTypes.string.isRequired,
    id: PropTypes.string.isRequired,
    name: PropTypes.string.isRequired,
};

const ConfirmPasswordField = ({ confirmPassword, setConfirmPassword }) => {
    const [showPassword, setShowPassword] = useState(false);

    return (
        <>
            <label htmlFor="confirmPassword" className="text-sm my-3">Confirm Password:</label>
            <div className="relative">
                <input
                    id="confirmPassword"
                    name="confirmPassword"
                    type={showPassword ? "text" : "password"}
                    required
                    value={confirmPassword}
                    className="w-full bg-gray-700 rounded p-2 text-white my-2 pr-10"
                    onChange={(e) => setConfirmPassword(e.target.value)}
                />
                <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-white"
                >
                    {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                </button>
            </div>
        </>
    );
};

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
    const [isAgeVerified, setIsAgeVerified] = useState(false);
    const navigate = useNavigate();
    const { login, isAuthenticated } = useAuth();

    useEffect(() => {
        if (isAuthenticated) {
            navigate('/profile');
        }
    }, [isAuthenticated, navigate]);

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

        if (isSignUp && !isAgeVerified) {
            toast.error("You must be at least 21 years old to register!");
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
                login(res.data);
                navigate('/');
            }

            toast.success(res.data.message);
            if (isSignUp) setTimeout(() => setIsSignUp(false), 500);
        } catch (err) {
            setError(err.response?.data?.detail || "Authentication failed");
            toast.error(error);
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
                <div className="flex items-center mb-3">
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
                            className="w-full bg-gray-700 rounded p-2 text-white my-2"
                            data-testid="email-input"
                        />
                        
                        <PasswordField
                            password={password}
                            setPassword={setPassword}
                            label="Password"
                            id="password"
                            name="password"
                        />

                        {isSignUp && <ConfirmPasswordField confirmPassword={confirmPassword} setConfirmPassword={setConfirmPassword}/>}

                        {isSignUp && (
                        <div className="flex flex-col items-center mt-4">
                            <div className="flex flex-row items-center w-full max-w-md">
                                <div className="relative flex items-center">
                                    <input 
                                        type="checkbox" 
                                        id="ageVerification" 
                                        name="ageVerification"
                                        checked={isAgeVerified}
                                        onChange={(e) => setIsAgeVerified(e.target.checked)}
                                        required={isSignUp}
                                        className="peer absolute opacity-0 w-5 h-5 cursor-pointer"
                                    />
                                    <div className="w-5 h-5 border-2 border-yellow-400 rounded flex items-center justify-center peer-checked:bg-yellow-400 peer-checked:border-yellow-400 transition-colors">
                                        {isAgeVerified && <Check size={14} className="text-black" />}
                                    </div>
                                </div>
                                <div className="text-sm text-gray-400 ml-3 flex-1">
                                    <label htmlFor="ageVerification" className="cursor-pointer select-none">
                                        By checking this box, you confirm that you are over 21 years old and eligible to play at Fepsino.
                                    </label>
                                </div>
                            </div>
                        </div>
                        )}

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
