import type { InputHTMLAttributes } from "react";

type TextInputProps = InputHTMLAttributes<HTMLInputElement> & {
    id: string;
    label: string;
    error?: boolean;
};

const TextInput = ({ id, label, error = false, className = "", ...props }: TextInputProps) => {
    const borderClasses = error
        ? "border-rose-300 dark:border-rose-500 focus:border-rose-400 focus:ring-rose-400/20"
        : "border-slate-200 dark:border-slate-700 focus:border-indigo-400 dark:focus:border-indigo-500 focus:ring-indigo-400/20 dark:focus:ring-indigo-500/20";

    return (
        <div>
            <label htmlFor={id} className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1.5">
                {label}
            </label>
            <input
                id={id}
                className={`w-full px-4 py-2.5 rounded-xl text-sm bg-slate-50 dark:bg-slate-800 border text-slate-900 dark:text-slate-100 placeholder:text-slate-400 dark:placeholder:text-slate-500 outline-none focus:ring-2 transition-all duration-200 ${borderClasses} ${className}`}
                {...props}
            />
        </div>
    );
};

export default TextInput;
