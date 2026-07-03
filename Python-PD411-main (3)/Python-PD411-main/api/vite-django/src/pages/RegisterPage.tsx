import { useMemo, useState } from "react";
import { Link, useNavigate } from "react-router";
import PasswordInput from "../components/PasswordInput";
import PhotoInput from "../components/PhotoInput";
import TextInput from "../components/TextInput";

const RegisterPage = () => {
    const navigate = useNavigate();
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [photo, setPhoto] = useState<File | null>(null);
    const [acceptedTerms, setAcceptedTerms] = useState(false);
    const [loading, setLoading] = useState(false);
    const [submitted, setSubmitted] = useState(false);

    const passwordsDoNotMatch = useMemo(() => {
        return confirmPassword.length > 0 && password !== confirmPassword;
    }, [password, confirmPassword]);

    const canSubmit = name.trim().length > 1 &&
        email.trim().length > 3 &&
        password.length >= 8 &&
        password === confirmPassword &&
        acceptedTerms;

    const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        setSubmitted(true);

        if (!canSubmit) {
            return;
        }

        setLoading(true);
        window.setTimeout(() => {
            setLoading(false);
            navigate("/");
        }, 1600);
    };

    return (
        <div className="min-h-screen bg-slate-50 dark:bg-slate-950 flex items-center justify-center px-4 pb-12 transition-colors duration-300">
            <div className="pointer-events-none fixed inset-0 overflow-hidden">
                <div className="absolute -top-32 left-10 w-[460px] h-[460px] rounded-full bg-indigo-400/10 dark:bg-indigo-600/10 blur-3xl" />
                <div className="absolute -bottom-32 right-10 w-[420px] h-[420px] rounded-full bg-emerald-400/10 dark:bg-emerald-500/10 blur-3xl" />
            </div>

            <div className="relative w-full max-w-[430px]">
                <div className="flex justify-center mb-8">
                    <Link to="/" className="flex items-center gap-2.5 group select-none">
                        <div className="w-10 h-10 rounded-2xl bg-gradient-to-br from-indigo-500 to-violet-600 flex items-center justify-center shadow-lg shadow-indigo-500/30 group-hover:scale-105 transition-transform duration-200">
                            <span className="text-white font-bold text-base">K</span>
                        </div>
                        <span className="font-semibold text-slate-800 dark:text-slate-100 text-lg tracking-tight">
                            KozakyApp
                        </span>
                    </Link>
                </div>

                <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-xl shadow-slate-200/50 dark:shadow-slate-900/50 p-8 transition-colors duration-300">
                    <div className="mb-7">
                        <h1 className="text-2xl font-bold text-slate-900 dark:text-slate-50 tracking-tight mb-1">
                            Створити акаунт
                        </h1>
                        <p className="text-sm text-slate-500 dark:text-slate-400">
                            Заповніть дані для швидкої реєстрації
                        </p>
                    </div>

                    <form onSubmit={handleSubmit} className="space-y-4">
                        <PhotoInput
                            id="photo"
                            label="Фото профілю"
                            value={photo}
                            onChange={setPhoto}
                        />

                        <TextInput
                            id="name"
                            type="text"
                            label="Ім'я"
                            value={name}
                            onChange={e => setName(e.target.value)}
                            placeholder="Ваше ім'я"
                            autoComplete="name"
                            required
                        />

                        <TextInput
                            id="email"
                            type="email"
                            label="Електронна пошта"
                            value={email}
                            onChange={e => setEmail(e.target.value)}
                            placeholder="name@example.com"
                            autoComplete="email"
                            required
                        />

                        <PasswordInput
                            id="password"
                            label="Пароль"
                            value={password}
                            onChange={e => setPassword(e.target.value)}
                            placeholder="Мінімум 8 символів"
                            autoComplete="new-password"
                            minLength={8}
                            required
                        />

                        <div>
                            <PasswordInput
                                id="confirmPassword"
                                label="Повторіть пароль"
                                value={confirmPassword}
                                onChange={e => setConfirmPassword(e.target.value)}
                                placeholder="Повторіть пароль"
                                autoComplete="new-password"
                                error={passwordsDoNotMatch}
                                required
                            />
                            {passwordsDoNotMatch && (
                                <p className="mt-1.5 text-xs text-rose-500 dark:text-rose-400">
                                    Паролі не збігаються
                                </p>
                            )}
                        </div>

                        <div className="flex items-start gap-2.5 pt-1">
                            <input
                                id="terms"
                                type="checkbox"
                                checked={acceptedTerms}
                                onChange={e => setAcceptedTerms(e.target.checked)}
                                className="mt-0.5 w-4 h-4 rounded-md border-slate-300 dark:border-slate-600 accent-indigo-500 cursor-pointer"
                            />
                            <label htmlFor="terms" className="text-sm text-slate-600 dark:text-slate-400 cursor-pointer select-none leading-5">
                                Погоджуюся з умовами користування
                            </label>
                        </div>

                        {submitted && !canSubmit && (
                            <p className="text-xs text-rose-500 dark:text-rose-400">
                                Заповніть усі поля коректно та прийміть умови.
                            </p>
                        )}

                        <button
                            type="submit"
                            disabled={loading}
                            className="w-full mt-2 py-2.5 px-4 rounded-xl text-sm font-semibold bg-gradient-to-r from-indigo-500 to-violet-600 text-white shadow-md shadow-indigo-500/30 hover:shadow-lg hover:shadow-indigo-500/40 hover:scale-[1.01] disabled:opacity-70 disabled:cursor-not-allowed disabled:scale-100 transition-all duration-200 flex items-center justify-center gap-2"
                        >
                            {loading ? (
                                <>
                                    <svg className="animate-spin w-4 h-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"/>
                                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"/>
                                    </svg>
                                    Реєстрація...
                                </>
                            ) : "Зареєструватися"}
                        </button>
                    </form>
                </div>

                <p className="text-center text-sm text-slate-500 dark:text-slate-400 mt-6">
                    Вже маєте акаунт?{" "}
                    <Link to="/login" className="text-indigo-500 dark:text-indigo-400 font-medium hover:underline">
                        Увійти
                    </Link>
                </p>
            </div>
        </div>
    );
};

export default RegisterPage;
