import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import About from "../components/About.jsx";
import React from "react";

describe("About Component", () => {
    it("renders the about section title and description", () => {
        render(<About />);

        expect(
            screen.getByRole("heading", { name: /about fepsino/i })
        ).toBeInTheDocument();

        expect(
            screen.getByText(/fepsino is a fictional online casino/i)
        ).toBeInTheDocument();
    });

    it("renders the creator list", () => {
        render(<About />);

        expect(screen.getByRole("heading", { name: /created by:/i })).toBeInTheDocument();

        const names = [
            "Vic. Kondratska: Team Lead, Frontend Developer",
            "Nik. Pashchuk: Backend Developer",
            "Vol. Demchyshyn: Backend Developer",
            "Mar. Husak: Backend Developer",
            "Dmy. Bilyk: Backend Developer",
        ];

        names.forEach(name => {
            expect(screen.getByText(name)).toBeInTheDocument();
        });
    });
});
