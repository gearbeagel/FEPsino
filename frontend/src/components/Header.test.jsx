import { render, screen, waitFor } from '@testing-library/react';
import { describe, it, vi, beforeEach, expect } from 'vitest';
import Header from './Header';
import fetchUser from './user/UserApi.jsx';
import { MemoryRouter } from 'react-router-dom';
import React from 'react';

vi.mock('./user/UserApi.jsx');

describe('Header Component', () => {
    beforeEach(() => {
        vi.resetAllMocks();
    });

    it('renders the site title', async () => {
        fetchUser.mockResolvedValue(null);
        render(<Header />, { wrapper: MemoryRouter });

        await waitFor(() => {
            expect(screen.getByText(/FEPSino/i)).toBeInTheDocument();
        });
    });

    it('shows Login / Sign Up button if user not logged in', async () => {
        fetchUser.mockResolvedValue(null);

        render(<Header />, { wrapper: MemoryRouter });

        await waitFor(() => {
            expect(screen.getByText(/Login \/ Sign Up/i)).toBeInTheDocument();
        });
    });

    it('shows user email when logged in', async () => {
        const mockUser = { email: 'test@example.com' };
        fetchUser.mockResolvedValue(mockUser);

        render(<Header />, { wrapper: MemoryRouter });

        await waitFor(() => {
            expect(screen.getByText(mockUser.email)).toBeInTheDocument();
        });
    });

    it('renders About link', async () => {
        fetchUser.mockResolvedValue(null);

        render(<Header />, { wrapper: MemoryRouter });

        await waitFor(() => {
            expect(screen.getByText(/About/i)).toBeInTheDocument();
        });
    });
});
