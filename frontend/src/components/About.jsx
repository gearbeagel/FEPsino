import React from "react";

export default function About() {
  return (
   <div className="container max-w-4xl mx-auto">
      <div className="bg-slate-900 border border-yellow-400 rounded-lg p-6">
        <h1 className="text-3xl font-bold mb-4">About FEPSino</h1>
        <p className="text-lg text-gray-400">
          FEPSino is a fictional online casino that offers a variety of games
          for entertainment purposes.
        </p>
      </div>
      <div className="bg-slate-900 border border-yellow-400 rounded-lg p-6 mt-8">
        <h1 className="text-3xl font-bold mb-4">Created by:</h1>
        <ul className="text-lg text-gray-400">
          <li>Vic. Kondratska: Team Lead, Frontend Developer</li>
          <li>Nik. Pashchuk: Backend Developer</li>
          <li>Vol. Demchyshyn: Backend Developer</li>
          <li>Mar. Husak: Backend Developer</li>
          <li>Dmy. Bilyk: Backend Developer</li>
        </ul>
      </div>
    </div>
  );
}
