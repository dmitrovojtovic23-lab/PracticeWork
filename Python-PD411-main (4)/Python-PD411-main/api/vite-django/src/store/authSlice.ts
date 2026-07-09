import { createSlice, type PayloadAction } from '@reduxjs/toolkit';
import type {IUserItem} from "../types/users/IUserItem.ts";

interface AuthState {
    accessToken: string | null;
    refreshToken: string | null;
    username: string | null;
    user: Partial<IUserItem> | null;
}

const getStoredUser = () => {
    const user = localStorage.getItem('user');

    if (!user) {
        return null;
    }

    try {
        return JSON.parse(user) as Partial<IUserItem>;
    } catch {
        localStorage.removeItem('user');
        return null;
    }
};

const initialState: AuthState = {
    accessToken: localStorage.getItem('accessToken'),
    refreshToken: localStorage.getItem('refreshToken'),
    username: localStorage.getItem('username'),
    user: getStoredUser(),
};

const authSlice = createSlice({
    name: 'auth',
    initialState,
    reducers: {
        setCredentials: (
            state,
            action: PayloadAction<{ access: string; refresh: string; username: string; user?: Partial<IUserItem> }>
        ) => {
            const { access, refresh, username, user } = action.payload;
            state.accessToken = access;
            state.refreshToken = refresh;
            state.username = username;
            state.user = user ?? { username };

            localStorage.setItem('accessToken', access);
            localStorage.setItem('refreshToken', refresh);
            localStorage.setItem('username', username);
            localStorage.setItem('user', JSON.stringify(state.user));
        },
        logout: (state) => {
            state.accessToken = null;
            state.refreshToken = null;
            state.username = null;
            state.user = null;

            localStorage.removeItem('accessToken');
            localStorage.removeItem('refreshToken');
            localStorage.removeItem('username');
            localStorage.removeItem('user');
        },
    },
});

export const { setCredentials, logout } = authSlice.actions;
export default authSlice.reducer;
