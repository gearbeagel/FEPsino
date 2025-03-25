import { BrowserRouter as Router, Routes, Route, useLocation } from "react-router-dom";
import { CSSTransition, TransitionGroup } from "react-transition-group";
import { useRef } from "react";
import Home from "./components/Home";
import SlotsGame from "./components/games/SlotsGame";
import Header from "./components/Header";
import About from "./components/About";
import Blackjack from "./components/games/BlackjackGame";
import DiceGame from "./components/games/DiceGame.jsx";
import SignUpIn from "./components/user/SignUpIn.jsx";
import "./App.css";

function AnimatedRoutes() {
  const location = useLocation();
  const nodeRef = useRef(null);

  return (
      <TransitionGroup className="flex-grow relative overflow-hidden">
        <CSSTransition
            key={location.pathname}
            nodeRef={nodeRef}
            timeout={200}
            classNames="fade"
            unmountOnExit
            onEntering={() => { document.body.style.overflow = "auto"; }}
            onExiting={() => { document.body.style.animation = "none"; }}
        >
          <div ref={nodeRef} className="absolute w-full">
            <Routes location={location}>
              <Route path="/" element={<Home />} />
              <Route path="/slots" element={<SlotsGame />} />
              <Route path="/blackjack" element={<Blackjack />} />
              <Route path="/dice" element={<DiceGame />} />
              <Route path="/profile" element={<h1>Profile</h1>} />
              <Route path="/about" element={<About />} />
              <Route path="/signup" element={<SignUpIn />} />
            </Routes>
          </div>
        </CSSTransition>
      </TransitionGroup>
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
