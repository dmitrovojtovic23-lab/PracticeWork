import {useEffect, useRef, useState} from "react";
import {Link, Outlet, useLocation, useNavigate} from "react-router";
import {useAppDispatch, useAppSelector} from "../store";
import {logout} from "../store/authSlice.ts";

const NAV_LINKS = [
    {label: "Головна", to: "/"},
    {label: "Профіль", to: "/profile"},
];

const SunIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24"
         fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <circle cx="12" cy="12" r="5"/>
        <line x1="12" y1="1" x2="12" y2="3"/>
        <line x1="12" y1="21" x2="12" y2="23"/>
        <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/>
        <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
        <line x1="1" y1="12" x2="3" y2="12"/>
        <line x1="21" y1="12" x2="23" y2="12"/>
        <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/>
        <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
    </svg>
);

const MoonIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24"
         fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
    </svg>
);

const ChevronDownIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24"
         fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <polyline points="6 9 12 15 18 9"/>
    </svg>
);

const LogoutIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24"
         fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
        <polyline points="16 17 21 12 16 7"/>
        <line x1="21" y1="12" x2="9" y2="12"/>
    </svg>
);

const MenuIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24"
         fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <line x1="4" y1="6" x2="20" y2="6"/>
        <line x1="4" y1="12" x2="20" y2="12"/>
        <line x1="4" y1="18" x2="20" y2="18"/>
    </svg>
);

const CloseIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24"
         fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <line x1="18" y1="6" x2="6" y2="18"/>
        <line x1="6" y1="6" x2="18" y2="18"/>
    </svg>
);

const RootLayout = () => {
    const dispatch = useAppDispatch();
    const navigate = useNavigate();
    const {accessToken, username, user} = useAppSelector(state => state.auth);
    const location = useLocation();
    const [dark, setDark] = useState(() => {
        if (typeof window !== "undefined") {
            return localStorage.getItem("theme") === "dark" ||
                (!localStorage.getItem("theme") && window.matchMedia("(prefers-color-scheme: dark)").matches);
        }
        return false;
    });
    const [dropdownOpen, setDropdownOpen] = useState(false);
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
    const dropdownRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        const root = document.documentElement;
        if (dark) {
            root.classList.add("dark");
            localStorage.setItem("theme", "dark");
        } else {
            root.classList.remove("dark");
            localStorage.setItem("theme", "light");
        }
    }, [dark]);

    useEffect(() => {
        const handleClickOutside = (event: MouseEvent) => {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
                setDropdownOpen(false);
            }
        };

        document.addEventListener("mousedown", handleClickOutside);
        return () => document.removeEventListener("mousedown", handleClickOutside);
    }, []);

    const handleLogout = () => {
        dispatch(logout());
        setDropdownOpen(false);
        setMobileMenuOpen(false);
        navigate("/");
    };

    return (
        <div className="min-h-screen bg-slate-50 dark:bg-slate-950 transition-colors duration-300">
            <header className="fixed top-0 left-0 right-0 z-50">
                <div className="mx-4 mt-4 rounded-2xl bg-white/70 dark:bg-slate-900/70 backdrop-blur-md border border-slate-200/60 dark:border-slate-700/60 shadow-sm shadow-slate-200/50 dark:shadow-slate-900/50 transition-colors duration-300">
                    <div className="max-w-6xl mx-auto px-5 h-16 flex items-center justify-between">
                        <Link to="/" className="flex items-center gap-2 group select-none">
                            <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-indigo-500 to-violet-600 flex items-center justify-center shadow-md shadow-indigo-500/30 group-hover:scale-105 transition-transform duration-200">
                                <span className="text-white font-bold text-sm">К</span>
                            </div>
                            <span className="font-semibold text-slate-800 dark:text-slate-100 text-[15px] tracking-tight">
                                КозакиApp
                            </span>
                        </Link>

                        <nav className="hidden md:flex items-center gap-1">
                            {NAV_LINKS.map(({label, to}) => {
                                const active = location.pathname === to;
                                return (
                                    <Link
                                        key={to}
                                        to={to}
                                        className={`px-4 py-2 rounded-xl text-sm font-medium transition-all duration-200 ${
                                            active
                                                ? "bg-indigo-50 dark:bg-indigo-500/15 text-indigo-600 dark:text-indigo-400"
                                                : "text-slate-500 dark:text-slate-400 hover:text-slate-800 dark:hover:text-slate-100 hover:bg-slate-100 dark:hover:bg-slate-800"
                                        }`}
                                    >
                                        {label}
                                    </Link>
                                );
                            })}
                        </nav>

                        <div className="flex items-center gap-3">
                            <button
                                onClick={() => setDark(d => !d)}
                                aria-label="Змінити тему"
                                className="w-9 h-9 rounded-xl flex items-center justify-center text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 hover:text-slate-800 dark:hover:text-slate-100 transition-all duration-200"
                            >
                                {dark ? <SunIcon/> : <MoonIcon/>}
                            </button>

                            {accessToken ? (
                                <>
                                    <div className="hidden md:flex items-center gap-2">
                                        <div className="relative" ref={dropdownRef}>
                                            <button
                                                onClick={() => setDropdownOpen(!dropdownOpen)}
                                                className="flex items-center gap-2 px-3 py-2 rounded-xl text-sm font-medium bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-200 hover:bg-slate-200 dark:hover:bg-slate-700 transition-all duration-200"
                                            >
                                                {user?.image ? (
                                                    <img
                                                        src={user.image}
                                                        alt={username || "User"}
                                                        className="w-5 h-5 rounded-full object-cover"
                                                    />
                                                ) : (
                                                    <div className="w-5 h-5 rounded-full bg-indigo-500 flex items-center justify-center text-white text-xs font-bold">
                                                        {username?.charAt(0).toUpperCase()}
                                                    </div>
                                                )}
                                                <span>{username}</span>
                                                <ChevronDownIcon/>
                                            </button>

                                            {dropdownOpen && (
                                                <div className="absolute right-0 mt-2 w-56 rounded-xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 shadow-xl z-50">
                                                    <div className="px-4 py-3 border-b border-slate-200 dark:border-slate-700">
                                                        <p className="text-xs font-medium text-slate-500 dark:text-slate-400">ПРОФІЛЬ</p>
                                                        <p className="mt-1 text-sm font-semibold text-slate-900 dark:text-slate-100">{username}</p>
                                                        {user?.email && (
                                                            <p className="mt-1 text-xs text-slate-500 dark:text-slate-400 truncate">{user.email}</p>
                                                        )}
                                                    </div>
                                                    <Link
                                                        to="/profile"
                                                        onClick={() => setDropdownOpen(false)}
                                                        className="block w-full px-4 py-2.5 text-sm text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors duration-200"
                                                    >
                                                        Мій профіль
                                                    </Link>
                                                    <button
                                                        onClick={handleLogout}
                                                        className="w-full px-4 py-2.5 flex items-center gap-2 text-sm text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-500/10 transition-colors duration-200 border-t border-slate-200 dark:border-slate-700"
                                                    >
                                                        <LogoutIcon/>
                                                        Вийти
                                                    </button>
                                                </div>
                                            )}
                                        </div>
                                    </div>

                                    <button
                                        onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                                        className="md:hidden w-9 h-9 rounded-xl flex items-center justify-center text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 hover:text-slate-800 dark:hover:text-slate-100 transition-all duration-200"
                                    >
                                        {mobileMenuOpen ? <CloseIcon/> : <MenuIcon/>}
                                    </button>
                                </>
                            ) : (
                                <>
                                    <Link
                                        className="hidden md:flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-medium bg-gradient-to-r from-indigo-500 to-violet-600 text-white shadow-md shadow-indigo-500/30 hover:shadow-indigo-500/50 hover:scale-[1.02] transition-all duration-200"
                                        to="/login"
                                    >
                                        Увійти
                                    </Link>
                                    <Link
                                        className="hidden md:flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-medium bg-gradient-to-r from-indigo-500 to-violet-600 text-white shadow-md shadow-indigo-500/30 hover:shadow-indigo-500/50 hover:scale-[1.02] transition-all duration-200"
                                        to="/registration"
                                    >
                                        Зареєструватись
                                    </Link>
                                    <button
                                        onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                                        className="md:hidden w-9 h-9 rounded-xl flex items-center justify-center text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 hover:text-slate-800 dark:hover:text-slate-100 transition-all duration-200"
                                    >
                                        {mobileMenuOpen ? <CloseIcon/> : <MenuIcon/>}
                                    </button>
                                </>
                            )}
                        </div>
                    </div>
                </div>
            </header>

            {mobileMenuOpen && accessToken && (
                <div className="fixed top-24 left-4 right-4 md:hidden z-40 rounded-2xl bg-white/95 dark:bg-slate-900/95 backdrop-blur-md border border-slate-200/60 dark:border-slate-700/60 shadow-lg">
                    <div className="p-4 space-y-2">
                        {NAV_LINKS.map(({label, to}) => {
                            const active = location.pathname === to;
                            return (
                                <Link
                                    key={to}
                                    to={to}
                                    onClick={() => setMobileMenuOpen(false)}
                                    className={`block px-4 py-2 rounded-xl text-sm font-medium transition-all duration-200 ${
                                        active
                                            ? "bg-indigo-50 dark:bg-indigo-500/15 text-indigo-600 dark:text-indigo-400"
                                            : "text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:hover:text-slate-100 hover:bg-slate-100 dark:hover:bg-slate-800"
                                    }`}
                                >
                                    {label}
                                </Link>
                            );
                        })}
                        <div className="my-2 border-t border-slate-200 dark:border-slate-700 pt-2">
                            <Link
                                to="/profile"
                                onClick={() => setMobileMenuOpen(false)}
                                className="block px-4 py-2 rounded-xl text-sm font-medium text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 transition-all duration-200"
                            >
                                Мій профіль
                            </Link>
                            <button
                                onClick={handleLogout}
                                className="w-full px-4 py-2 rounded-xl text-sm font-medium text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-500/10 transition-all duration-200 text-left flex items-center gap-2"
                            >
                                <LogoutIcon/>
                                Вийти
                            </button>
                        </div>
                    </div>
                </div>
            )}

            {mobileMenuOpen && !accessToken && (
                <div className="fixed top-24 left-4 right-4 md:hidden z-40 rounded-2xl bg-white/95 dark:bg-slate-900/95 backdrop-blur-md border border-slate-200/60 dark:border-slate-700/60 shadow-lg">
                    <div className="p-4 space-y-2">
                        <Link
                            to="/login"
                            onClick={() => setMobileMenuOpen(false)}
                            className="block px-4 py-2 rounded-xl text-sm font-medium bg-gradient-to-r from-indigo-500 to-violet-600 text-white text-center hover:shadow-lg transition-all duration-200"
                        >
                            Увійти
                        </Link>
                        <Link
                            to="/registration"
                            onClick={() => setMobileMenuOpen(false)}
                            className="block px-4 py-2 rounded-xl text-sm font-medium bg-gradient-to-r from-indigo-500 to-violet-600 text-white text-center hover:shadow-lg transition-all duration-200"
                        >
                            Зареєструватись
                        </Link>
                    </div>
                </div>
            )}

            <main className="pt-28">
                <Outlet/>
            </main>
        </div>
    );
};

export default RootLayout;
