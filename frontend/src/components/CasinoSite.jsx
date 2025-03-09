import { Coins, Dice5, Club } from 'lucide-react';

export default function Homepage() {
  return (
    <div className="h-screen overflow-hidden bg-black text-white flex flex-col">
      <header className="bg-gray-900 p-4">
        <div className="container mx-auto flex items-center justify-between">
          <h1 className="text-2xl font-bold text-yellow-400">FEPSino</h1>
          <nav className="hidden md:block">
            <ul className="flex space-x-4">
              <li>
                <a href="#" className="hover:text-yellow-400">
                  Home
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-yellow-400">
                  Games
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-yellow-400">
                  Promotions
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-yellow-400">
                  About
                </a>
              </li>
            </ul>
          </nav>
          <button className="border border-yellow-400 bg-yellow-400 text-black px-4 py-2 rounded hover:bg-yellow-500 transition-colors">
            Login / Sign Up
          </button>
        </div>
      </header>

      <main className="flex-grow flex flex-col overflow-hidden">
        {/* Gradient background div */}
        <div className="bg-gradient-to-b from-gray-900 to-black py-12"></div>
        
        {/* Welcome section with reduced margins */}
        <section className="flex-none flex items-center justify-center">
          <div className="container mx-auto text-center">
            <h2 className="text-4xl md:text-6xl font-bold my-4">Welcome to FEPSino</h2>
            <p className="text-xl mb-1">Experience the thrill of our exclusive games.</p>
          </div>
        </section>

        {/* Games section */}
        <section className="flex-grow flex items-center justify-center mt-2">
          <div className="container mx-auto">
            <h2 className="text-3xl font-bold mb-4 text-center">Our Featured Games</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <GameCard
                title="Slot Machines"
                description="Spin to win with our wide variety of themed slot machines."
                icon={<Coins className="h-12 w-12 text-yellow-400" />}
              />
              <GameCard
                title="Blackjack"
                description="Test your skills against our dealers in this classic card game."
                icon={<Club className="h-12 w-12 text-yellow-400" />}
              />
              <GameCard
                title="Dice Games"
                description="Roll the dice and try your luck with our exciting dice games."
                icon={<Dice5 className="h-12 w-12 text-yellow-400" />}
              />
            </div>
          </div>
        </section>
      </main>

      <footer>
        <div className="bg-gradient-to-b from-black to-gray-900 py-12"></div>
        <div className="bg-gray-900 py-4">
          <div className="container mx-auto text-center">
            <p>&copy; 2025 FEPSino. All rights reserved.</p>
            <p className="text-sm text-gray-400">Please gamble responsibly. 18+</p>
          </div>
        </div>
      </footer>
    </div>
  );
}

function GameCard({ title, description, icon }) {
  return (
    <div className="bg-gray-800 border border-yellow-400 rounded-lg p-6 text-center">
      <div className="flex items-center justify-center text-2xl font-bold text-yellow-400">
        {icon}
        <span className="ml-2">{title}</span>
      </div>
      <p className="text-gray-300 mt-4">{description}</p>
      <button className="bg-yellow-400 text-black hover:bg-yellow-500 px-6 py-2 rounded mt-4 transition-colors">
        Play Now
      </button>
    </div>
  );
}