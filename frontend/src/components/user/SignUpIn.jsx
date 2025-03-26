import React, {useState} from "react";
import {User} from "lucide-react";
import {AnimatePresence, motion} from "framer-motion";
import formVariants from "../animations/FormAnimations";

export default function SignUpIn() {
    const [isSignUp, setIsSignUp] = useState(true);
    const toggleForm = () => setIsSignUp(!isSignUp);

    const googleIcon = () => {
        return (
            <svg className="h-5 w-5 mr-2" viewBox="0 0 48 48">
                <path
                    fill="black"
                    d="M24 9.5c3.9 0 7.1 1.3 9.5 3.4l7-7C35.8 2.5 30.2 0 24 0 14.6 0 6.6 5.4 2.6 13.3l8.2 6.4C12.6 13.1 17.8 9.5 24 9.5z"
                />
                <path
                    fill="black"
                    d="M46.5 24c0-1.6-.1-3.1-.4-4.5H24v9h12.7c-.6 3.1-2.4 5.7-4.9 7.4l7.5 5.8c4.4-4.1 7.2-10.1 7.2-17.7z"
                />
                <path
                    fill="black"
                    d="M10.8 28.7c-1.1-3.1-1.1-6.5 0-9.6L2.6 13.3C-1.1 20.1-1.1 27.9 2.6 34.7l8.2-6z"
                />
                <path
                    fill="black"
                    d="M24 48c6.2 0 11.4-2.1 15.2-5.7l-7.5-5.8c-2.1 1.4-4.8 2.3-7.7 2.3-6.2 0-11.5-4.2-13.4-10.1l-8.2 6.4C6.6 42.6 14.6 48 24 48z"
                />
            </svg>
        );
    }

    return (
        <div className="flex-grow flex flex-col items-center p-6">
            <motion.div
                className="container max-w-4xl bg-slate-900 border border-yellow-400 rounded-lg p-6 shadow-xl w-full overflow-hidden"
                initial={{height: "auto"}}
                animate={{height: "auto"}}
                transition={{duration: 0.5, ease: "easeInOut"}}
            >
                <div className="flex items-center">
                    <User className="h-6 w-6 text-yellow-400 mr-2"/>
                    <span className="text-xl text-yellow-400">
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
                        {isSignUp ? (
                            <>
                                <div className="text-sm my-3">Email:</div>
                                <input type="text" className="w-full bg-gray-700 rounded p-2 text-white"/>
                                <div className="text-sm my-3">Password:</div>
                                <input type="password" className="w-full bg-gray-700 rounded p-2 text-white"/>
                                <div className="text-sm my-3">Confirm Password:</div>
                                <input type="password" className="w-full bg-gray-700 rounded p-2 text-white"/>

                                <div className="flex flex-col items-center">
                                    <div className="text-sm text-gray-400 mt-4">
                                        Already have an account?{" "}
                                        <button onClick={toggleForm} className="text-yellow-400">
                                            Sign in
                                        </button>
                                    </div>
                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                        <button
                                            className="bg-yellow-400 text-black hover:bg-yellow-500 px-6 py-2 rounded mt-4 transition-colors w-75 flex items-center justify-center">
                                            Sign in
                                        </button>
                                        <button
                                            className="bg-yellow-400 text-black hover:bg-yellow-500 px-6 py-2 rounded mt-4 transition-colors w-75 flex items-center justify-center">
                                            {googleIcon()} Sign in with Google
                                        </button>
                                    </div>
                                </div>
                            </>
                        ) : (
                            <>
                                <div className="text-sm my-3">Email:</div>
                                <input type="text" className="w-full bg-gray-700 rounded p-2 text-white"/>
                                <div className="text-sm my-3">Password:</div>
                                <input type="password" className="w-full bg-gray-700 rounded p-2 text-white"/>

                                <div className="flex flex-col items-center">
                                    <div className="text-sm text-gray-400 mt-4">
                                        Don't have an account?{" "}
                                        <button onClick={toggleForm} className="text-yellow-400">
                                            Sign up
                                        </button>
                                    </div>
                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                        <button
                                            className="bg-yellow-400 text-black hover:bg-yellow-500 px-6 py-2 rounded mt-4 transition-colors w-75 flex items-center justify-center">
                                            Sign in
                                        </button>
                                        <button
                                            className="bg-yellow-400 text-black hover:bg-yellow-500 px-6 py-2 rounded mt-4 transition-colors w-75 flex items-center justify-center">
                                            {googleIcon()} Sign in with Google
                                        </button>
                                    </div>
                                </div>
                            </>
                        )}
                    </motion.div>
                </AnimatePresence>
            </motion.div>
        </div>
    );
}