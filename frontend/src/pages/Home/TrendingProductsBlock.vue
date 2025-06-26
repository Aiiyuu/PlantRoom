<template>
    <div class="trending-products" id="trending-products">
        <h1 class="trending-products__title">Trending Products</h1>

        <!-- Sorting bar: only show if not loading and inventory has items -->
        <div v-if="!inventoryStore.isLoading && inventoryStore.inventory?.length" class="trending-products__sorting-bar">
            <span
                class="trending-products__sorting-bar__item"
                v-for="method in sortingMethods"
                :key="method"
            >
                <button
                    :class="{ selected: selectedSorting === method }"
                    @click="selectSorting(method)"
                >
                  {{ method }}
                </button>
            </span>
        </div>

        <!-- Loading skeleton: show while loading -->
        <div v-if="inventoryStore.isLoading" class="trending-products__carousel">
            <div class="trending-products__carousel__inner">
                <PlantCard
                    v-for="n in 5"
                    :key="n"
                    class="trending-products__carousel__inner__item"
                    :isLoading="true"
                />
            </div>
        </div>

        <!-- Actual carousel: show if not loading and inventory has items -->
        <div
            v-else-if="inventoryStore.inventory?.length"
            class="trending-products__carousel"
            ref="carouselWindow"
        >
            <div class="trending-products__carousel__inner" ref="carouselInner">
                <PlantCard
                    class="trending-products__carousel__inner__item"
                    v-for="item in inventoryStore.inventory"
                    :key="item.id"
                    :plant="item"
                    :isLoading="false"
                />
            </div>

            <div class="trending-products__carousel__navigation">
                <button
                    class="trending-products__carousel__navigation__item prev"
                    @click="scrollCarousel('prev')"
                >
                    <img src="@/assets/icons/arrow.svg" alt="Previous" />
                    <span>Prev</span>
                </button>

                <button
                    class="trending-products__carousel__navigation__item next"
                    @click="scrollCarousel('next')"
                >
                    <span>Next</span>
                    <img class="rotate-180" src="@/assets/icons/arrow.svg" alt="Next" />
                </button>
            </div>
        </div>

        <!-- No data message -->
        <div v-else>
            <h1>No plants available</h1>
        </div>
    </div>
</template>

<script lang="ts" setup>
import PlantCard from "@/components/ui/PlantCard.vue"
import { ref, onMounted, computed } from 'vue'
import { useInventoryStore } from "@/stores/inventory"

const inventoryStore = useInventoryStore()


/* ------------------ Sorting implementation --------------------- */

// Define your sorting methods
const sortingMethods = ['featured', 'cheapest', 'name']

// Reactive ref for selected sorting method
const selectedSorting = ref('featured')

// Function to change the selected sorting method
function selectSorting(method: string) {
    selectedSorting.value = method

    // Update the inventory sorting method based on the selected sorting option
    inventoryStore.updateSortMethod(method)
}

onMounted(() => {
    // Fetch date from the inventory API endpoint
    inventoryStore.fetchInventory()
})


/* ------------------ Carousel implementation --------------------- */

// Carousel references and state
const carouselInner = ref<HTMLElement | null>(null);
const carouselWindow = ref<HTMLElement | null>(null);

// Start index for the carousel (0 means the first item)
let carouselCurrentIndex = 0

// Scroll the carousel container
function scrollCarousel(direction: "prev" | "next") {
    if (!carouselInner.value && !carouselWindow.value) return;

    // Retrieves the first child of the carouselInner
    const firstChild = carouselInner.value!.firstElementChild;
    if (!firstChild) return;

    // Get the number of child elements inside carouselInner
    const numberOfChildren = carouselInner.value!.children.length;

    // Get the computed styles of the first child
    const styles = window.getComputedStyle(firstChild);

    // Get the width and margin-right of the first child
    const width = parseFloat(styles.width); // Converts width to a float
    const marginRight = parseFloat(styles.marginRight); // Converts margin-right to a float

    // Calculate the number of cards visible on the screen based on window width
    const visibleCards = Math.floor(carouselWindow.value!.offsetWidth / (width + marginRight));

    // Calculate the number of cards that will be scrolled per "next" or "prev" action
    const cardsToScroll = 1;

    // Update carousel index based on direction
    if (direction === "next") {
        // Move to the next group of cards, but not beyond the last group
        carouselCurrentIndex = Math.min(carouselCurrentIndex + cardsToScroll, numberOfChildren - visibleCards);
    } else if (direction === "prev") {
        // Move to the previous group of cards, but not before the first group
        carouselCurrentIndex = Math.max(carouselCurrentIndex - cardsToScroll, 0);
    }

    // Update carousel position by adjusting translation
    carouselInner.value!.style.transform = `translateX(-${(width + marginRight) * carouselCurrentIndex}px)`;
}

</script>

<style lang="scss" scoped>
.trending-products {
    @apply w-full min-h-screen bg-white py-8 px-8 md:px-16 flex flex-col justify-center items-center;

    &__title {
        @apply font-medium text-4xl
    }

    &__sorting-bar {
        @apply flex justify-between items-center;

        &__item {
            @apply flex items-center mr-8;

            & > button {
                @apply text-sm font-normal cursor-pointer text-muted duration-300 ease-out;

                &.selected {
                    @apply text-dark;
                }
            }

            &:last-child {
                @apply mr-0;

                &::after {
                    display: none;
                }
            }

            &::after {
                content: "";
                @apply block w-0.5 h-4 bg-dark ml-8;
            }
        }
    }

    &__carousel {
        @apply relative w-full overflow-x-hidden;

        &__inner {
            @apply h-full w-full flex items-start duration-300 ease-in-out;

            .card {
                @apply mr-10;

                &:last-child {
                    @apply mr-0;
                }
            }
        }

        &__navigation {
            @apply flex items-center justify-center mt-16;

            &__item {
                @apply relative flex items-center justify-center border-dark border-b-2 pb-2 opacity-100 duration-300
                    ease-out hover:opacity-50;

                span {
                    @apply text-sm font-normal uppercase ml-2;
                }

                &:last-child {
                    @apply ml-8;

                    span {
                        @apply ml-0 mr-2;
                    }
                }
            }
        }
    }

    & > * {
        @apply mb-10;

        &:last-child {
            @apply mb-0;
        }
    }
}
</style>