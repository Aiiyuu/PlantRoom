

/**
 * Represents the data required to register a new user.
 *
 * @property {string} email - The user's email address for login and contact.
 * @property {string} name - The user's full name or display name.
 * @property {string} password - The user's password for account authentication.
 */
export default interface SignupPayload {
    email: string;
    name: string;
    password: string;
}
