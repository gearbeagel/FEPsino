import { render, screen } from "@testing-library/react";
import About from "../components/About";
import React from "react";
import { describe, it, expect } from "vitest";

describe("About component", () => {
    it("renders About FEPSino section", () => {
        render(<About />);
        expect(screen.getByText("About FEPSino")).toBeInTheDocument();
        expect(
            screen.getByText(/FEPSino is a modern online casino/i)
        ).toBeInTheDocument();
    });

    it("renders Our Games section with all game titles", () => {
        render(<About />);
        expect(screen.getByText("Our Games")).toBeInTheDocument();
        expect(screen.getByText("Slot Machines")).toBeInTheDocument();
        expect(screen.getByText("Blackjack")).toBeInTheDocument();
        expect(screen.getByText("Dice Games")).toBeInTheDocument();
    });

    it("renders Technology Stack section with subsections", () => {
        render(<About />);
        expect(screen.getByText("Technology Stack")).toBeInTheDocument();
        expect(screen.getByText("Frontend")).toBeInTheDocument();
        expect(screen.getByText("Backend")).toBeInTheDocument();
        expect(screen.getByText("Github Repository Link")).toBeInTheDocument();
    });

    it("includes the GitHub repo link", () => {
        render(<About />);
        const link = screen.getByRole("link", { name: /check us out on github/i });
        expect(link).toHaveAttribute("href", "https://github.com/gearbeagel/FEPsino");
    });

    it("renders team members correctly", () => {
        render(<About />);
        expect(screen.getByText("Gamblers (Team Members)")).toBeInTheDocument();
        expect(screen.getByText(/Vic. Kondratska/)).toBeInTheDocument();
        expect(screen.getByText(/Nik. Pashchuk/)).toBeInTheDocument();
        expect(screen.getByText(/Dmy. Bilyk/)).toBeInTheDocument();
    });
});
