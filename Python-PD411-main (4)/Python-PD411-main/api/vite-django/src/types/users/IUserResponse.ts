import type {IUserItem} from "./IUserItem.ts";

export interface IUserResponse {
    message: string
    username: string
    id?: string
    email?: string
    first_name?: string
    last_name?: string
    image?: string
    user?: IUserItem
    tokens: {
        refresh: string
        access: string
    }
}
