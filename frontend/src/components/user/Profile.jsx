import {useEffect, useState} from "react";
import fetchUser from "./UserApi.jsx";
import {Banknote, DollarSign, Mail, Pencil, User} from "lucide-react";

export default function Profile() {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [isEditing, setIsEditing] = useState(false);

    useEffect(() => {
        const getUser = async () => {
            try {
                const res = await fetchUser()
                setUser(res);
            } catch (err) {
                console.error('Error fetching user:', err);
            } finally {
                setLoading(false);
            }
        };

        getUser();
    }, []);

    const handleEdit = async (e) => {
        e.preventDefault();
        setError(null);

        try {
            const res = await fetch(`${apiUrl}/user/update/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                },
                body: JSON.stringify(user)
            });

            if (!res.ok) throw new Error('Failed to update user profile');

            const data = await res.json();
            setUser(data);
            setIsEditing(false);
        } catch (err) {
            setError(err.message);
        }
    }

    const apiUrl = import.meta.env.VITE_API_URL;

    return (
        <div className="flex-grow flex flex-col items-center p-6">
            <div className="container max-w-4xl bg-slate-900 border border-yellow-400 rounded-lg p-6 shadow-xl w-full">
                <div className="flex relative justify-between items-center mb-4">
                    <div className="absolute top-0 right-0 flex flex-col space-y-2">
                        <button
                            onClick={() => setIsEditing(!isEditing)}
                            className="flex row bg-yellow-400 text-black px-4 py-2 rounded hover:bg-yellow-500 transition-colors w-auto"
                        > <Pencil className="h-6 w-6 text-black mr-2"/> {isEditing ? "Save" : "Edit"} </button>
                        <button className="flex row bg-yellow-400 text-black px-4 py-2 rounded hover:bg-yellow-500 transition-colors w-auto">
                            <DollarSign className="h-6 w-6 text-black mr-2"/>Top Up</button>
                    </div>
                    <div className="flex items-center">
                        <User className="h-6 w-6 text-yellow-400 mr-2"/>
                        <span className="text-xl text-yellow-400">Profile</span>
                    </div>
                </div>
                <div className="flex flex-col items-start gap-2">
                    <div className="flex items-center">
                        <Mail className="h-6 w-6 text-yellow-400 mr-2"/><span className="text-xl"> {user?.email}</span>
                    </div>
                    <div className="flex items-center">
                        <Banknote className="h-6 w-6 text-yellow-400 mr-2"/><span className="text-xl"> $1000 </span>
                    </div>
                </div>
                { isEditing &&
                    <form onSubmit={handleEdit} className="flex flex-col gap-4 mt-6">
                        <label className="block text-sm mb-1">Old Password</label>
                        <input
                            type="password"
                            value={user?.old_password}
                            onChange={(e) => setUser({...user, old_password: e.target.value})}
                            className="bg-gray-700 rounded p-2 text-white"
                            placeholder="Old Password"
                        />
                        <label className="block text-sm mb-1">New Password</label>
                        <input
                            type="password"
                            value={user?.password}
                            onChange={(e) => setUser({...user, password: e.target.value})}
                            className="bg-gray-700 rounded p-2 text-white"
                            placeholder="Password"
                        />
                        <label className="block text-sm mb-1">Confirm new password</label>
                        <input
                            type="password"
                            value={user?.confirm_password}
                            onChange={(e) => setUser({...user, confirm_password: e.target.value})}
                            className="bg-gray-700 rounded p-2 text-white"
                            placeholder="Confirm Password"
                        />
                    </form>
                }
            </div>
        </div>
)
}