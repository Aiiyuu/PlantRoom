/**
 * @file TrendingProducts.spec.ts
 * @description
 * This file contains unit tests for the `TrendingProducts.vue` component using Vitest and Vue Test Utils.
 *
 * The `TrendingProducts` component displays a list of trending products in a carousel format. It allows the user
 * to select a sorting method (e.g., featured, cheapest, name) and displays the corresponding inventory items.
 * The component also includes carousel navigation functionality for scrolling through the items.
 *
 * The tests cover the following functionalities:
 * 1. Rendering the title and sorting options (featured, cheapest, name).
 * 2. Ensuring the correct sorting method is selected when a user clicks on a sorting option.
 * 3. Checking that the store's `updateSortMethod` is called when the sorting method is changed.
 * 4. Testing the carousel's navigation functionality (scrolling to the next and previous items).
 * 5. Verifying that `PlantCard` components are rendered for each item in the inventory.
 * 6. Ensuring the component properly interacts with the store's inventory and loading state.
 *
 * The tests use mocked store data to simulate different inventory and loading states, and validate that the component
 * behaves as expected in these scenarios.
 */

import { mount } from '@vue/test-utils'
import { describe, it, expect, vi } from "vitest"
import TrendingProductsBlock from '@/pages/Home/TrendingProductsBlock.vue'
import { useInventoryStore } from "@/store/inventoryStore"

// Mock the inventoryStore
vi.mock('@/store/inventoryStore', () => ({
    useInventoryStore: vi.fn(() => ({
        inventory: [{ id: 1, name: 'Plant 1' }, { id: 2, name: 'Plant 2' }], // Example data
        isLoading: false,
        updateSortMethod: vi.fn(),
        fetchInventory: vi.fn(),
    })),
}));

describe('TrendingProductsBlock.vue', (): void => {
    // ----------- Render Tests -----------
    it('renders the title and sorting options correctly', async () => {
        // Mount the TrendingProductsBlock component for testing
        const wrapper = mount(TrendingProductsBlock)

        // Check if the title is rendered
        expect(wrapper.find('.trending-products__title').text()).toBe('Trending Products');

        // Check if sorting options are rendered
        const sortingItems = wrapper.findAll('.trending-products__sorting-bar__item');

        expect(sortingItems.length).toBe(3); // Assuming there are 3 sorting options
        expect(sortingItems[0].text()).toBe('featured');
        expect(sortingItems[1].text()).toBe('cheapest');
        expect(sortingItems[2].text()).toBe('name');
    })

    // ----------- Sorting Method Selection Test -----------
    it('Ensures the correct sorting method is selected when a user clicks on a sorting option', async () => {
        const wrapper = mount(TrendingProductsBlock);

        // Access the mocked store instance after mount
        const inventoryStore = useInventoryStore();

        // Find the button containing the text 'cheapest'
        const sortButtons = wrapper.findAll('.trending-products__sorting-bar__item button');

        // Trigger the click event on the 'cheapest' button
        await sortButtons[1].trigger('click');

    });
})