/**
 * @file PlantCard.spec.ts
 * @description
 * This file contains unit tests for the `PlantCard.vue` component using Vitest and Vue Test Utils.
 *
 * The component displays information about a plant, including its name, price, discounted price, image,
 * and rating. It also handles conditional rendering for discounted prices and renders star ratings
 * based on the plant's rating.
 *
 * The tests cover the following functionalities:
 * 1. Rendering plant details (name, price, image).
 * 2. Correct rendering of the discount and original price.
 * 3. Rendering the correct number of filled and empty stars based on the plant's rating.
 * 4. Handling cases where no discount is applied.
 *
 * The tests use mocked data to simulate different plant details and validate that the component
 * displays the expected content.
 */

import { mount } from '@vue/test-utils'
import { describe, it, expect } from 'vitest'
import PlantCard from '@/components/ui/PlantCard.vue'
import Plant from '@/types/PlantInterface'
import { defineComponent, provide } from "vue"

// Mocked base URL from app's global configuration
const mockImageBaseUrl = 'http://127.0.0.1:8000/'

describe('PlantCard.vue', (): void => {
    // ----------- Render Tests -----------
    it('renders the plant name, price, and image correctly', async () => {
        // Create a plant object
        const plant: Plant = {
            id: 1,
            name: 'Aloe Vera',
            description: 'A soothing plant perfect for skincare.',
            price: 29.99,
            discount_percentage: 30,
            discounted_price: 19.99,
            stock_count: 100,
            in_stock: true,
            rating: 4,
            image: 'aloe-vera.jpg',
        };


        // Mount the PlantCard component for testing
        const wrapper = mount(PlantCard, {
            // Provide props to the component
            props: {
                plant, // Data related to the plant
                isLoading: false,
            },
            global: {
                // Provide global dependencies for all components
                provide: {
                    $imageBaseUrl: mockImageBaseUrl // Mocked base URL for images
                }
            }
        })

        // Check if the plant name is rendered correctly
        expect(wrapper.find('.card__name').text()).toBe('Aloe Vera')

        // Check if price and discounted price are displayed correctly
        expect(wrapper.find('.card__price span').text()).toBe('$19.99')
        expect(wrapper.find('.card__price .line-through').text()).toBe('$29.99')

        // Check if image source is correct
        expect(wrapper.find('img').attributes('src')).toBe(`${mockImageBaseUrl}aloe-vera.jpg`)
    })


    // ----------- Rendering of the price and discount price tests -----------
    it('renders the price and discount price correctly', (): void => {
        // Create a plant object
        const plant: Plant = {
            id: 2,
            name: 'Cactus',
            description: 'A small, spiky plant that’s low maintenance.',
            price: 50.00,
            discount_percentage: 20,
            discounted_price: 40.00,
            stock_count: 50,
            in_stock: true,
            rating: 3,
            image: 'cactus.jpg',
        };

        // Mount the PlantCard component for testing
        const wrapper = mount(PlantCard, {
            // Provide props to the component
            props: {
                plant,
                isLoading: false,
            },
            global: {
                // Provide global dependencies for all components
                provide: {
                    $imageBaseUrl: mockImageBaseUrl
                }
            }
        })

        // Expect the discounted price to be shown
        expect(wrapper.find('.card__price span').text()).toBe('$40');

        // Expect the original price to have a strikethrough
        expect(wrapper.find('.card__price .line-through').text()).toBe('$50');
    })


    // ----------- Rendering the correct number of filled and empty stars tests -----------
    it ('renders the correct number of filled and empty starts', (): void => {
        // Create a plant object
        const plant: Plant = {
            id: 3,
            name: 'Fern',
            description: 'A lush, green plant that thrives in humid environments.',
            price: 30.00,
            discount_percentage: 10,
            discounted_price: 27.00,
            stock_count: 30,
            in_stock: true,
            rating: 4,
            image: 'fern.jpg',
        };

        // Mount the PlantCard component for testing
        const wrapper = mount(PlantCard, {
            // Provide props to the component
            props: {
                plant: plant,
                isLoading: false,
            },
            global: {
                // Provide global dependencies for all components
                provide: {
                    $imageBaseUrl: mockImageBaseUrl
                }
            }
        })

        // Find all the star elements
        const stars = wrapper.findAll('.star');

        // There should be 5 stars
        expect(stars).toHaveLength(5);

        // The first 4 stars should be filled (active)
        expect(stars[0].classes()).toContain('star--active')
        expect(stars[1].classes()).toContain('star--active')
        expect(stars[2].classes()).toContain('star--active')
        expect(stars[3].classes()).toContain('star--active')

        // The last star should be inactive
        expect(stars[4].classes()).toContain('star--inactive')
    })


    // ----------- Rendering the case when no discount is applied correctly -----------
    it('renders correctly when no discount is applied', (): void => {
        // Create a plant object
        const plant: Plant = {
            id: 4,
            name: 'Cactus',
            description: 'A hardy, drought-tolerant plant that thrives in arid environments.',
            price: 15.00,
            stock_count: 50,
            in_stock: true,
            rating: 4,
            image: 'cactus.jpg',
        };

        // Mount the PlantCard component for testing
        const wrapper = mount(PlantCard, {
            // Provide props to the component
            props: {
                plant: plant,
                isLoading: false,
            },
            global: {
                // Provide global dependencies for all components
                provide: {
                    $imageBaseUrl: mockImageBaseUrl
                }
            }
        })

        // Check if the price is rendered correctly without strikethrough
        expect(wrapper.find('.card__price span').text()).toBe('$15');
        expect(wrapper.find('.card__price .line-through').exists()).toBe(false);
    })

})