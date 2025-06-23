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
 * 6. Verify that a "no items" message is displayed when the inventory is empty and loading is false. *
 *
 * The tests use mocked store data to simulate different inventory and loading states, and validate that the component
 * behaves as expected in these scenarios.
 */

import { mount } from '@vue/test-utils'
import { setActivePinia, createPinia } from "pinia"
import { beforeEach, describe, it, expect, vi } from "vitest"
import TrendingProductsBlock from '@/pages/Home/TrendingProductsBlock.vue'
import PlantCard from '@/components/ui/PlantCard.vue'
import { useInventoryStore } from "@/store/inventoryStore"
import Plant from '@/types/PlantInterface'

// Mock response data
const mockPlants: Plant[] = [
    {
        id: 1,
        name: 'Aloe Vera',
        description: 'Aloe Vera is a succulent plant known for its medicinal properties.',
        price: 10,
        discount_percentage: 10,
        discounted_price: 9,
        stock_count: 25,
        in_stock: true,
        rating: 2,
        image: 'https://example.com/images/aloe-vera.jpg',
    },
    {
        id: 2,
        name: 'Snake Plant',
        description: 'Snake Plant is a hardy, low-maintenance indoor plant.',
        price: 15,
        discount_percentage: 0,
        discounted_price: null,
        stock_count: 0,
        in_stock: false,
        rating: 5,
        image: 'https://example.com/images/snake-plant.jpg',
    }
]

describe('TrendingProductsBlock.vue', (): void => {
    beforeEach(() => {
        setActivePinia(createPinia())
        vi.clearAllMocks()
    })

    // ----------- Render Tests -----------
    it('renders the title and sorting options correctly', async () => {
        // Mount the TrendingProductsBlock component for testing
        const wrapper = mount(TrendingProductsBlock)
        const store = useInventoryStore()

        // Make sure the inventory state is not empty
        store.inventory = [ ...mockPlants ]

        // Wait for Vue to update
        await wrapper.vm.$nextTick()

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
    it('ensures the correct sorting method is selected when a user clicks on a sorting option', async () => {
        const wrapper = mount(TrendingProductsBlock)

        // Access the mocked store instance after mount
        const store = useInventoryStore()

        // Make sure the inventory state is not empty
        store.inventory = [ ...mockPlants ]

        // Wait for Vue to update
        await wrapper.vm.$nextTick()

        // Find the sorting buttons
        const sortButtons = wrapper.findAll('.trending-products__sorting-bar__item button')
        expect(sortButtons.length).toBe(3) // Ensure sorting buttons exist

        // Trigger the click event on the 'cheapest' button
        await sortButtons[1].trigger('click')

        // Ensure that the `sortMethod` is updated and set to 'cheapest'
        expect(store.sortMethod).toBe('cheapest')
    })

    // ----------- Verify that the store's `updateSortMethod` is called when the sorting method is changed -----------
    it("verify that the store's `updateSortMethod` is called after changing the sorting method", async () => {
        // Mount the TrendingProductsBlock component for testing
        const wrapper = mount(TrendingProductsBlock);
        const store = useInventoryStore();

        // Make sure the inventory state is not empty
        store.inventory = [ ...mockPlants ]

        // Wait for Vue to update
        await wrapper.vm.$nextTick()

        // Spy on the store's method
        const spy = vi.spyOn(store, 'updateSortMethod')

        // Find the sorting buttons
        const sortButtons = wrapper.findAll('.trending-products__sorting-bar__item button');
        // Trigger the click event on the 'name' button
        await sortButtons[2].trigger('click');

        // Ensure that the `sortMethod` is updated and set to 'name'
        expect(store.sortMethod).toBe('name')

        // Assert the method was called with the correct argument
        expect(spy).toHaveBeenCalled()
        expect(spy).toHaveBeenCalledWith('name')
    })

    // ----------- Make sure the carousel is working correctly -----------
    it('scrolls the carousel correctly when navigation buttons are clicked', async () => {
        const wrapper = mount(TrendingProductsBlock, {
            attachTo: document.body, // Required to measure layout dimensions correctly
        })

        const store = useInventoryStore()

        // Provide mock inventory with proper Plant structure
        store.inventory = Array.from({ length: 10 }, (_, i) => ({
            id: i + 1,
            name: `Plant ${i + 1}`,
            description: `Description for Plant ${i + 1}`,
            price: 10 + i,
            discount_percentage: 0,
            discounted_price: null,
            stock_count: 5,
            in_stock: true,
            rating: 4.5,
            image: `/images/plant${i + 1}.jpg`,
        }))

        await wrapper.vm.$nextTick()

        // Retrieve the carousel window and inner container elements
        const carouselInner = wrapper.vm.carouselInner as HTMLElement
        const carouselWindow = wrapper.vm.carouselWindow as HTMLElement

        // Mock layout dimensions
        Object.defineProperty(carouselWindow, 'offsetWidth', { value: 700 }) // Fits ~3 cards
        const firstChild = carouselInner.firstElementChild as HTMLElement;
        Object.defineProperty(firstChild, 'offsetWidth', { value: 230 })

        // Mock getComputedStyle to include margin-right: 40px
        vi.spyOn(window, 'getComputedStyle').mockReturnValue({
            width: '230px',
            marginRight: '40px',
        } as any)

        const nextBtn = wrapper.find('.trending-products__carousel__navigation__item.next')
        const prevBtn = wrapper.find('.trending-products__carousel__navigation__item.prev')

        // Scroll forward (230 + 40 = 270px)
        await nextBtn.trigger('click')
        expect(carouselInner.style.transform).toContain('translateX(-270px)')

        // Scroll forward again
        await nextBtn.trigger('click')
        expect(carouselInner.style.transform).toContain('translateX(-540px)')

        // Scroll backward
        await prevBtn.trigger('click')
        expect(carouselInner.style.transform).toContain('translateX(-270px)')

        // Scroll back to the start
        await prevBtn.trigger('click')
        expect(carouselInner.style.transform).toContain('translateX(-0px)')
    })

    // ----------- Verify that a PlantCard component is rendered for each inventory item -----------
    it('renders a PlantCard component for each inventory item', async () => {
        // Mount the TrendingProductsBlock component fot testing
        const wrapper = mount(TrendingProductsBlock)
        const store = useInventoryStore()

        // Mock inventory with 5 items
        store.inventory = Array.from({ length: 5 }, (_, i) => ({
            id: i + 1,
            name: `Plant ${i + 1}`,
            description: `Description for Plant ${i + 1}`,
            price: 10 + i,
            discount_percentage: 0,
            discounted_price: null,
            stock_count: 5,
            in_stock: true,
            rating: 4.5,
            image: `/images/plant${i + 1}.jpg`,
        }))

        await wrapper.vm.$nextTick()

        // Find all PlantCard components rendered
        const plantCards = wrapper.findAllComponents(PlantCard)

        // Assert the number of PlantCards equals inventory length
        expect(plantCards).toHaveLength(store.inventory.length);
    })

    // ----------- Verify that a "no items" message is shown when inventory is empty and loading is false -----------
    it('shows no items message when inventory is empty and loading is false', async () => {
        // Mount the TrendingProductsBlock component for testing
        const wrapper = mount(TrendingProductsBlock);
        const store = useInventoryStore()

        // Make sure that isLoading is set to false and the inventory state is empty
        store.isLoading = false;
        store.inventory = [];


        // Make sure the appropriate message is shown
        expect(wrapper.text()).toContain('No plants available')

        // Check that the sorting bar is not displayed (v-if="inventoryStore.inventory?.length")
        const sortingBar = wrapper.find('.trending-products__sorting-bar');
        expect(sortingBar.exists()).toBe(false);

        // Check that the carousel is not displayed (v-if="inventoryStore.inventory?.length")
        const carousel = wrapper.find('.trending-products__carousel');
        expect(carousel.exists()).toBe(false);
    });
})