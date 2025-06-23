/**
 * @file FeedbackCard.spec.ts
 * @description
 * This file contains unit tests for the `FeedbackCard.vue` component using Vitest and Vue Test Utils.
 *
 * The component displays information about a feedback, including its author, content, and rating.
 * It also renders star ratings based on the feedback's rating.
 *
 * The tests cover the following functionalities:
 * 1. Rendering feedback details (name, price, image).
 * 2. Rendering the correct number of filled and empty stars based on the feedback's rating.
 *
 * The tests use mocked data to simulate different plant details and validate that the component
 * displays the expected content.
 */

import { mount } from '@vue/test-utils'
import { describe, it, expect } from 'vitest'
import FeedbackCard from '@/components/ui/FeedbackCard.vue'
import Feedback from '@/types/FeedbackInterface'



describe('FeedbackCard.vue', () => {
    // Create the feedback object
    const feedback: Feedback = {
        id: 1,
        user: {
            id: 101,
            email: "johndoe@example.com",
            name: "John Doe",
            data_joined: "2024-03-15T10:00:00Z",
            is_superuser: false,
        },
        content: "Great service and easy to use!",
        rating: 3,
        added_at: "2025-06-22T14:30:00Z",
        is_current_user: true,
    }

    // ----------- Render Tests -----------
    it('renders the feedback author, content, and added_at date correctly', async () => {
        const wrapper = mount(FeedbackCard, {
            // Provide props to the component
            props: {
                feedback,
                isLoading: false
            }
        })

        // Basic assertions to see if rendering works
        expect(wrapper.find('.card__header__title').text()).toContain('John Doe');
        expect(wrapper.find('.card__header__date').text()).toContain('2025-06-22T14:30:00Z');
        expect(wrapper.find('.card__content p').text()).toContain('Great service and easy to use!');
    })

    // ----------- Rendering the correct number of filled and empty stars tests -----------
    it ('renders the correct number of filled and empty starts', (): void => {
        // Mount the FeedbackCard for testing
        const wrapper = mount(FeedbackCard, {
            // Provide props to the component
            props: {
                feedback,
                isLoading: false
            }
        })

        // Find all the star elements
        const stars = wrapper.findAll('.star');

        // There should be 5 stars
        expect(stars).toHaveLength(5);

        // The first 3 stars should be filled (active)
        expect(stars[0].classes()).toContain('star--active')
        expect(stars[1].classes()).toContain('star--active')
        expect(stars[2].classes()).toContain('star--active')

        // The last two stars should be inactive
        expect(stars[3].classes()).toContain('star--inactive')
        expect(stars[4].classes()).toContain('star--inactive')
    })
})