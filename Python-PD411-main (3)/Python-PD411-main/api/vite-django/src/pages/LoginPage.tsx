import { useState } from "react";
import { Link, useNavigate } from "react-router";
import * as z from "zod";
import { Controller, useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";

import { saveAuth, useLoginMutation } from "../services/authApi";

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

const formSchema = z.object({
    email: z.string().email({ message: "Введіть коректну електронну пошту" }),
    password: z
        .string()
        .min(6, { message: "Пароль повинен містити щонайменше 6 символів" })
        .max(100, { message: "Пароль занадто довгий" }),
});

const LoginPage = () => {
    const navigate = useNavigate();
    const [showPass, setShowPass] = useState(false);
    const [serverError, setServerError] = useState("");
    const [login, { isLoading }] = useLoginMutation();

    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            email: "",
            password: "",
        },
    });

    const onSubmit = async (data: z.infer<typeof formSchema>) => {
        setServerError("");

        try {
            const auth = await login(data).unwrap();
            saveAuth(auth);
            navigate("/");
        } catch {
            setServerError("Невірний email або пароль.");
        }
    };

    return (
        <div className="min-h-screen bg-slate-50 dark:bg-slate-950 flex items-center justify-center px-4 transition-colors duration-300">
            <div className="pointer-events-none fixed inset-0 overflow-hidden">
                <div className="absolute -top-40 -left-40 w-[600px] h-[600px] rounded-full bg-indigo-400/10 dark:bg-indigo-600/10 blur-3xl" />
                <div className="absolute -bottom-40 -right-40 w-[500px] h-[500px] rounded-full bg-violet-400/10 dark:bg-violet-600/10 blur-3xl" />
            </div>

            <div className="relative w-full max-w-[400px]">
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
                            Вхід до акаунту
                        </h1>
                        <p className="text-sm text-slate-500 dark:text-slate-400">
                            Увійдіть за email та паролем
                        </p>
                    </div>

                    <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
                        <Controller
                            name="email"
                            control={form.control}
                            render={({ field, fieldState }) => (
                                <div>
                                    <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1.5">
                                        Електронна пошта
                                    </label>
                                    <input
                                        type="email"
                                        {...field}
                                        placeholder="kozak@sich.ua"
                                        required
                                        className={`w-full px-4 py-2.5 rounded-xl text-sm bg-slate-50 dark:bg-slate-800 border ${fieldState.error ? "border-red-400 dark:border-red-500" : "border-slate-200 dark:border-slate-700"} text-slate-900 dark:text-slate-100 placeholder:text-slate-400 dark:placeholder:text-slate-500 outline-none focus:border-indigo-400 dark:focus:border-indigo-500 focus:ring-2 focus:ring-indigo-400/20 dark:focus:ring-indigo-500/20 transition-all duration-200`}
                                    />
                                    {fieldState.error && (
                                        <p className="mt-1.5 text-sm text-red-500 dark:text-red-400">
                                            {fieldState.error.message}
                                        </p>
                                    )}
                                </div>
                            )}
                        />

                        <Controller
                            name="password"
                            control={form.control}
                            render={({ field, fieldState }) => (
                                <div>
                                    <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1.5">
                                        Пароль
                                    </label>
                                    <div className="relative">
                                        <input
                                            type={showPass ? "text" : "password"}
                                            {...field}
                                            placeholder="********"
                                            className={`w-full px-4 py-2.5 pr-11 rounded-xl text-sm bg-slate-50 dark:bg-slate-800 border ${fieldState.error ? "border-red-400 dark:border-red-500" : "border-slate-200 dark:border-slate-700"} text-slate-900 dark:text-slate-100 placeholder:text-slate-400 dark:placeholder:text-slate-500 outline-none focus:border-indigo-400 dark:focus:border-indigo-500 focus:ring-2 focus:ring-indigo-400/20 dark:focus:ring-indigo-500/20 transition-all duration-200`}
                                        />
                                        <button
                                            type="button"
                                            onClick={() => setShowPass(value => !value)}
                                            className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 dark:text-slate-500 hover:text-slate-600 dark:hover:text-slate-300 transition-colors duration-150"
                                            aria-label="Показати пароль"
                                        >
                                            <EyeIcon open={showPass} />
                                        </button>
                                    </div>
                                    {fieldState.error && (
                                        <p className="mt-1.5 text-sm text-red-500 dark:text-red-400">
                                            {fieldState.error.message}
                                        </p>
                                    )}
                                </div>
                            )}
                        />

                        {serverError && (
                            <p className="text-sm text-red-500 dark:text-red-400">
                                {serverError}
                            </p>
                        )}

                        <button
                            type="submit"
                            disabled={isLoading}
                            className="w-full mt-2 py-2.5 px-4 rounded-xl text-sm font-semibold bg-gradient-to-r from-indigo-500 to-violet-600 text-white shadow-md shadow-indigo-500/30 hover:shadow-lg hover:shadow-indigo-500/40 hover:scale-[1.01] disabled:opacity-70 disabled:cursor-not-allowed disabled:scale-100 transition-all duration-200 flex items-center justify-center gap-2"
                        >
                            {isLoading ? "Вхід..." : "Увійти"}
                        </button>
                    </form>
                </div>

                <p className="text-center text-sm text-slate-500 dark:text-slate-400 mt-6">
                    Ще немає акаунту?{" "}
                    <Link to="/register" className="text-indigo-500 dark:text-indigo-400 font-medium hover:underline">
                        Зареєструватися
                    </Link>
                </p>
            </div>
        </div>
    );
};

export default LoginPage;
