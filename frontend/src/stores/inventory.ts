
import { defineStore } from 'pinia'
import Plant from '@/types/PlantInterface'
import axios, { AxiosResponse } from 'axios'

export const useInventoryStore = defineStore('inventory', {
    state: () => ({
        inventory: [] as Plant[],
        sortMethod: 'rating',
        isLoading: false,
        error: null as string | null,

        filter: {
            in_stock: false,
            on_discount: false,
            price: {
                min: 0,
                max: 1000,
            }
        }
    }),

    getters: {
        /**
         * Returns the list of inventory items after applying all active filters.
         */
        filteredInventory(state): Plant[] {
            return state.inventory.filter((plant) => {
                // Apply in-stock filter only if it's enabled
                const inStockFilter = !state.filter.in_stock || plant.in_stock

                // Apply on-discount filter only if it's enabled
                const onDiscountFilter = !state.filter.on_discount || plant.discount_percentage > 0

                // Apply price filters (always applied)
                const minPriceFilter = plant.price >= state.filter.price.min
                const maxPriceFilter = plant.price <= state.filter.price.max

                // Return true only if the plant satisfies all filters
                return inStockFilter && onDiscountFilter && minPriceFilter && maxPriceFilter
            })
        },

        /**
         * Returns filtered items sorted by the selected sort method (e.g. price, rating, name).
         */
        sortedFilteredInventory(state): Plant[] {
            const filtered = this.filteredInventory
            const sortMethod = state.sortMethod
            const sorted = [...filtered] // Copy to avoid mutating original

            switch (true) {
                case sortMethod === 'Low to High':
                    return sorted.sort((a, b) => a.price - b.price)

                case sortMethod === 'High to Low':
                    return sorted.sort((a, b) => b.price - a.price)

                case sortMethod === 'Top Rated':
                    return sorted.sort((a, b) => b.rating - a.rating)

                case sortMethod === 'Lowest Rated':
                    return sorted.sort((a, b) => a.rating - b.rating)

                case sortMethod === 'A to Z':
                    return sorted.sort((a, b) => a.name.localeCompare(b.name))

                case sortMethod === 'Z to A':
                    return sorted.sort((a, b) => b.name.localeCompare(a.name))

                default:
                    return sorted
            }
        }
    },

    actions: {
        /**
         * Fetch a list of inventory items from the API endpoint.
         */
        async fetchInventory(): Promise<void> {
            // Reset the isLoading and error states before fetching data
            this.isLoading = true
            this.error = null

            try {
                const response: AxiosResponse<Plant[]> = await axios('inventory')
                this.inventory = response.data // Update the inventory array
            } catch (error: unknown) {
                // Type assertion to tell TypeScript that error is an instance of Error
                if (error instanceof Error) {
                    this.error = error.message || 'Failed to load inventory.';
                } else {
                    // Handle other cases where error may not be an instance of Error
                    this.error = 'Failed to load inventory.';
                }
            } finally {
                this.isLoading = false
            }
        },

        /**
         * Sort inventory based on the current sort method.
         */
        sortInventory(): void {
            const sortMethod = this.sortMethod
            const sortedInventory = [...this.inventory] // Create a shallow copy to avoid mutation

            switch (sortMethod) {
                case 'featured':
                    this.inventory = sortedInventory.sort((a, b) => b.rating - a.rating) // Descending order
                    break
                case 'cheapest':
                    this.inventory = sortedInventory.sort((a, b) => a.price - b.price) // Ascending order
                    break
                case 'name':
                    this.inventory = sortedInventory.sort((a, b) => a.name.localeCompare(b.name)); // Ascending order
                    break
                default:
                    break
            }
        },

        /**
         * Updates the sorting method used in the component.
         *
         * @param sortMethod - A string representing the new sorting method.
         * This value will be assigned to the `sortMethod` property of the class.
         */
        updateSortMethod(sortMethod: string): void {
            this.sortMethod = sortMethod
            this.sortInventory() // Re-sort inventory when sortMethod changes
        },

        /**
         * Reset all filter values to their initial defaults
         */
        resetFilters(): void {
            this.filter = {
                in_stock: false,
                on_discount: false,
                price: {
                    min: 0,
                    max: 1000,
                },
            }
        }
    }
})