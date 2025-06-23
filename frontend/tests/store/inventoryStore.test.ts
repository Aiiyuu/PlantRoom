/**
 * @file inventoryStore.test.ts
 * @description
 * This file contains unit tests for the `inventoryStore` Pinia store using Vitest.
 *
 * The `inventoryStore` manages the inventory of plant products, including loading state,
 * error handling, and sorting functionality. It fetches data from an external API
 * and allows users to sort inventory by rating, price, or name.
 *
 * The tests cover the following functionalities:
 * 1. Verifying the store initializes with the correct default state.
 * 2. Ensuring that `fetchInventory` correctly updates state on success.
 * 3. Testing error handling when `fetchInventory` fails.
 * 4. Confirming that `sortInventory` correctly sorts the inventory based on the selected sort method.
 * 5. Verifying that `updateSortMethod` updates the sort method and triggers re-sorting.
 *
 * Axios is mocked to simulate API success and failure scenarios. Test data is used to validate
 * sorting behavior for different methods (`featured`, `cheapest`, `name`).
 */


import { createPinia, setActivePinia } from 'pinia'
import { beforeEach, expect, describe, test, vi } from 'vitest'
import axios from 'axios'
import Plant from '@/types/PlantInterface'

vi.mock('axios')

const mockedAxios = axios as unknown as {
    default: { mockResolvedValue: (value: any) => void }
}

import { useInventoryStore } from '@/store/inventoryStore'


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


describe('InventoryStore', () => {
    beforeEach(() => {
        setActivePinia(createPinia())
        vi.clearAllMocks()
    })


    // --------- Verify that the store initializes with the correct default state ---------
    test('initializes store with correct default state', () => {
        const inventory = useInventoryStore()

        // Ensure the isLoading state is false by default
        expect(inventory.isLoading).toBe(false)

        // Ensure the inventory array is initially empty
        expect(inventory.inventory).toHaveLength(0)

        // Ensure the error state is null by default
        expect(inventory.error).toBeNull()

        // Ensure the default sorting method is set to 'rating'
        expect(inventory.sortMethod).toBe('rating')
    })

    // --------- Ensures fetchInventory sets loading state, populates inventory, and clears errors on success ---------
    test('fetchInventory correctly updates state on success', async () => {
        const store = useInventoryStore()

        // Set mock implementation
        mockedAxios.default.mockResolvedValue({ data: mockPlants })

        // Now call fetch method
        await store.fetchInventory()

        // Assert expected results
        expect(store.inventory).toEqual(mockPlants)
        expect(store.isLoading).toBe(false)
        expect(store.error).toBeNull()
    })

    // -------- Ensure fetchInventory correctly handles case if something went wrong --------
    test('fetchInventory sets error state on failure', async () => {
        const store = useInventoryStore()

        // Simulate Axios throwing an error
        const errorMessage = 'Network Error'
        const error = new Error(errorMessage)

        // Mock Axios to reject
        const mockedAxios = axios as unknown as {
            default: { mockRejectedValue: (error: unknown) => void }
        }

        mockedAxios.default.mockRejectedValue(error)

        // Run store fetch
        await store.fetchInventory()


        // Assertions
        expect(store.inventory).toEqual([])       // Should still be empty
        expect(store.isLoading).toBe(false)       // Should be false after attempt
        expect(store.error).toBe(errorMessage)    // Error message should be set
    })

    // -------- Ensure the `sortInventory` correctly sorts the inventory based on the provided sort method ---------
    test('sortInventory correctly updates sorts the inventory', () => {
        const store = useInventoryStore()

        // Update the inventory state and the sortMethod state
        store.inventory = [ ...mockPlants ]
        store.sortMethod = 'featured'

        // Create own sorted inventory list by rating (featured)
        const sortedByRatingDesc = [...mockPlants].sort((a, b) => b.rating - a.rating)

        // Verify that sortInventory returns the expected sortedByRatingDesc result
        store.sortInventory()
        expect(store.inventory).toEqual(sortedByRatingDesc)
    })

    // -------- Ensure `updateSortMethod` updates `sortMethod` and re-sorts the inventory ---------
    test('updateSortMethod updates sortMethod and re-sorts the inventory', () => {
        const store = useInventoryStore()

        // Update the inventory state by inserting plant objects
        store.inventory = [ ...mockPlants ]

        // Update sort method to 'cheapest' (which should sort by price ascending)
        store.updateSortMethod('cheapest')

        // Verify the sortMethod state was updated
        expect(store.sortMethod).toBe('cheapest')

        // Create a sorted inventory list by price (ascending)
        const expectedSorted = [...mockPlants].sort((a, b) => a.price - b.price)

        // Verify that the inventory list matches the expected sorted order
        expect(store.inventory).toEqual(expectedSorted)
    })
})