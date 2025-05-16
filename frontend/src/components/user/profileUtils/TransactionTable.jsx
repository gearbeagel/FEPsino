import React from "react";
import { Wallet } from "lucide-react";
import DisplayDate from "../DateApi.jsx";
import PropTypes from "prop-types";

export default function TransactionTable({ transactions }) {
    return (
        <div className="mt-6">
            <div className="flex items-center mb-4">
                <Wallet className="h-6 w-6 text-yellow-400 mr-2" />
                <span className="text-xl text-yellow-400">Transactions</span>
            </div>
            {transactions.length === 0 ? (
                <div className="text-gray-400 text-center">
                    No transactions available.
                </div>
            ) : (
                <div>
                    <table className="table-fixed w-full text-left border-collapse border border-gray-700">
                        <colgroup>
                            <col className="w-[30%]" />
                            <col className="w-[32%]" />
                            <col className="w-[32%]" />
                        </colgroup>
                        <thead className="bg-gray-800 text-yellow-400">
                        <tr>
                            <th className="px-4 py-2 border-y border-gray-700">Date</th>
                            <th className="px-4 py-2 border-y border-gray-700">Type</th>
                            <th className="px-4 py-2 border-y border-gray-700">Amount</th>
                        </tr>
                        </thead>
                    </table>

                    <div className="overflow-auto max-h-60">
                        <table className="table-fixed w-full text-left border-collapse border border-gray-700 border-t-0">
                            <colgroup>
                                <col className="w-[33%]" />
                                <col className="w-[33%]" />
                                <col className="w-[33%]" />
                            </colgroup>
                            <tbody>
                            {transactions.map((t, i) => (
                                <tr key={i} className="odd:bg-gray-700 even:bg-gray-800 hover:bg-gray-600">
                                    <td className="px-4 py-2 border border-gray-700 break-words">
                                        <DisplayDate dateString={t.date} />
                                    </td>
                                    <td className="px-4 py-2 border border-gray-700 break-words">
                                        {t.transaction_type}
                                    </td>
                                    <td className="px-4 py-2 border border-gray-700 break-words">
                                        {parseFloat(t.amount).toFixed(2)}
                                    </td>
                                </tr>
                            ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            )}
        </div>
    );
}

TransactionTable.propTypes = {
    transactions: PropTypes.arrayOf(
        PropTypes.shape({
            date: PropTypes.string.isRequired,
            transaction_type: PropTypes.string.isRequired,
            amount: PropTypes.number.isRequired,
        })
    ).isRequired,
}