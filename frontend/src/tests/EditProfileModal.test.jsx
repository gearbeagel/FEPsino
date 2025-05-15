import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import EditProfileModal from '../components/user/profileUtils/EditProfileModal.jsx';
import { vi, describe, beforeEach, it, expect } from 'vitest';
import { toast } from 'react-toastify';

vi.mock('react-toastify', () => ({
    toast: {
        error: vi.fn(),
    },
    ToastContainer: () => <div data-testid="toast-container" />,
}));

describe('EditProfileModal', () => {
    const onClose = vi.fn();
    const onSubmit = vi.fn();
    const baseUser = { user: { email: 'a@b.com' }, username: 'alice' };

    beforeEach(() => {
        vi.clearAllMocks();
    });

    it('does not render when show=false', () => {
        render(
            <EditProfileModal
                show={false}
                onClose={onClose}
                onSubmit={onSubmit}
                userData={baseUser}
            />
        );
        expect(screen.queryByRole('form')).toBeNull();
    });

    it('renders email section by default and prefills fields', () => {
        render(
            <EditProfileModal
                show={true}
                onClose={onClose}
                onSubmit={onSubmit}
                userData={baseUser}
            />
        );
        const emailInput = screen.getByPlaceholderText('New Email');
        expect(emailInput).toHaveValue('a@b.com');
        fireEvent.click(screen.getByText('Username'));
        expect(screen.getByPlaceholderText('New Username')).toHaveValue('alice');
    });

    it('password validation: old===new triggers toast.error', () => {
        render(
            <EditProfileModal
                show={true}
                onClose={onClose}
                onSubmit={onSubmit}
                userData={baseUser}
            />
        );
        fireEvent.click(screen.getByText('Password'));
        fireEvent.change(screen.getByPlaceholderText('Old Password'), {
            target: { value: '1234' },
        });
        fireEvent.change(screen.getByPlaceholderText('New Password'), {
            target: { value: '1234' },
        });
        fireEvent.change(screen.getByPlaceholderText('Confirm Password'), {
            target: { value: '1234' },
        });
        fireEvent.click(screen.getByText('Save'));
        expect(toast.error).toHaveBeenCalledWith(
            'New password must be different from the current password'
        );
    });

    it('password mismatch triggers toast.error', () => {
        render(
            <EditProfileModal
                show={true}
                onClose={onClose}
                onSubmit={onSubmit}
                userData={baseUser}
            />
        );
        fireEvent.click(screen.getByText('Password'));
        fireEvent.change(screen.getByPlaceholderText('Old Password'), {
            target: { value: 'oldpass' },
        });
        fireEvent.change(screen.getByPlaceholderText('New Password'), {
            target: { value: 'newpass1' },
        });
        fireEvent.change(screen.getByPlaceholderText('Confirm Password'), {
            target: { value: 'newpass2' },
        });
        fireEvent.click(screen.getByText('Save'));
        expect(toast.error).toHaveBeenCalledWith('New passwords do not match');
    });

    it('valid submission calls onSubmit with editData', () => {
        render(
            <EditProfileModal
                show={true}
                onClose={onClose}
                onSubmit={onSubmit}
                userData={baseUser}
            />
        );
        fireEvent.change(screen.getByPlaceholderText('New Email'), {
            target: { value: 'new@domain.com' },
        });
        fireEvent.click(screen.getByText('Save'));
        expect(onSubmit).toHaveBeenCalledWith(
            expect.objectContaining({ email: 'new@domain.com' })
        );
    });
});