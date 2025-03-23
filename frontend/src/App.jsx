import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./components/Home";
import SlotsGame from "./components/games/SlotsGame";
import "./App.css";
import Header from "./components/Header";
import Footer from "./components/Footer";
import About from "./components/About";
import Blackjack from "./components/games/BlackjackGame";
import DiceGame from "./components/games/DiceGame.jsx";

function App() {
  return (
    <Router>
    <div className="h-screen overflow-hidden bg-black text-white flex flex-col">
      <Header />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/slots" element={<SlotsGame />} />
          <Route path="/blackjack" element={<Blackjack />} />
          <Route path="/dice" element={<DiceGame />} />
          <Route path="/profile" element={<h1>Profile</h1>} />
          <Route path="/about" element={<About />} />
        </Routes>
      <Footer />
    </div>
    </Router>
  );
}

export default App;
