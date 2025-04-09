import React from "react";
import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { describe, test, beforeEach, expect } from "vitest";
import Home from "./Home";

describe("Home Component", () => {
    beforeEach(() => {
        localStorage.clear();
    });

    test("shows sign-in prompt when not authenticated", () => {
        render(
            <MemoryRouter>
                <Home />
            </MemoryRouter>
        );

        expect(screen.getByText(/sign in required/i)).toBeInTheDocument();
        expect(screen.getByText(/please sign in to access the games/i)).toBeInTheDocument();
        expect(screen.getByRole("button", { name: /sign in \/ sign up/i })).toBeInTheDocument();
    });

    test("displays game cards when authenticated", () => {
        localStorage.setItem("access_token", "mock-token");

        render(
            <MemoryRouter>
                <Home />
            </MemoryRouter>
        );

        expect(screen.getAllByText(/slot machines/i).length).toBeGreaterThan(0);
        expect(screen.getAllByText(/blackjack/i).length).toBeGreaterThan(0);
        expect(screen.getAllByText(/dice games/i).length).toBeGreaterThan(0);

        const playButtons = screen.getAllByRole("button", { name: /play now/i });
        expect(playButtons).toHaveLength(3);
    });

    test("matches snapshot when authenticated", () => {
        localStorage.setItem("access_token", "mock-token");

        const { asFragment } = render(
            <MemoryRouter>
                <Home />
            </MemoryRouter>
        );

        expect(asFragment()).toMatchSnapshot();
    });
});
