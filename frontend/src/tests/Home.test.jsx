// src/tests/Home.test.jsx
import React from "react";
import { render, screen } from "@testing-library/react";
import { fireEvent } from "@testing-library/dom";
import Home from "../components/Home";
import { MemoryRouter } from "react-router-dom";
import { describe, it, expect, beforeEach } from "vitest";

describe("Home component (with GameCards)", () => {
    beforeEach(() => {
        localStorage.clear();
    });

    function renderHome() {
        return render(
            <MemoryRouter>
                <Home />
            </MemoryRouter>
        );
    }

    it("renders welcome text and featured-games header", () => {
        renderHome();
        expect(screen.getByText("Welcome to FEPSino")).toBeInTheDocument();
        expect(screen.getByText("Our Featured Games")).toBeInTheDocument();
    });

    it("shows three game cards with correct titles and descriptions", () => {
        renderHome();
        // titles
        expect(screen.getByText("Slot Machines")).toBeInTheDocument();
        expect(screen.getByText("Blackjack")).toBeInTheDocument();
        expect(screen.getByText("Dice Games")).toBeInTheDocument();

        // descriptions (just check one to confirm)
        expect(
            screen.getByText(/Spin to win with our wide variety of themed slot machines\./i)
        ).toBeInTheDocument();
    });

    it("when not authenticated, buttons are disabled and links blocked", () => {
        renderHome();

        // Buttons read "Join us to play!" and are disabled
        const joinButtons = screen.getAllByRole("button", { name: /join us to play!/i });
        expect(joinButtons).toHaveLength(3);
        joinButtons.forEach((btn) => expect(btn).toBeDisabled());

        // Links should have the CSS class that blocks pointer-events
        const links = screen.getAllByRole("link");
        links.forEach((link) => {
            expect(link).toHaveClass("pointer-events-none");
        });
    });

    it("when authenticated, buttons are enabled and links work", () => {
        // simulate login
        localStorage.setItem("access_token", "dummy-token");
        renderHome();

        // Buttons read "Play Now" and are enabled
        const playButtons = screen.getAllByRole("button", { name: /play now/i });
        expect(playButtons).toHaveLength(3);
        playButtons.forEach((btn) => expect(btn).toBeEnabled());

        // Links should NOT have the blocking class
        const links = screen.getAllByRole("link");
        links.forEach((link) => {
            expect(link).not.toHaveClass("pointer-events-none");
        });
    });
});
