import axios from "axios";

export default async function fetchUser() {
    const res = await axios.get(`${import.meta.env.VITE_API_URL}/user/profile`, {
        headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
    });
    return res.data;
}