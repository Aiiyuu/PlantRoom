
import { defineStore } from "pinia"
import Feedback from '@/types/FeedbackInterface'
import axios, { AxiosResponse } from 'axios'

export const useFeedbackStore = defineStore("feedback", {
    state: () => ({
        feedbacks: [] as Feedback[],
        isLoading: false,
        error: null as string | null,
    }),

    actions: {
        /**
         * Fetch a list of feedback from the API endpoint
         */
        async fetchFeedbacks(): Promise<void> {
            // Reset the isLoading and error states before fetching data
            this.isLoading = true
            this.error = null

            try {
                const response: AxiosResponse<Feedback[]> = await axios.get('feedback')
                this.feedbacks = response.data // Update the feedbacks array

            } catch( error: unknown ) {
                // Type assertion to tell TypeScript that error is an instance of Error
                if (error instanceof Error) {
                    this.error = error.message || 'Failed to load feedbacks.';
                } else {
                    // Handle other cases where error may not be an instance of Error
                    this.error = 'Failed to load feedbacks.';
                }
            } finally {
                this.isLoading = false
            }
        }
    }
})