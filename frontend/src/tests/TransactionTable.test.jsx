import React from 'react';
import { render, screen } from '@testing-library/react';
import TransactionTable from '../components/user/profileUtils/TransactionTable.jsx';
import DisplayDate from '../components/user/DateApi.jsx';
import { vi, describe, beforeEach, it, expect } from 'vitest';

vi.mock(
    '../components/user/DateApi.jsx',
    () => ({
        default: ({ dateString }) => <span data-testid="date">{dateString}</span>,
    })
);

describe('TransactionTable', () => {
    it('renders no-transactions message', () => {
        render(<TransactionTable transactions={[]} />);
        expect(
            screen.getByText('No transactions available.')
        ).toBeInTheDocument();
    });

    it('renders a table row per transaction', () => {
        const txns = [
            { date: '2025-05-01', transaction_type: 'deposit', amount: '10' },
            { date: '2025-05-02', transaction_type: 'withdrawal', amount: '5.5' },
        ];
        render(<TransactionTable transactions={txns} />);
        const rows = screen.getAllByRole('row');
        expect(rows).toHaveLength(3);
        expect(screen.getAllByTestId('date')[0]).toHaveTextContent('2025-05-01');
        expect(screen.getByText('deposit')).toBeInTheDocument();
        expect(screen.getByText('5.50')).toBeInTheDocument();
    });
});
