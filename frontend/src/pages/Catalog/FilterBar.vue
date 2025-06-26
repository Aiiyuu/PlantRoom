<template>
    <div class="filter">
        <form class="filter__wrapper" @reset.prevent="store.resetFilters()">
            <div>
                <h1 class="filter__wrapper__title">Filter products</h1>

                <PriceFilter />

                <hr>

                <div>
                    <div class="filter__wrapper__checkbox-field mb-4">
                        <label for="in-stock">In stock</label>
                        <input id="in-stock" type="checkbox" v-model="inStock" />
                    </div>

                    <div class="filter__wrapper__checkbox-field">
                        <label for="on-discount">On discount</label>
                        <input id="on-discount" type="checkbox" v-model="onDiscount" />
                    </div>
                </div>
            </div>


            <button type="reset" class="filter__wrapper__reset">Reset</button>
        </form>
    </div>
</template>

<script lang="ts" setup>
import { ref, computed } from "vue"
import PriceFilter from "@/pages/Catalog/PriceFilter.vue"
import { useInventoryStore } from '@/stores/inventory'

// Access your Pinia inventory store instance
const store = useInventoryStore()

// Computed property for two-way binding with 'in_stock' filter in the store:
// - Getter: returns the current 'in_stock' value from the Pinia store
// - Setter: updates the 'in_stock' value in the store when input changes
const inStock = computed({
    get: () => store.filter.in_stock,
    set: (val: boolean) => {
        store.filter.in_stock = val
    }
})

// Computed property for two-way binding with 'on_discount' filter in the store:
// - Getter: returns the current 'on_discount' value from the Pinia store
// - Setter: updates the 'on_discount' value in the store when input changes
const onDiscount = computed({
    get: () => store.filter.on_discount,
    set: (val: boolean) => {
        store.filter.on_discount = val
    }
})
</script>

<style lang="scss" scoped>
 .filter {
     &__wrapper {
         @apply bg-gray-50 border-2 border-gray-200 rounded-xl px-4 py-8 md:w-[350px] h-full text-dark
            flex flex-col justify-between;

         &__title {
             @apply text-2xl text-dark font-medium;
         }

         &__checkbox-field {
             @apply flex flex-row-reverse items-center justify-end w-full;

             label {
                 @apply ml-4 my-0 select-none;
             }

             input {
                 @apply w-5 h-5 accent-dark;
             }
         }

         &__reset {
             @apply bg-dark text-white py-2 px-8 hover:bg-gray-600 duration-300 ease-out rounded-xl;
         }

         & > div > * {
             @apply mb-8;

             &:last-child {
                 @apply mb-0;
             }
         }
     }
 }
</style>