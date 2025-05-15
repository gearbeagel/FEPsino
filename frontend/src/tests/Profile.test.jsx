import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import Profile from '../components/user/Profile.jsx';
import axios from 'axios';
import { vi } from 'vitest';
import { BrowserRouter } from 'react-router-dom';
import * as authModule from '../context/AuthContext.jsx';

vi.mock('axios');

vi.mock('react-router-dom', async () => {
    const actual = await vi.importActual('react-router-dom');
    return {
        ...actual,
        useNavigate: () => vi.fn()
    };
});

vi.mock(
    '../components/user/profileUtils/UserProfileInfo.jsx',
    () => ({
        default: ({ user }) => (
            <div data-testid="UserProfileInfo">stub: {JSON.stringify(user)}</div>
        )
    })
);
vi.mock(
    '../components/user/profileUtils/TransactionTable.jsx',
    () => ({ default: () => <div data-testid="TransactionTable" /> })
);
vi.mock(
    '../components/user/profileUtils/TransactionModal.jsx',
    () => ({ default: () => <div data-testid="TransactionModal" /> })
);
vi.mock(
    '../components/user/profileUtils/EditProfileModal.jsx',
    () => ({ default: () => <div data-testid="EditProfileModal" /> })
);

describe('Profile component', () => {
    const mockUser = { foo: 'bar' };
    const mockTxns = [{ id: 1 }];

    beforeEach(() => {
        vi.spyOn(authModule, 'useAuth').mockReturnValue({
            logout: vi.fn()
        });

        axios.get.mockImplementation((url) => {
            if (url.endsWith('/user/profile/')) {
                return Promise.resolve({ data: mockUser });
            }
            if (url.endsWith('/user/transaction/')) {
                return Promise.resolve({ data: mockTxns });
            }
            return Promise.reject(new Error('unexpected GET ' + url));
        });
    });

    afterEach(() => {
        vi.clearAllMocks();
    });

    test('renders Profile and child stubs once data loads', async () => {
        render(
            <BrowserRouter>
                <Profile />
            </BrowserRouter>
        );

        await waitFor(() =>
            expect(screen.getByTestId('UserProfileInfo')).toBeInTheDocument()
        );

        expect(screen.getByTestId('TransactionTable')).toBeInTheDocument();
        expect(screen.getByTestId('TransactionModal')).toBeInTheDocument();
        expect(screen.getByTestId('EditProfileModal')).toBeInTheDocument();
    });

    test('does not render child stubs while loading', () => {
        axios.get.mockImplementation(() => new Promise(() => {}));

        render(
            <BrowserRouter>
                <Profile />
            </BrowserRouter>
        );

        expect(screen.queryByTestId('UserProfileInfo')).toBeNull();
        expect(screen.queryByTestId('TransactionTable')).toBeNull();
    });
});
