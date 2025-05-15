export const fetchBalance = async (setBalance, user) => {
    try {
        if (user && user.balance !== undefined && !isNaN(parseFloat(user.balance))) {
            setBalance(parseFloat(user.balance));
        } else {
            const response = await fetch(
                `${import.meta.env.VITE_API_URL}/user/profile/`,
                {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${localStorage.getItem("access_token")}`,
                    },
                }
            );
            const result = await response.json();
            if (!response.ok) throw new Error(result.error || "Unexpected error");
            const balance = parseFloat(result.balance || 0);
            setBalance(balance);
        }
    } catch (error) {
        throw new Error("Failed to fetch balance: " + error.message);
    }
};
