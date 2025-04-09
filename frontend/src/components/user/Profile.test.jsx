import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import Profile from './Profile';
import fetchUser from './UserApi.jsx';
import { describe, it, vi, beforeEach, expect, afterEach } from "vitest";

vi.mock('./UserApi.jsx');

const mockUser = {
    email: 'test@example.com',
    old_password: '',
    password: '',
    confirm_password: '',
};

describe('Profile Component', () => {
    beforeEach(() => {
        fetchUser.mockResolvedValue(mockUser);
        localStorage.setItem('access_token', 'mock-token');
    });

    afterEach(() => {
        vi.clearAllMocks();
    });

    it('renders the user email after fetch', async () => {
        render(<Profile />);
        const email = await screen.findByText(/test@example.com/i);
        expect(email).toBeInTheDocument();
    });

    it('toggles editing mode and shows form fields', async () => {
        render(<Profile />);
        const editBtn = await screen.findByRole('button', { name: /edit/i });
        fireEvent.click(editBtn);

        expect(screen.getByPlaceholderText("Old Password")).toBeInTheDocument();
        expect(screen.getByPlaceholderText("Password")).toBeInTheDocument();
        expect(screen.getByPlaceholderText("Confirm Password")).toBeInTheDocument();
    });

    it('updates input fields correctly', async () => {
        render(<Profile />);
        const editBtn = await screen.findByRole('button', { name: /edit/i });
        fireEvent.click(editBtn);

        const newPassword = screen.getByPlaceholderText("Password");
        fireEvent.change(newPassword, { target: { value: 'newpass123' } });

        expect(newPassword.value).toBe('newpass123');
    });

    it('sends PUT request when saving profile', async () => {
        global.fetch = vi.fn(() =>
            Promise.resolve({
                ok: true,
                json: () => Promise.resolve(mockUser),
            })
        );

        render(<Profile />);
        const editBtn = await screen.findByRole('button', { name: /edit/i });
        fireEvent.click(editBtn);

        const form = screen.getByTestId('edit-form');
        fireEvent.submit(form);

        await waitFor(() => {
            expect(global.fetch).toHaveBeenCalledWith(
                expect.stringContaining('/user/update/'),
                expect.objectContaining({
                    method: 'PUT',
                })
            );
        });
    });
});
