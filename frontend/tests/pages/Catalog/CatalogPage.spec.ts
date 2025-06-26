/**
 * @file Catalog.spec.ts
 * @description
 * This file contains unit tests for the `Catalog.vue` component using Vitest and Vue Test Utils.
 *
 * The `Catalog` component displays a list of plants with sorting and filtering capabilities:
 * - Shows the count of displayed plants and total inventory.
 * - Allows sorting via a dropdown with several methods.
 * - Displays applied filters with clickable "remove" actions.
 * - Renders a list of `PlantCard` components or a "No plants available" message.
 *
 * The tests cover:
 * 1. Rendering counts based on store data.
 * 2. Rendering and selecting sort options.
 * 3. Display and functionality of applied filters removing.
 * 4. Conditional rendering of plant cards or no data message.
 * 5. Calls to store methods such as fetching inventory and updating sort.
 */

import { mount } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { nextTick } from "vue"
import CatalogPage from '@/pages/Catalog/CatalogPage.vue'
import Plant from '@/types/PlantInterface'
import { createPinia, setActivePinia } from 'pinia'
import { useInventoryStore } from '@/stores/inventory'

// Mock PlantCard component (simplify)
vi.mock('@/components/ui/PlantCard.vue', () => ({
    default: {
        template: '<div class="plant-card-mock">{{ plant.id }}</div>',
        props: ['plant', 'isLoading'],
    },
}))

describe('Catalog.vue', () => {
    let inventoryStore: ReturnType<typeof useInventoryStore>
    let wrapper: ReturnType<typeof mount>

    beforeEach(() => {
        setActivePinia(createPinia())
        inventoryStore = useInventoryStore()

        // Mock fetchInventory to avoid real API calls
        vi.spyOn(inventoryStore, 'fetchInventory').mockResolvedValue(undefined)
        // Spy on updateSortMethod without changing state (test separately by setting state)
        vi.spyOn(inventoryStore, 'updateSortMethod')

        // Setup mock inventory data for tests
        inventoryStore.inventory = [
            {
                id: 1,
                name: 'Plant A',
                description: 'A lovely plant A',
                price: 20,
                discount_percentage: 10,
                discounted_price: 18,
                stock_count: 15,
                in_stock: true,
                rating: 4.5,
                image: 'plant-a.jpg',
            },
            {
                id: 2,
                name: 'Plant B',
                description: 'A lovely plant B',
                price: 30,
                discount_percentage: 0,
                discounted_price: null,
                stock_count: 0,
                in_stock: false,
                rating: 3.8,
                image: 'plant-b.jpg',
            },
            {
                id: 3,
                name: 'Plant C',
                description: 'A lovely plant C',
                price: 25,
                discount_percentage: 5,
                discounted_price: 23.75,
                stock_count: 5,
                in_stock: true,
                rating: 4.0,
                image: 'plant-c.jpg',
            },
        ] as Plant[]

        // Reset filters and sorting method to default state
        inventoryStore.filter = {
            price: { min: 0, max: 1000 },
            in_stock: false,
            on_discount: false,
        }
        inventoryStore.sortMethod = 'Top Rated'

        // Mount the CatalogPage component
        wrapper = mount(CatalogPage)
    })

    // ----------- Verify that the component renders counts of displayed plants and total inventory correctly -----------
    it('renders counts of displayed plants and total inventory', () => {
        expect(wrapper.find('.catalog__navigation').text())
            .toContain(`Showing ${inventoryStore.filteredInventory.length} results from total ${inventoryStore.inventory.length}`)
    })

    // ----------- Verify that the component renders the sort dropdown and allows changing sort methods -----------
    it('renders and allows changing sort methods', async () => {
        const select = wrapper.find('select')

        // Ensure the sort select dropdown exists
        expect(select.exists()).toBe(true)

        // Default selected value is first sort method 'Top Rated'
        expect((select.element as HTMLSelectElement).value).toBe('Top Rated')

        // Change selection to 'Low to High'
        await select.setValue('Low to High')

        // updateSortMethod should be called with the new sort method
        expect(inventoryStore.updateSortMethod).toHaveBeenCalledWith('Low to High')
    })

    // ----------- Verify that the component renders applied filters and allows removing them -----------
    it('renders applied filters and allows removing them', async () => {
        // Set filters so they appear in the UI
        inventoryStore.filter.price = { min: 10, max: 200 }
        inventoryStore.filter.in_stock = true
        inventoryStore.filter.on_discount = true

        // Wait again if needed after mount for DOM updates
        await nextTick()

        // Applied filters list items should be 3
        const filterItems = wrapper.findAll('.catalog__navigation__applied-filters ul li')
        expect(filterItems.length).toBe(3)

        // Click price filter item to reset price filter to default values
        await filterItems[0].trigger('click')
        expect(inventoryStore.filter.price.min).toBe(0)
        expect(inventoryStore.filter.price.max).toBe(1000)

        // Click in_stock filter item to disable the filter
        await filterItems[1].trigger('click')
        expect(inventoryStore.filter.in_stock).toBe(false)

        // Click on_discount filter item to disable the filter
        await filterItems[2].trigger('click')
        expect(inventoryStore.filter.on_discount).toBe(false)
    })

    // ----------- Verify that the component renders PlantCard components for each plant in filtered inventory -----------
    it('renders PlantCard components when plants are available', () => {
        // PlantCard is mocked, but should render one per plant in filtered inventory
        const plantCards = wrapper.findAll('.plant-card-mock')

        // Check if the number of rendered PlantCard mocks matches filtered inventory length
        expect(plantCards.length).toBe(inventoryStore.filteredInventory.length)
    })

    // ----------- Verify that the component shows a message when no plants are available -----------
    it('renders no plants available message when no plants are available', async () => {
        // Clear inventory to simulate no available plants
        inventoryStore.inventory = []

        await nextTick()

        // Check that the no plants available message is rendered
        expect(wrapper.text()).toContain('No plants available')
    })

    // ----------- Verify that fetchInventory is called when the component is mounted -----------
    it('calls fetchInventory on mounted', () => {
        // Ensure fetchInventory was called on mount
        expect(inventoryStore.fetchInventory).toHaveBeenCalled()
    })
})