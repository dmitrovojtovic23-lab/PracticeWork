import { useEffect, useState } from "react";

type PhotoInputProps = {
    id: string;
    label: string;
    value: File | null;
    onChange: (file: File | null) => void;
};

const PhotoInput = ({ id, label, value, onChange }: PhotoInputProps) => {
    const [previewUrl, setPreviewUrl] = useState("");

    useEffect(() => {
        if (!value) {
            setPreviewUrl("");
            return;
        }

        const nextPreviewUrl = URL.createObjectURL(value);
        setPreviewUrl(nextPreviewUrl);

        return () => URL.revokeObjectURL(nextPreviewUrl);
    }, [value]);

    return (
        <div>
            <span className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
                {label}
            </span>
            <label htmlFor={id} className="flex items-center gap-4 cursor-pointer">
                <span className="relative flex h-20 w-20 shrink-0 items-center justify-center overflow-hidden rounded-full border border-slate-200 bg-slate-50 text-slate-400 shadow-sm transition-all duration-200 hover:border-indigo-300 hover:ring-4 hover:ring-indigo-400/10 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-500 dark:hover:border-indigo-500">
                    {previewUrl ? (
                        <img src={previewUrl} alt="Аватар" className="h-full w-full object-cover" />
                    ) : (
                        <svg xmlns="http://www.w3.org/2000/svg" width="34" height="34" viewBox="0 0 24 24"
                             fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round">
                            <path d="M20 21a8 8 0 0 0-16 0"/>
                            <circle cx="12" cy="7" r="4"/>
                        </svg>
                    )}
                </span>
                <span>
                    <span className="block text-sm font-medium text-slate-700 dark:text-slate-200">
                        Обрати фото
                    </span>
                    <span className="block text-xs text-slate-500 dark:text-slate-400">
                        JPG, PNG або WebP
                    </span>
                </span>
            </label>
            <input
                id={id}
                type="file"
                accept="image/png,image/jpeg,image/webp"
                onChange={event => onChange(event.target.files?.[0] ?? null)}
                className="sr-only"
            />
        </div>
    );
};

export default PhotoInput;
