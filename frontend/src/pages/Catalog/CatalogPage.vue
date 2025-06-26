<template>
    <div class="catalog">
        <div class="catalog__navigation">
            <div>
                <h4>
                    Showing
                    <span>{{ displayedPlants.length }}</span>
                    results from total
                    <span>{{ inventoryStore.inventory.length }}</span>
                </h4>

                <!-- Sort dropdown -->
                <form @submit.prevent>
                    <select v-model="selectedSort" @change="onSortChange">
                        <option
                            v-for="(method, index) in sortMethods"
                            :key="method"
                            :value="method"
                            :selected="index === 0"
                        >
                            {{ method }}
                        </option>
                    </select>
                </form>
            </div>

            <div class="catalog__navigation__applied-filters">
                <span>
                    <h4>Applied filters:</h4>
                </span>

                <ul>
                    <li
                        v-if="inventoryStore.filter.price.min > 0 || inventoryStore.filter.price.max < 1000"
                        @click="() => {
                            inventoryStore.filter.price.min = 0;
                            inventoryStore.filter.price.max = 1000;
                        }"
                    >
                        ${{ inventoryStore.filter.price.min }} - ${{ inventoryStore.filter.price.max }}
                        <span class="close-button"></span>
                    </li>

                    <li v-if="inventoryStore.filter.in_stock" @click="() => inventoryStore.filter.in_stock = false">
                        In stock
                        <span class="close-button"></span>
                    </li>

                    <li v-if="inventoryStore.filter.on_discount" @click="() => inventoryStore.filter.on_discount = false">
                        On discount
                        <span class="close-button"></span>
                    </li>
                </ul>
            </div>
        </div>

        <TransitionGroup
            v-if="displayedPlants.length"
            name="list"
            tag="div"
            class="catalog__card-list"
        >
            <div
                class="catalog__card-list__item"
                v-for="item in displayedPlants"
                :key="item.id"
            >
                <PlantCard :plant="item" :isLoading="false" />
            </div>
        </TransitionGroup>
        <div v-else class="catalog__no-available">
            <h1>No plants available</h1>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { computed, onMounted, ref } from 'vue'
import { useInventoryStore } from "@/stores/inventory"
import PlantCard from "@/components/ui/PlantCard.vue"

const inventoryStore = useInventoryStore()

// A computed value that always reflects the current list of plants after all active filters are applied
const displayedPlants = computed(() => inventoryStore.sortedFilteredInventory)

// List of sort methods with friendly names + old keys mapped in the store
const sortMethods = [
    'Top Rated', 'Lowest Rated', 'Low to High',
    'High to Low', 'Z to A', 'A to Z',
]

// Reactive variable for selected sort
const selectedSort = ref(sortMethods[0])

// Update store's sortMethod and trigger sorting when dropdown changes
function onSortChange() {
    inventoryStore.updateSortMethod(selectedSort.value)
}

onMounted(() => {
    // Fetch date from the inventory API endpoint
    inventoryStore.fetchInventory()
})
</script>

<style lang="scss" scoped>
/* Add these outside of your BEM structure */
.list-enter-active,
.list-leave-active {
    transition: all 0.3s ease;
}

.list-enter-from,
.list-leave-to {
    opacity: 0;
    transform: translateY(10px);
}

.list-move {
    transition: transform 0.3s ease;
}

.catalog {
    @apply flex flex-col w-full lg:pl-8;

    &__navigation {
        @apply w-full;

        div:first-child {
            @apply w-full flex justify-between items-center;

            h4 {
                @apply text-md font-normal text-muted md:mr-8;

                span {
                    @apply text-dark;
                }
            }

            form {
                @apply block w-36 h-10 relative bg-gray-100 px-4 py-2 rounded-xl;

                /* Add a custom SVG arrow as background */
                &::after {
                    content: "";
                    background-image: url("@/assets/icons/arrow-select.svg");
                    @apply absolute top-1/2 -translate-y-1/2 right-4 w-8 h-8 bg-center bg-no-repeat;
                }

                select {
                    @apply absolute z-20 top-0 left-0 w-full h-full appearance-none bg-transparent text-dark px-4
                        outline-none text-sm;

                    option {
                        @apply text-sm text-dark hover:text-white hover:bg-dark duration-300 ease-out;
                    }
                }
            }

        }

        &__applied-filters {
            @apply w-full flex justify-start items-center;

            span {
                @apply  min-h-12 flex items-center;

                h4 {
                    @apply text-md text-muted font-normal mr-8 whitespace-nowrap;
                }
            }

            ul {
                @apply flex items-center flex-wrap;

                li {
                    @apply mr-4 px-4 text-sm h-10 rounded-full border-2 border-dark text-dark flex
                        items-center justify-between cursor-pointer duration-100 ease-in-out hover:bg-dark
                        hover:text-white my-1;

                    span {
                        @apply relative block w-3 h-3 ml-4 duration-100 ease-in-out

                            before:absolute before:top-1/2 before:-translate-y-1/2 before:w-full before:h-0.5
                            before:bg-dark before:rotate-45

                            after:absolute after:top-1/2 after:-translate-y-1/2 after:w-full after:h-0.5
                            after:bg-dark after:-rotate-45;
                    }

                    &:hover span {
                        @apply before:bg-white after:bg-white;
                    }

                    &:last-child {
                        @apply mr-0;
                    }
                }
            }
        }

        & > * {
            @apply mb-4;

            &:last-child {
                @apply mb-0;
            }
        }
    }

    &__card-list {
        @apply w-full grid grid-cols-12 gap-x-4 gap-y-10;

        &__item {
            @apply col-span-12 sm:col-span-6 md:col-span-4 lg:col-span-6 xl:col-span-4 2xl:col-span-3;

            .card {
                @apply w-full
            }
        }
    }

    &__no-available {
        @apply w-full mt-16 flex justify-center items-center;

        h1 {
            @apply text-2xl text-muted font-medium font-outfit;
        }
    }
}
</style>