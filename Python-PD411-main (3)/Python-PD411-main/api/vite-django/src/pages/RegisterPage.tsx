import { useMemo, useState } from "react";
import { Link, useNavigate } from "react-router";

const EyeIcon = ({ open }: { open: boolean }) => open ? (
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24"
         fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
        <circle cx="12" cy="12" r="3"/>
    </svg>
) : (
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24"
         fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94"/>
        <path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19"/>
        <line x1="1" y1="1" x2="23" y2="23"/>
    </svg>
);

const RegisterPage = () => {
    const navigate = useNavigate();
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [showPassword, setShowPassword] = useState(false);
    const [showConfirmPassword, setShowConfirmPassword] = useState(false);
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
                        <div>
                            <label htmlFor="name" className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1.5">
                                Ім'я
                            </label>
                            <input
                                id="name"
                                type="text"
                                value={name}
                                onChange={e => setName(e.target.value)}
                                placeholder="Ваше ім'я"
                                autoComplete="name"
                                required
                                className="w-full px-4 py-2.5 rounded-xl text-sm bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-slate-100 placeholder:text-slate-400 dark:placeholder:text-slate-500 outline-none focus:border-indigo-400 dark:focus:border-indigo-500 focus:ring-2 focus:ring-indigo-400/20 dark:focus:ring-indigo-500/20 transition-all duration-200"
                            />
                        </div>

                        <div>
                            <label htmlFor="email" className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1.5">
                                Електронна пошта
                            </label>
                            <input
                                id="email"
                                type="email"
                                value={email}
                                onChange={e => setEmail(e.target.value)}
                                placeholder="name@example.com"
                                autoComplete="email"
                                required
                                className="w-full px-4 py-2.5 rounded-xl text-sm bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-slate-100 placeholder:text-slate-400 dark:placeholder:text-slate-500 outline-none focus:border-indigo-400 dark:focus:border-indigo-500 focus:ring-2 focus:ring-indigo-400/20 dark:focus:ring-indigo-500/20 transition-all duration-200"
                            />
                        </div>

                        <div>
                            <label htmlFor="password" className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1.5">
                                Пароль
                            </label>
                            <div className="relative">
                                <input
                                    id="password"
                                    type={showPassword ? "text" : "password"}
                                    value={password}
                                    onChange={e => setPassword(e.target.value)}
                                    placeholder="Мінімум 8 символів"
                                    autoComplete="new-password"
                                    minLength={8}
                                    required
                                    className="w-full px-4 py-2.5 pr-11 rounded-xl text-sm bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-slate-100 placeholder:text-slate-400 dark:placeholder:text-slate-500 outline-none focus:border-indigo-400 dark:focus:border-indigo-500 focus:ring-2 focus:ring-indigo-400/20 dark:focus:ring-indigo-500/20 transition-all duration-200"
                                />
                                <button
                                    type="button"
                                    onClick={() => setShowPassword(v => !v)}
                                    className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 dark:text-slate-500 hover:text-slate-600 dark:hover:text-slate-300 transition-colors duration-150"
                                    aria-label={showPassword ? "Сховати пароль" : "Показати пароль"}
                                >
                                    <EyeIcon open={showPassword} />
                                </button>
                            </div>
                        </div>

                        <div>
                            <label htmlFor="confirmPassword" className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1.5">
                                Повторіть пароль
                            </label>
                            <div className="relative">
                                <input
                                    id="confirmPassword"
                                    type={showConfirmPassword ? "text" : "password"}
                                    value={confirmPassword}
                                    onChange={e => setConfirmPassword(e.target.value)}
                                    placeholder="Повторіть пароль"
                                    autoComplete="new-password"
                                    required
                                    className={`w-full px-4 py-2.5 pr-11 rounded-xl text-sm bg-slate-50 dark:bg-slate-800 border text-slate-900 dark:text-slate-100 placeholder:text-slate-400 dark:placeholder:text-slate-500 outline-none focus:ring-2 transition-all duration-200 ${
                                        passwordsDoNotMatch
                                            ? "border-rose-300 dark:border-rose-500 focus:border-rose-400 focus:ring-rose-400/20"
                                            : "border-slate-200 dark:border-slate-700 focus:border-indigo-400 dark:focus:border-indigo-500 focus:ring-indigo-400/20 dark:focus:ring-indigo-500/20"
                                    }`}
                                />
                                <button
                                    type="button"
                                    onClick={() => setShowConfirmPassword(v => !v)}
                                    className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 dark:text-slate-500 hover:text-slate-600 dark:hover:text-slate-300 transition-colors duration-150"
                                    aria-label={showConfirmPassword ? "Сховати пароль" : "Показати пароль"}
                                >
                                    <EyeIcon open={showConfirmPassword} />
                                </button>
                            </div>
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
