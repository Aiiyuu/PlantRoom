
/**
 * Represents a user object
 */
export default interface User {
    id: number,
    name: string,
    email: string,
    is_superuser: boolean,
    date_joined: string,
}