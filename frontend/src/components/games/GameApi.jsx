export const getRandomInt = (max) => {
    const array = new Uint32Array(1);
    window.crypto.getRandomValues(array);
    return (array[0] % max) + 1;
};

export const getRandomReels = (max) => {
    const array = new Uint32Array(1);
    window.crypto.getRandomValues(array);
    return array[0] % max;
};

const suitsArray = ["hearts", "diamonds", "clubs", "spades"];

const values = [
    { name: "2", value: 2 }, { name: "3", value: 3 }, { name: "4", value: 4 },
    { name: "5", value: 5 }, { name: "6", value: 6 }, { name: "7", value: 7 },
    { name: "8", value: 8 }, { name: "9", value: 9 }, { name: "10", value: 10 },
    { name: "J", value: 10 }, { name: "Q", value: 10 }, { name: "K", value: 10 },
    { name: "A", value: 11 }
];

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

export class Deck {
    constructor() {
        this.reset();
    }

    reset() {
        this.cards = suitsArray.flatMap(suit =>
            values.map(({ name, value }) => ({ suit, name, value }))
        );
        this.shuffle();
    }

    shuffle() {
        for (let i = this.cards.length - 1; i > 0; i--) {
            const j = Math.floor(
                window.crypto.getRandomValues(new Uint32Array(1))[0] /
                (0xFFFFFFFF + 1) * (i + 1)
            );
            [this.cards[i], this.cards[j]] = [this.cards[j], this.cards[i]];
        }
    }

    drawCard() {
        if (this.cards.length === 0) {
            this.reset();
        }
        return this.cards.pop();
    }

    getCount() {
        return this.cards.length;
    }
}
