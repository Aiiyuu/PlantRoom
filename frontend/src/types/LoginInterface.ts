

/**
 * Represents the data required to login.
 *
 * @property {string} email - The user's email address for login and contact.
 * @property {string} password - The user's password for account authentication.
 */
export default interface LoginPayload {
  email: string;
  password: string;
}
