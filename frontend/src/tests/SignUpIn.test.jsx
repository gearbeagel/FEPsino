import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { describe, it, vi, beforeEach, expect } from "vitest";
import "@testing-library/jest-dom";
import SignUpIn from "../components/user/SignUpIn.jsx";
import { BrowserRouter } from "react-router-dom";
import { ToastContainer } from "react-toastify";

vi.mock("react-router-dom", async () => {
    const actual = await vi.importActual("react-router-dom");
    return {
        ...actual,
        useNavigate: () => vi.fn(),
    };
});

vi.mock("axios");

beforeEach(() => {
    localStorage.clear();
    vi.stubGlobal("location", {
        ...window.location,
        reload: vi.fn(),
    });
});

const renderWithRouter = (ui) => {
    return render(
        <BrowserRouter>
            {ui}
            <ToastContainer />
        </BrowserRouter>
    );
};

describe("SignUpIn component", () => {
    beforeEach(() => {
        localStorage.clear();
        vi.resetAllMocks();
    });

    it("renders sign-up form initially", () => {
        renderWithRouter(<SignUpIn/>);
        const header = screen.getByText((content, el) => {
            return el.tagName.toLowerCase() === "span" && content === "Sign up";
        });
        expect(header).toBeInTheDocument();

        const button = screen.getByRole("button", {name: "Sign up"});
        expect(button).toBeInTheDocument();
    });

    it("toggles to sign-in form", () => {
        renderWithRouter(<SignUpIn/>);
        const toggleButton = screen.getByRole("button", {name: "Sign in"});
        fireEvent.click(toggleButton);

        const header = screen.getByText((content, el) => {
            return el.tagName.toLowerCase() === "span" && content === "Sign in";
        });
        expect(header).toBeInTheDocument();
    });

    it("shows error when required fields are missing", async () => {
        renderWithRouter(<SignUpIn/>);
        const submitButton = screen.getByRole("button", {name: "Sign up"});
        fireEvent.click(submitButton);

        await waitFor(() => {
            expect(screen.getByText("All fields are required!")).toBeInTheDocument();
        });
    });

    it("shows error when passwords don't match during sign up", async () => {
        renderWithRouter(<SignUpIn/>);
        fireEvent.change(screen.getByLabelText("Email:"), {
            target: {value: "user@example.com"},
        });
        fireEvent.change(screen.getByLabelText("Password:"), {
            target: {value: "password123"},
        });
        fireEvent.change(screen.getByLabelText("Confirm Password:"), {
            target: {value: "differentpass"},
        });
        const submitButton = screen.getByRole("button", {name: "Sign up"});
        fireEvent.click(submitButton);

        await waitFor(() => {
            expect(screen.getByText("Passwords do not match!")).toBeInTheDocument();
        });
    });
});
