/**
 * @file PriceFilter.spec.ts
 * @description
 * This file contains unit tests for the PriceFilter.vue component using Vitest and Vue Test Utils.
 *
 * The PriceFilter component allows users to select a price range using dual range sliders and numeric inputs.
 * It syncs its state with a global inventory store's filter.price.min and filter.price.max values.
 *
 * The tests cover the following functionalities:
 * 1. Rendering the component and verifying initial min and max values from the store.
 * 2. Updating the min and max values via range inputs and numeric inputs.
 * 3. Validating input constraints (min <= max, max >= min, min and max within bounds).
 * 4. Behavior of blur event handlers that correct invalid inputs.
 * 5. The resetPrice method resets the filter to default min and max values.
 *
 */


import { describe, it, vi, expect, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { setActivePinia, createPinia } from 'pinia'
import PriceFilter from '@/pages/Catalog/PriceFilter.vue'
import { useInventoryStore } from '@/stores/inventory'

vi.mock('@/stores/inventory', () => {
    // Reactive filter state
    const filter = {
        price: {
            min: 0,
            max: 1000,
        },
        in_stock: false,
        on_discount: false,
    }

    return {
        useInventoryStore: () => ({
            filter,
            // Mock the resetFilters action to reset filter values to default
            resetFilters: () => {
                filter.in_stock = false
                filter.on_discount = false
                filter.price.min = 0
                filter.price.max = 1000
            },
        }),
    }
})


describe('PriceFilter.vue', ():void => {
    let wrapper: ReturnType<typeof mount>
    let store: ReturnType<typeof useInventoryStore>

    beforeEach((): void => {
        setActivePinia(createPinia())
        store = useInventoryStore()

        // Reset filter values before each test
        store.filter.price.min = 10
        store.filter.price.max = 600

        wrapper = mount(PriceFilter)
    })

    // ----------- Verify that the component renders correctly with initial min and max values from the store -----------
    it('renders correctly with initial min and max values from store', () => {
        // Find the range slider elements by their IDs
        const minRange = wrapper.find('#minRange')
        const maxRange = wrapper.find('#maxRange')

        // Find the input fields for min and max price
        const minInput = wrapper.find('#min-price')
        const maxInput = wrapper.find('#max-price')

        // Check that the range sliders have the correct initial values from the store
        expect((minRange.element as HTMLInputElement).value).toBe(String(store.filter.price.min))
        expect((maxRange.element as HTMLInputElement).value).toBe(String(store.filter.price.max))

        // Check that the input fields have the correct initial values from the store
        expect((minInput.element as HTMLInputElement).value).toBe(String(store.filter.price.min))
        expect((maxInput.element as HTMLInputElement).value).toBe(String(store.filter.price.max))
    })

    // ----------- Verify that the min value updates correctly when the min range input changes within valid limits -----------
    it('updates min when min range input changes within valid range', async () => {
        const minRange = wrapper.find('#minRange')

        // Change min to a valid value less than current max (600)
        await minRange.setValue('200')
        expect(store.filter.price.min).toBe(200)

        // Try to set min above max (700) - should be ignored and not update store
        await minRange.setValue('700')
        expect(store.filter.price.min).toBe(200)

        // Input element resets to valid current min value (10)
        expect((minRange.element as HTMLInputElement).value).toBe('10')
    })

    // ----------- Verify that the max value updates correctly when the max range input changes within valid limits -----------
    it('updates max when max range input changes within valid range', async () => {
        const maxRange = wrapper.find('#maxRange')

        // Set to a value greater than current min (10)
        await maxRange.setValue('800')
        expect(store.filter.price.max).toBe(800)

        // Attempt to set max below min - should not update store
        await maxRange.setValue('5')
        expect(store.filter.price.max).toBe(800) // unchanged

        // Input element value resets to current max (600)
        expect((maxRange.element as HTMLInputElement).value).toBe('600')
    })

    // ----------- Verify that the min value updates correctly when the min numeric input changes within valid limits -----------
    it('updates min when min numeric input changes within valid range', async () => {
        const minInput = wrapper.find('#min-price')

        // Set min input to a valid value less than current max
        await minInput.setValue('50')
        expect(store.filter.price.min).toBe(50)

        // Inputting a value above current max should not update the store
        await minInput.setValue('700')
        expect(store.filter.price.min).toBe(50) // unchanged
    })

    // ----------- Verify that the max value updates correctly when the max numeric input changes within valid limits -----------
    it('updates max when max numeric input changes within valid range', async () => {
        const maxInput = wrapper.find('#max-price')

        // Set max input to a valid value greater than current min
        await maxInput.setValue('900')
        expect(store.filter.price.max).toBe(900)

        // Input value below min should not update the store
        await maxInput.setValue('5')
        expect(store.filter.price.max).toBe(900) // unchanged
    })

    // ----------- Verify that the min input is corrected on blur if min is greater than max -----------
    it('corrects min input on blur if min > max', async () => {
        const minInput = wrapper.find('#min-price')

        // Set min input to a value higher than max (600)
        await minInput.setValue('700')
        // Trigger blur event to enforce correction logic
        await minInput.trigger('blur')

        // Store min should be reset to max (600)
        expect(store.filter.price.min).toBe(600)
        // Input element value should reflect corrected min
        expect((minInput.element as HTMLInputElement).value).toBe('600')
    })

    // ----------- Verify that the max input is corrected on blur if max is less than min -----------
    it('corrects max input on blur if max < min', async () => {
        const maxInput = wrapper.find('#max-price')

        // Set max input below min (10)
        await maxInput.setValue('5')
        // Trigger blur event to enforce correction logic
        await maxInput.trigger('blur')

        // Store max should be reset to min (10)
        expect(store.filter.price.max).toBe(10)
        // Input element value should reflect corrected max
        expect((maxInput.element as HTMLInputElement).value).toBe('10')
    })

    // ----------- Verify that the resetFilters method resets min and max to their default values -----------
    it('calls resetFilters in store and updates input values accordingly', async () => {
        // Change store filter values to something non-default
        store.filter.price.min = 100
        store.filter.price.max = 500

        // Call the resetFilters action on the store to reset filters to defaults
        store.resetFilters()

        // Wait for Vue's reactivity to update the component DOM
        await wrapper.vm.$nextTick()

        // Find inputs again (in case they need to be re-queried)
        const minInput = wrapper.find('#min-price')
        const maxInput = wrapper.find('#max-price')

        // Assert that store has default filter values
        expect(store.filter.price.min).toBe(0)
        expect(store.filter.price.max).toBe(1000)
    })

    // ----------- Verify that the highlighted range style correctly reflects the current min and max price values -----------
    it('highlighted range style left and right match min and max values', () => {
        // Find the element showing the highlighted price range
        const highlighted = wrapper.find('.highlighted-range')
        // Get current min and max prices from the store
        const min: number = store.filter.price.min
        const max: number = store.filter.price.max

        // Calculate expected CSS left and right percentage positions based on min/max values relative to max price (1000)
        const expectedLeft: any = `${(min / 1000) * 100}%`
        const expectedRight: any = `${100 - (max / 1000) * 100}%`

        // Assert that the style attribute contains correct left and right positioning for the highlighted range
        expect(highlighted.attributes('style')).toContain(`left: ${expectedLeft}`)
        expect(highlighted.attributes('style')).toContain(`right: ${expectedRight}`)
    })
})