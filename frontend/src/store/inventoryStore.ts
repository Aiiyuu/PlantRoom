
import { defineStore } from 'pinia'
import axios, { AxiosResponse } from 'axios'

export interface Plant {
    id:number,
    name: string,
    description: string,
    price: number,
    discount_percentage: number,
    stock_count: number,
    rating: number,
    image: string,
}

// Discounted price and isInstock

export const useInventoryStore = defineStore('inventory', {
    state: () => ({
        inventory: [] as Plant[],
        sortMethod: 'rating',
        isLoading: false,
        error: null as string | null
    }),

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
        }
    }
})