/**
 * @file feedbackStore.test.ts
 * @description
 * This file contains unit tests for the `feedbackStore` Pinia store using Vitest.
 *
 * The `feedbackStore` manages the feedbacks, including loading state, error handling.
 * It fetches data from an external API.
 *
 * The tests cover the following functionalities:
 * 1. Verifying the store initializes with the correct default state.
 * 2. Ensuring that `fetchInventory` correctly updates state on success.
 * 3. Testing error handling when `fetchInventory` fails.
 *
 * Axios is mocked to simulate API success and failure scenarios.
 */

import { setActivePinia, createPinia } from "pinia"
import { beforeEach, describe, test, vi, expect } from "vitest"
import axios from 'axios'
import Feedback from '@/types/FeedbackInterface'
import { useFeedbackStore } from "@/store/feedbackStore"

vi.mock('axios')


describe('FeedbackStore', (): void => {
    // Mock response data
    const mockFeedbacks: Feedback[] = [
        {
            id: 1,
            user: {
                id: 101,
                email: "alice@example.com",
                name: "Alice Johnson",
                data_joined: "2023-01-15T10:20:30Z",
                is_superuser: false,
            },
            content: "Great product, really helped me with my workflow!",
            rating: 5,
            added_at: "2024-04-01T08:45:00Z",
            is_current_user: false,
        },
        {
            id: 2,
            user: {
                id: 102,
                email: "bob.smith@example.com",
                name: "Bob Smith",
                data_joined: "2022-11-22T14:12:00Z",
                is_superuser: true,
            },
            content: "Good overall, but could use some improvements in UI.",
            rating: 3,
            added_at: "2024-05-10T12:30:00Z",
            is_current_user: true,
        },
        {
            id: 3,
            user: {
                id: 103,
                email: "carol@example.com",
                name: "Carol Davis",
                data_joined: "2024-02-10T09:00:00Z",
                is_superuser: false,
            },
            content: "Not satisfied with the customer support response time.",
            rating: 2,
            added_at: "2024-05-15T16:20:00Z",
            is_current_user: false,
        }
    ]

    beforeEach((): void => {
        setActivePinia(createPinia())
        vi.clearAllMocks()
    })

    // --------- Verify that the store initializes with the correct default state ---------
    test('initializes store with correct default state', () => {
        const inventory = useFeedbackStore()

        // Ensure the isLoading state is false by default
        expect(inventory.isLoading).toBe(false)

        // Ensure the feedbacks array is initially empty
        expect(inventory.feedbacks).toHaveLength(0)

        // Ensure the error state is null by default
        expect(inventory.error).toBeNull()
    })

    // --------- Ensures fetchFeedbacks sets loading state, populates feedbacks, and clears errors on success ---------
    test('fetchFeedbacks correctly updates state on success', async () => {
        const store = useFeedbackStore()

        // Set mock implementation
        vi.mocked(axios.get).mockResolvedValue({ data: mockFeedbacks })

        // Now call fetch method
        await store.fetchFeedbacks()

        // Assert expected results
        expect(store.isLoading).toBe(false)
        expect(store.feedbacks).toEqual(mockFeedbacks)
        expect(store.error).toBeNull()
    })

    // -------- Ensure fetchFeedbacks correctly handles case if something went wrong --------
    test('fetchFeedbacks sets error state on failure', async () => {
        const store = useFeedbackStore()

        // Simulate Axios throwing an error
        const errorMessage = 'Network Error'
        const error = new Error(errorMessage)

        // Mock axios.get to reject
        vi.mocked(axios.get).mockRejectedValue(error)

        // Run fetch method
        await store.fetchFeedbacks()

        // Asertions
        expect(store.isLoading).toBe(false)
        expect(store.feedbacks).toEqual([])
        expect(store.error).toBe(errorMessage)
    })
})