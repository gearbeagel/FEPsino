import React from "react";
import { Coins, Dice5, Club, User } from "lucide-react";
import { Link } from "react-router-dom";
import PropTypes from 'prop-types';

function GameCard({ title, description, icon, link, isAuthenticated }) {
    return (
        <div className="bg-slate-900 border border-yellow-400 rounded-lg p-6 text-center">
            <div className="flex items-center justify-center text-2xl font-bold text-yellow-400">
                {icon}
                <span className="ml-2">{title}</span>
            </div>
            <p className="text-gray-300 mt-4">{description}</p>
            <Link
                to={link}
                onClick={(e) => !isAuthenticated && e.preventDefault()}
                className={!isAuthenticated ? 'pointer-events-none' : ''}
            >
                <button
                disabled={!isAuthenticated}
                    className="bg-yellow-400 text-black hover:bg-yellow-500 disabled:bg-slate-600 px-6 py-2 rounded mt-4 transition-colors">
                    {isAuthenticated ? "Play Now" : "Join us to play!"}
                </button>
            </Link>
        </div>
    );
}

GameCard.propTypes = {
    title: PropTypes.string.isRequired,
    description: PropTypes.string.isRequired,
    icon: PropTypes.string.isRequired,
    link: PropTypes.string.isRequired,
    isAuthenticated: PropTypes.bool.isRequired,
};


export default function Home() {
    const isAuthenticated = localStorage.getItem("access_token") !== null;

    return (
        <div className="flex flex-col">
            <section className="flex-none flex items-center justify-center">
                <div className="container mx-auto text-center">
                    <h2 className="text-4xl md:text-6xl font-bold my-4">
                        Welcome to FEPSino
                    </h2>
                    <p className="text-xl mb-1">
                        Experience the thrill of our exclusive games.
                    </p>
                </div>
            </section>

            <section className="flex-grow flex items-center justify-center sm:mt-2 md:mt-16 sm:p-6 sm:pt-40 md:p-0 overflow-y-auto">
                <div className="container mx-auto">
                    <h2 className="text-3xl font-bold mb-4 text-center">
                        Our Featured Games
                    </h2>
                            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                                <GameCard
                                    title="Slot Machines"
                                    description="Spin to win with our wide variety of themed slot machines."
                                    icon={<Coins className="h-12 w-12 text-yellow-400" />}
                                    link="/slots"
                                    isAuthenticated={isAuthenticated}
                                />
                                <GameCard
                                    title="Blackjack"
                                    description="Test your skills against our dealers in this classic card game."
                                    icon={<Club className="h-12 w-12 text-yellow-400" />}
                                    link="/blackjack"
                                    isAuthenticated={isAuthenticated}
                                />
                                <GameCard
                                    title="Dice Games"
                                    description="Roll the dice and try your luck with our exciting dice games."
                                    icon={<Dice5 className="h-12 w-12 text-yellow-400" />}
                                    link="/dice"
                                    isAuthenticated={isAuthenticated}
                                />
                            </div>
                </div>
            </section>
        </div>
    );
}