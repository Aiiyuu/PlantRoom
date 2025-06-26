/**
 * @file FilterBar.spec.ts
 * @description
 * This file contains unit tests for the `FilterBar.vue` component using Vitest and Vue Test Utils.
 *
 * The `FilterBar` component provides product filtering options:
 * - Price range selection through the embedded `PriceFilter` component.
 * - Boolean filters for "in stock" and "on discount" using checkboxes.
 * - A reset button that resets all filters via the store's resetFilters method.
 *
 * The tests cover:
 * 1. Rendering of the component and its child PriceFilter.
 * 2. Proper two-way binding between checkbox inputs and the store's filter state.
 * 3. Behavior of the reset button triggering the store's resetFilters method.
 */

import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { setActivePinia, createPinia } from 'pinia'
import FilterBar from '@/pages/Catalog/FilterBar.vue'
import PriceFilter from '@/pages/Catalog/PriceFilter.vue'
import { useInventoryStore } from "@/stores/inventory"

// Define a mock store object outside
const mockStore = {
    filter: {
        in_stock: false,
        on_discount: false,
        price: { min: 0, max: 100 },
    },
    resetFilters: vi.fn(),
}

// Mock the module to always return the same mockStore instance
vi.mock('@/stores/inventory', () => ({
    useInventoryStore: () => mockStore,
}))


describe('FilterBar.vue', () => {
    let wrapper: ReturnType<typeof mount>
    let store: ReturnType<typeof useInventoryStore>

    beforeEach(() => {
        setActivePinia(createPinia())
        store = useInventoryStore()

        // Reset store state before each test
        store.filter.in_stock = false
        store.filter.on_discount = false
        vi.clearAllMocks()

        wrapper = mount(FilterBar)
    })

    // ----------- Verify that the Filter component renders with PriceFilter child and relevant checkboxes -----------
    it('renders the Filter component and PriceFilter child', () => {
        // Check if the PriceFilter child component is rendered inside the wrapper
        expect(wrapper.findComponent(PriceFilter).exists()).toBe(true)

        // Find checkboxes for "in stock" and "on discount" filters by their IDs
        const inStockCheckbox = wrapper.find('#in-stock')
        const onDiscountCheckbox = wrapper.find('#on-discount')

        // Verify that both checkboxes exist in the component
        expect(inStockCheckbox.exists()).toBe(true)
        expect(onDiscountCheckbox.exists()).toBe(true)
    })

    // ----------- Verify that the filter checkboxes are bound to the store and update store values on user interaction -----------
    it('checkboxes are bound to store filter values and update on interaction', async () => {
        // Find the checkboxes for "in stock" and "on discount" filters
        const inStockCheckbox = wrapper.find('#in-stock')
        const onDiscountCheckbox = wrapper.find('#on-discount')

        // Assert initial checkbox states match the store filter values
        expect(inStockCheckbox.element.checked).toBe(store.filter.in_stock)
        expect(onDiscountCheckbox.element.checked).toBe(store.filter.on_discount)

        // Simulate checking the "in stock" checkbox, store value should update to true
        await inStockCheckbox.setChecked(true)
        expect(store.filter.in_stock).toBe(true)

        // Simulate checking the "on discount" checkbox, store value should update to true
        await onDiscountCheckbox.setChecked(true)
        expect(store.filter.on_discount).toBe(true)
    })

    // ----------- Verify that triggering the form reset event calls the store's resetFilters action -----------
    it('clicking reset button calls store.resetFilters', async () => {
        // Find the form element wrapping the filters
        const form = wrapper.find('form')

        // Trigger the form's reset event (this simulates clicking the reset button in a form)
        await form.trigger('reset')

        // Expect the store.resetFilters method to have been called
        expect(store.resetFilters).toHaveBeenCalled()
    })
})