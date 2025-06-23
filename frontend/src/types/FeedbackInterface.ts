

/**
 * Represents a feedback object.
 */
export default interface Feedback {
    id: number,
    user: {
        id: number,
        email: string,
        name: string,
        data_joined: string,
        is_superuser: boolean,
    },
    content: string,
    rating: number,
    added_at: string,
    is_current_user: boolean,
}

