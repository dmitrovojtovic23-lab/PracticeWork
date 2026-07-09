import {Navigate} from "react-router";
import {useGetUsersQuery} from "../services/usersApi.ts";
import {useAppSelector} from "../store";

const ProfilePage = () => {
    const {accessToken, username, user: storedUser} = useAppSelector(state => state.auth);
    const {data: users, isLoading} = useGetUsersQuery(undefined, {
        skip: !accessToken || !username,
    });

    if (!accessToken || !username) {
        return <Navigate to="/login" replace/>;
    }

    const user = users?.find(item => item.username === username) ?? storedUser ?? {username};
    const fullName = [user.first_name, user.last_name].filter(Boolean).join(" ");
    const fields = [
        {label: "ID", value: user.id},
        {label: "Логін", value: user.username},
        {label: "Email", value: user.email},
        {label: "Ім'я", value: user.first_name},
        {label: "Прізвище", value: user.last_name},
    ];

    return (
        <div className="min-h-screen bg-slate-50 dark:bg-slate-950 px-4 pb-16 transition-colors duration-300">
            <div className="max-w-4xl mx-auto">
                <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-sm overflow-hidden">
                    <div className="bg-gradient-to-r from-indigo-500 to-violet-600 px-8 py-10">
                        <div className="flex flex-col sm:flex-row sm:items-center gap-5">
                            {user.image ? (
                                <img
                                    src={user.image}
                                    alt={user.username}
                                    className="w-24 h-24 rounded-2xl object-cover border-4 border-white/40 shadow-lg"
                                />
                            ) : (
                                <div className="w-24 h-24 rounded-2xl bg-white/20 border-4 border-white/30 flex items-center justify-center text-white text-4xl font-bold shadow-lg">
                                    {user.username?.charAt(0).toUpperCase()}
                                </div>
                            )}
                            <div>
                                <p className="text-white/80 text-sm font-medium">@{user.username}</p>
                                <h1 className="text-3xl font-bold text-white mt-1">
                                    {fullName || user.username}
                                </h1>
                                {user.email && (
                                    <p className="text-white/80 text-sm mt-2">{user.email}</p>
                                )}
                            </div>
                        </div>
                    </div>

                    <div className="p-8">
                        <h2 className="text-xl font-semibold text-slate-900 dark:text-slate-50 mb-5">
                            Інформація профілю
                        </h2>

                        {isLoading ? (
                            <div className="py-10 text-center text-slate-500 dark:text-slate-400">
                                Завантаження...
                            </div>
                        ) : (
                            <div className="grid sm:grid-cols-2 gap-4">
                                {fields.map(field => (
                                    <div
                                        key={field.label}
                                        className="rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-800/50 p-4"
                                    >
                                        <p className="text-xs font-medium uppercase text-slate-500 dark:text-slate-400">
                                            {field.label}
                                        </p>
                                        <p className="mt-1 text-slate-900 dark:text-slate-100 break-words">
                                            {field.value || "Не вказано"}
                                        </p>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ProfilePage;
