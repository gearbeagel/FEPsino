import React from "react";
import { Coins, Dice5, Club, Code, Users, SquareChartGantt, SquareChevronRight, FolderCode, Gamepad, Info } from "lucide-react";

export default function About() {
  return (
    <div className="container max-w-6xl mx-auto p-4">
      <div className="grid md:grid-cols-2 gap-6">
        <div className="space-y-6">
          <div className="bg-slate-900 border border-yellow-400 rounded-lg p-6 h-max">
          <div className="flex items-center mb-4">
          <Info className="h-6 w-6 text-yellow-400 mr-2" />
            <h2 className="text-2xl font-bold text-yellow-400">About FEPSino</h2>
            </div>
            <p className="text-lg text-gray-300 mb-4">
              FEPSino is a modern online casino platform that offers an exciting gaming experience
              with a variety of classic casino games.
            </p>
          </div>

          <div className="bg-slate-900 border border-yellow-400 rounded-lg p-6 h-max">
          <div className="flex items-center mb-4">
          <Gamepad className="h-6 w-6 text-yellow-400 mr-2" />
            <h2 className="text-2xl font-bold text-yellow-400">Our Games</h2>
            </div>
            <div className="space-y-4">
              <div className="bg-slate-800 p-4 rounded-lg">
                <div className="flex items-center mb-2">
                  <Coins className="h-6 w-6 text-yellow-400 mr-2" />
                  <h3 className="font-bold text-yellow-400">Slot Machines</h3>
                </div>
                <p className="text-gray-300 text-sm">
                  Experience the thrill of our modern slot machines with multiple paylines
                  and exciting bonus features. Match symbols to win big!
                </p>
              </div>
              <div className="bg-slate-800 p-4 rounded-lg">
                <div className="flex items-center mb-2">
                  <Club className="h-6 w-6 text-yellow-400 mr-2" />
                  <h3 className="font-bold text-yellow-400">Blackjack</h3>
                </div>
                <p className="text-gray-300 text-sm">
                  Test your skills in this classic card game. Beat the dealer by getting
                  closer to 21 without going over. Perfect for strategic players!
                </p>
              </div>
              <div className="bg-slate-800 p-4 rounded-lg">
                <div className="flex items-center mb-2">
                  <Dice5 className="h-6 w-6 text-yellow-400 mr-2" />
                  <h3 className="font-bold text-yellow-400">Dice Games</h3>
                </div>
                <p className="text-gray-300 text-sm">
                  Roll the dice and test your luck! Choose from different dice types
                  and bet on your favorite numbers. Simple yet exciting!
                </p>
              </div>
            </div>
          </div>
        </div>

        <div className="space-y-6">
          <div className="bg-slate-900 border border-yellow-400 rounded-lg p-6 h-max">
          <div className="flex items-center mb-4">
          <Code className="h-6 w-6 text-yellow-400 mr-2" />
            <h2 className="text-2xl font-bold text-yellow-400">Technology Stack</h2>
            </div>
            <div className="space-y-4">
              <div className="bg-slate-800 p-4 rounded-lg">
                <div className="flex items-center mb-2">
                <SquareChartGantt className="h-6 w-6 text-yellow-400 mr-2" />
                  <h3 className="font-bold text-yellow-400">Frontend</h3>
                </div>
                <p className="text-gray-300 text-sm cursor-pointer">React.js, Tailwind CSS, Lucide Icons</p>
              </div>
              <div className="bg-slate-800 p-4 rounded-lg">
                <div className="flex items-center mb-2">
                  <SquareChevronRight className="h-6 w-6 text-yellow-400 mr-2" />
                  <h3 className="font-bold text-yellow-400">Backend</h3>
                </div>
                <p className="text-gray-300 text-sm cursor-pointer">Django REST Framework, PostgreSQL</p>
              </div>
              <div className="bg-slate-800 p-4 rounded-lg">
                <div className="flex items-center mb-2">
                  <FolderCode className="h-6 w-6 text-yellow-400 mr-2" />
                  <h3 className="font-bold text-yellow-400">Github Repository Link</h3>
                </div>
                <a href='https://github.com/gearbeagel/FEPsino'>
                <p className="text-gray-300 text-sm cursor-pointer">
                  Check us out on Github :D
                </p>
                </a>
              </div>
            </div>
          </div>

          <div className="bg-slate-900 border border-yellow-400 rounded-lg p-6 h-max">
            <div className="flex items-center mb-4">
              <Users className="h-6 w-6 text-yellow-400 mr-2" />
              <h2 className="text-2xl font-bold text-yellow-400">Gamblers (Team Members)</h2>
            </div>
            <div className="space-y-4">
              <div className="bg-slate-800 p-4 rounded-lg">
                <ul className="text-gray-300 text-sm space-y-2">
                  <li>Vic. Kondratska — Team Lead, Developer</li>
                  <li>Nik. Pashchuk — Tech Lead, Developer</li>
                  <li>Vol. Demchyshyn — Developer</li>
                  <li>Mar. Husak — Developer</li>
                  <li>Dmy. Bilyk — Developer</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
