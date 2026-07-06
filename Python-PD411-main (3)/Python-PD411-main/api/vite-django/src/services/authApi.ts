import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

export type User = {
    id: number;
    username: string;
    email: string;
    first_name: string;
    last_name: string;
    image_small: string | null;
    image_medium: string | null;
    image_large: string | null;
};

export type AuthResponse = {
    user: User;
    access: string;
    refresh: string;
};

export type RegisterRequest = FormData;

export type LoginRequest = {
    email: string;
    password: string;
};

export const saveAuth = (auth: AuthResponse) => {
    localStorage.setItem("accessToken", auth.access);
    localStorage.setItem("refreshToken", auth.refresh);
    localStorage.setItem("user", JSON.stringify(auth.user));
};

export const authApi = createApi({
    reducerPath: "authApi",
    baseQuery: fetchBaseQuery({
        baseUrl: import.meta.env.VITE_API_URL ?? "http://127.0.0.1:8000/api/",
        prepareHeaders: headers => {
            const token = localStorage.getItem("accessToken");
            if (token) {
                headers.set("Authorization", `Bearer ${token}`);
            }
            return headers;
        },
    }),
    endpoints: builder => ({
        register: builder.mutation<AuthResponse, RegisterRequest>({
            query: body => ({
                url: "users/register/",
                method: "POST",
                body,
            }),
        }),
        login: builder.mutation<AuthResponse, LoginRequest>({
            query: body => ({
                url: "users/login/",
                method: "POST",
                body,
            }),
        }),
    }),
});

export const { useRegisterMutation, useLoginMutation } = authApi;
