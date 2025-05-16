import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import TransactionModal from '../components/user/profileUtils/TransactionModal.jsx';
import { vi, expect, it, describe, beforeEach } from 'vitest';
import { toast } from 'react-toastify';

vi.mock('react-toastify', () => ({
    toast: { error: vi.fn() },
    ToastContainer: () => <div data-testid="toast-container" />,
}));

describe('TransactionModal', () => {
    const onClose = vi.fn();
    const onSubmit = vi.fn();

    beforeEach(() => {
        vi.clearAllMocks();
    });

    it('does not render when show=false', () => {
        render(
            <TransactionModal
                show={false}
                onClose={onClose}
                onSubmit={onSubmit}
                userBalance={100}
            />
        );
        expect(screen.queryByRole('form')).toBeNull();
    });

    it('valid deposit submits correctly', () => {
        render(
            <TransactionModal
                show={true}
                onClose={onClose}
                onSubmit={onSubmit}
                userBalance={100}
            />
        );
        fireEvent.change(screen.getByPlaceholderText('Amount'), {
            target: { value: '50' },
        });
        fireEvent.click(screen.getByText('Submit'));
        expect(onSubmit).toHaveBeenCalledWith('50', 'DEPOSIT');
    });

    it('negative amount shows error', () => {
        render(
            <TransactionModal
                show={true}
                onClose={onClose}
                onSubmit={onSubmit}
                userBalance={100}
            />
        );
        fireEvent.change(screen.getByPlaceholderText('Amount'), {
            target: { value: '-10' },
        });
        fireEvent.click(screen.getByText('Submit'));
        expect(onSubmit).not.toHaveBeenCalled();
    });

    it('withdrawal over balance shows error', () => {
        render(
            <TransactionModal
                show={true}
                onClose={onClose}
                onSubmit={onSubmit}
                userBalance={50}
            />
        );
        // switch to withdrawal
        fireEvent.change(screen.getByDisplayValue('Top Up'), {
            target: { value: 'WITHDRAWAL' },
        });
        fireEvent.change(screen.getByPlaceholderText('Amount'), {
            target: { value: '100' },
        });
        fireEvent.click(screen.getByText('Submit'));
        expect(toast.error).toHaveBeenCalledWith(
            'Insufficient funds for withdrawal'
        );
        expect(onSubmit).not.toHaveBeenCalled();
    });
});
