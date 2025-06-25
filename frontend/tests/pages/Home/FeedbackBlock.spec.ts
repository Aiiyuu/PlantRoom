/**
 * @file FeedbackBlock.spec.ts
 * @description
 * This file contains unit tests for the `FeedbackBlock.vue` component using Vitest and Vue Test Utils.
 *
 * The `FeedbackBlock` component displays a list of feedbacks in a carousel format.
 *
 * The tests cover the following functionalities:
 * 1. Verifying that `FeedbackCard` components are rendered for each item feedback item.
 * 2. Verify that a "no items" message is displayed when the feedbacks state is empty and loading is false. *
 *
 * The tests use mocked stores data to simulate different feedback and loading states, and validate that the component
 * behaves as expected in these scenarios.
 */


import { mount } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import FeedbackCard from '@/components/ui/FeedbackCard.vue'
import FeedbackBlock from "@/pages/Home/FeedbackBlock.vue"
import Feedback from '@/types/FeedbackInterface'
import { setActivePinia, createPinia } from 'pinia'
import { useFeedbackStore } from "@/stores/feedback"

describe('FeedbackBlock.vue', (): void=> {
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

    beforeEach(() => {
        setActivePinia(createPinia())
        vi.clearAllMocks()
    })

    // ----------- Verify that a FeedbackCard is rendered for each feedback item -----------
    it('renders a FeedbackCard component for each feedback item', async () => {
        const store = useFeedbackStore()

        // Mock fetchFeedbacks to immediately set feedbacks to mockFeedbacks
        store.fetchFeedbacks = vi.fn().mockResolvedValue(undefined)
        store.feedbacks = mockFeedbacks

        const wrapper = mount(FeedbackBlock)

        // Wait for onMounted fetchFeedbacks to resolve
        await wrapper.vm.$nextTick()
        await wrapper.vm.$nextTick() // sometimes need extra tick to ensure reactive updates

        // duplicatedFeedbacks should now be twice the length of feedbacks
        const feedbackCards = wrapper.findAllComponents(FeedbackCard)
        expect(feedbackCards).toHaveLength(mockFeedbacks.length * 2)
    })

    // ----------- Verify that a "no items" message is shown when feedback list is empty and loading is false -----------
    it('shows no items message when feedback list is empty and loading is false', async () => {
        // Mount the FeedbackBlock component for testing
        const wrapper = mount(FeedbackBlock);
        const store = useFeedbackStore()

        // Make sure that isLoading is set to false and the feedbacks state is empty
        store.isLoading = false;
        store.feedbacks = [];

        // Make sure the appropriate message is shown
        expect(wrapper.text()).toContain('No feedbacks available')

        // Check that the feedback__list is not displayed (v-if="feedbackStore.feedbacks?.length")
        const feedbackList = wrapper.find('.feedback__list');
        expect(feedbackList.exists()).toBe(false);
    })
})

