import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import Header from "../components/Header";
import { useAuth } from "../context/AuthContext";
import { MemoryRouter } from "react-router-dom";
import { describe, it, expect, vi } from "vitest";

vi.mock("../context/AuthContext", () => ({
    useAuth: vi.fn(),
}));

describe("Header component", () => {
    it("renders nothing while loading", () => {
        useAuth.mockReturnValue({ loading: true });
        const { container } = render(
            <MemoryRouter>
                <Header />
            </MemoryRouter>
        );
        expect(container.firstChild).toBeNull();
    });

    it("shows Login / Sign Up when not authenticated", () => {
        useAuth.mockReturnValue({ loading: false, isAuthenticated: false });
        render(
            <MemoryRouter>
                <Header />
            </MemoryRouter>
        );

        expect(screen.getByText(/login \/ sign up/i)).toBeInTheDocument();
        expect(screen.queryByRole("link", { name: /profile/i })).toBeNull();
    });

    it("shows Profile link when authenticated", () => {
        useAuth.mockReturnValue({ loading: false, isAuthenticated: true });
        render(
            <MemoryRouter>
                <Header />
            </MemoryRouter>
        );

        const profileLink = screen.getByRole("link", { name: "" });
        expect(profileLink).toHaveAttribute("href", "/profile");

        expect(screen.queryByText(/login \/ sign up/i)).toBeNull();
    });

    it("toggles mobile menu and shows Profile when authenticated", () => {
        useAuth.mockReturnValue({ loading: false, isAuthenticated: true });
        const { container } = render(
            <MemoryRouter>
                <Header />
            </MemoryRouter>
        );

        fireEvent.click(screen.getByRole("button"));
        expect(container.querySelector(".absolute.top-16")).toBeInTheDocument();

        const mobileProfile = container.querySelector('.absolute.top-16 a[href="/profile"]');
        expect(mobileProfile).toBeInTheDocument();

        fireEvent.click(mobileProfile);
        expect(container.querySelector(".absolute.top-16")).toBeNull();
    });
});
