import React from "react";
import { render, screen, fireEvent, waitFor, act } from "@testing-library/react";
import axios from "axios";
import { toast } from "react-toastify";
import { vi, describe, it, beforeEach, afterEach, expect } from "vitest";

const loginMock = vi.fn();
const navigateMock = vi.fn();


vi.mock("react-toastify", () => ({
    toast: {
        success: vi.fn(),
        error: vi.fn(),
    },
    ToastContainer: () => <div data-testid="toast-container" />,
}));

vi.mock("react-router-dom", async () => {
    const actual = await vi.importActual("react-router-dom");
    return {
        ...actual,
        useNavigate: () => navigateMock,
        MemoryRouter: actual.MemoryRouter,
    };
});

vi.mock("../context/AuthContext", () => ({
    useAuth: () => ({
        isAuthenticated: false,
        login: loginMock,
    }),
}));
import SignUpIn from "../components/user/SignUpIn";
import { MemoryRouter } from "react-router-dom";

function renderComponent() {
    return render(
        <MemoryRouter>
            <SignUpIn />
        </MemoryRouter>
    );
}

describe("SignUpIn component", () => {
    beforeEach(() => {
        vi.clearAllMocks();
        vi.spyOn(axios, "post");
    });

    afterEach(() => {
        vi.useRealTimers();
    });

    it("renders Sign up form by default", () => {
        renderComponent();
        expect(screen.getByTestId("auth-title")).toHaveTextContent("Sign up");
        expect(screen.getByTestId("email-input")).toBeInTheDocument();
        expect(screen.getByTestId("password-input")).toBeInTheDocument();
        expect(screen.getByLabelText(/confirm password/i)).toBeInTheDocument();
        expect(screen.getByTestId("auth-submit")).toHaveTextContent("Sign up");
    });

    it("toggles to Sign in form", () => {
        const { container } = renderComponent();
        const authFieldsPre = container.querySelectorAll('input[type="email"], input[type="password"]');
        expect(authFieldsPre).toHaveLength(3);

        fireEvent.click(screen.getByTestId("toggle-auth-form"));
        expect(screen.getByTestId("auth-title")).toHaveTextContent("Sign in");
    });

    it("shows error if fields are empty on submit", async () => {
        renderComponent();
        fireEvent.click(screen.getByTestId("auth-submit"));
        await waitFor(() =>
            expect(toast.error).toHaveBeenCalledWith("All fields are required!")
        );
    });

    it("shows error when passwords do not match", async () => {
        renderComponent();
        fireEvent.change(screen.getByTestId("email-input"), {
            target: { value: "a@a.com" },
        });
        fireEvent.change(screen.getByTestId("password-input"), {
            target: { value: "pass1" },
        });
        fireEvent.change(screen.getByLabelText(/confirm password/i), {
            target: { value: "pass2" },
        });
        fireEvent.click(screen.getByTestId("auth-submit"));
        await waitFor(() =>
            expect(toast.error).toHaveBeenCalledWith("Passwords do not match!")
        );
    });

    it("shows error when age not verified on sign up", async () => {
        renderComponent();
        fireEvent.change(screen.getByTestId("email-input"), {
            target: { value: "a@a.com" },
        });
        fireEvent.change(screen.getByTestId("password-input"), {
            target: { value: "pass1" },
        });
        fireEvent.change(screen.getByLabelText(/confirm password/i), {
            target: { value: "pass1" },
        });
        fireEvent.click(screen.getByTestId("auth-submit"));
        await waitFor(() =>
            expect(toast.error).toHaveBeenCalledWith(
                "You must be at least 21 years old to register!"
            )
        );
    });
});
