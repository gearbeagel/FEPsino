import React from 'react';
import { render, screen, fireEvent, waitFor, within } from '@testing-library/react';
import Profile from '../components/user/Profile.jsx';
import fetchUser from '../components/user/UserApi.jsx';
import { describe, it, vi, beforeEach, afterEach, expect } from 'vitest';

// 1) Mock the default export of UserApi.jsx
vi.mock('../components/user/UserApi.jsx', () => ({
    default: vi.fn(),
}));

vi.mock('../components/user/UserApi.jsx', () => ({
    default: vi.fn(),
}));

describe('Profile Component', () => {
    const mockUser = {
        email: 'test@example.com',
        old_password: '',
        password: '',
        confirm_password: '',
    };

    beforeEach(() => {
        fetchUser.mockResolvedValue(mockUser);
        // stub localStorage.getItem for Authorization header
        vi.spyOn(Storage.prototype, 'getItem').mockReturnValue('mock-token');
    });

    afterEach(() => {
        vi.clearAllMocks();
    });

    it('shows user email after fetch', async () => {
        render(<Profile />);
        // email
        expect(await screen.findByText(mockUser.email)).toBeInTheDocument();
    });

    it('toggles into edit mode and renders all three password inputs', async () => {
        render(<Profile />);
        // click "Edit"
        const editBtn = await screen.findByRole('button', { name: /edit/i });
        fireEvent.click(editBtn);

        // form appears
        const form = screen.getByTestId('edit-form');
        expect(form).toBeInTheDocument();

        // three placeholders: Old Password, Password, Confirm Password
        const inputs = within(form).getAllByPlaceholderText(/password/i);
        expect(inputs).toHaveLength(3);
        expect(inputs[0]).toHaveAttribute('placeholder', 'Old Password');
        expect(inputs[1]).toHaveAttribute('placeholder', 'Password');
        expect(inputs[2]).toHaveAttribute('placeholder', 'Confirm Password');
    });

    it('allows you to type into the new‐password field', async () => {
        render(<Profile />);
        fireEvent.click(await screen.findByRole('button', { name: /edit/i }));
        const [, newPassInput] = screen.getAllByPlaceholderText(/password/i);
        fireEvent.change(newPassInput, { target: { value: 'newsecret' } });
        expect(newPassInput).toHaveValue('newsecret');
    });

    it('submits a PUT request when the form is submitted', async () => {
        // mock global.fetch for the update call
        global.fetch = vi.fn(() =>
            Promise.resolve({
                ok: true,
                json: () => Promise.resolve(mockUser),
            })
        );

        render(<Profile />);
        fireEvent.click(await screen.findByRole('button', { name: /edit/i }));

        const [oldInput, newInput, confirmInput] = screen.getAllByPlaceholderText(/password/i);
        fireEvent.change(oldInput,    { target: { value: 'oldpass' } });
        fireEvent.change(newInput,    { target: { value: 'newpass' } });
        fireEvent.change(confirmInput,{ target: { value: 'newpass' } });

        // submit the form
        fireEvent.submit(screen.getByTestId('edit-form'));

        await waitFor(() => {
            expect(global.fetch).toHaveBeenCalledWith(
                expect.stringContaining('/user/update/'),
                expect.objectContaining({ method: 'PUT' })
            );
        });
    });
});