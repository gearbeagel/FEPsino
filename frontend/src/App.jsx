import {BrowserRouter as Router, Routes, Route, useLocation } from "react-router-dom";
import { AnimatePresence, motion } from "framer-motion";
import Home from "./components/Home";
import SlotsGame from "./components/games/SlotsGame";
import Header from "./components/Header";
import About from "./components/About";
import DiceGame from "./components/games/DiceGame.jsx";
import SignUpIn from "./components/user/SignUpIn.jsx";
import routerVariants from "./components/animations/RouterAnimations.jsx";
import "./App.css";
import Profile from "./components/user/Profile.jsx";
import BlackJackGame from "./components/games/BlackjackGame.jsx";

const withAnimation = (WrappedComponent) => {
    return function AnimatedComponent(props) {
        return (
            <motion.div
                variants={routerVariants}
                initial="hidden"
                animate="visible"
                exit="hidden"
                transition="transition"
            >
                <WrappedComponent {...props} />
            </motion.div>
        );
    };
};

const AnimatedHome = withAnimation(Home);
const AnimatedSlotsGame = withAnimation(SlotsGame);
const AnimatedBlackjack = withAnimation(BlackJackGame);
const AnimatedDiceGame = withAnimation(DiceGame);
const AnimatedAbout = withAnimation(About);
const AnimatedSignUpIn = withAnimation(SignUpIn);
const AnimatedProfile = withAnimation(Profile);

function AnimatedRoutes() {
    const location = useLocation();

    return (
        <AnimatePresence mode="wait">
            <Routes location={location} key={location.pathname}>
                <Route path="/" element={<AnimatedHome />} />
                <Route path="/slots" element={<AnimatedSlotsGame />} />
                <Route path="/blackjack" element={<AnimatedBlackjack />} />
                <Route path="/dice" element={<AnimatedDiceGame />} />
                <Route path="/about" element={<AnimatedAbout />} />
                <Route path="/signup" element={<AnimatedSignUpIn />} />
                <Route path="/profile" element={<AnimatedProfile />} />
            </Routes>
        </AnimatePresence>
    );
}

function App() {
    return (
        <Router>
            <div className="h-screen overflow-hidden bg-black text-white flex flex-col">
                <Header />
                <main className="flex-grow flex flex-col overflow-hidden bg-gradient-to-b from-gray-900 to-black pt-12 pb-4">
                    <AnimatedRoutes />
                </main>
            </div>
        </Router>
    );
}

export default App;