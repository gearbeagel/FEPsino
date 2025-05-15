import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import UserProfileInfo from '../components/user/profileUtils/UserProfileInfo.jsx';
import { DollarSign, Mail, Pencil, User2, User } from 'lucide-react';
import { vi, describe, expect } from 'vitest';

describe('UserProfileInfo', () => {
    const user = {
        username: 'alice',
        user: { email: 'a@b.com' },
        balance: '123.45',
    };
    const onEdit = vi.fn();
    const onNewTxn = vi.fn();
    const onLogout = vi.fn();

    it('displays username, email, and balance', () => {
        render(
            <UserProfileInfo
                user={user}
                onEditProfile={onEdit}
                onNewTransaction={onNewTxn}
                onLogout={onLogout}
            />
        );
        expect(screen.getByText("alice's profile")).toBeInTheDocument();
        expect(screen.getByText('a@b.com')).toBeInTheDocument();
        expect(screen.getByText('$123.45')).toBeInTheDocument();
    });

    it('buttons call callbacks', () => {
        render(
            <UserProfileInfo
                user={user}
                onEditProfile={onEdit}
                onNewTransaction={onNewTxn}
                onLogout={onLogout}
            />
        );
        fireEvent.click(screen.getByRole('button', { name: /Edit Profile/i }));
        expect(onEdit).toHaveBeenCalled();
        fireEvent.click(screen.getByRole('button', { name: /New Transaction/i }));
        expect(onNewTxn).toHaveBeenCalled();
        fireEvent.click(screen.getByRole('button', { name: /Log out/i }));
        expect(onLogout).toHaveBeenCalled();
    });
});
