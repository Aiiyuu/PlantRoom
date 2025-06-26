<template>
    <div class="price-filter">
        <div class="price-filter__form">
            <div class="price-filter__form__field range">
                <label>Price</label>

                <div>
                    <!-- Highlighted selected range -->
                    <div
                        class="highlighted-range"
                        :style="{
                            right: `${100 - (max / 1000) * 100}%`,
                            left: `${(min / 1000) * 100}%`,
                        }"
                    />

                    <input
                        type="range"
                        min="0"
                        max="1000"
                        :value="min"
                        @input="onMinRangeChange"
                        id="minRange"
                    />
                    <input
                        type="range"
                        min="0"
                        max="1000"
                        :value="max"
                        @input="onMaxRangeChange"
                        id="maxRange"
                    />
                </div>
            </div>

            <div class="flex justify-between w-full">
                <div class="price-filter__form__field">
                    <label for="min-price">from</label>
                    <input
                        id="min-price"
                        type="number"
                        :value="min"
                        @input="onMinInputChange"
                        @blur="onMinInputBlur"
                        min="0"
                        max="1000"
                    />
                </div>

                <div class="price-filter__form__field">
                    <label for="max-price">to</label>
                    <input
                        id="max-price"
                        type="number"
                        :value="max"
                        @input="onMaxInputChange"
                        @blur="onMaxInputBlur"
                        min="0"
                        max="1000"
                    />
                </div>
            </div>
        </div>
    </div>
</template>


<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import { useInventoryStore } from '@/stores/inventory'

const store = useInventoryStore()

// Reactive variables for min and max price values
// Create computed properties to sync with store's filter.price.min/max
const min = computed({
    get: () => store.filter.price.min,
    set: (val: number) => {
        // Keep min within bounds and less or equal to max
        if (val >= 0 && val <= store.filter.price.max) {
            store.filter.price.min = val
        }
    }
})

const max = computed({
    get: () => store.filter.price.max,
    set: (val: number) => {
        // Keep max within bounds and greater or equal to min
        if (val <= 1000 && val >= store.filter.price.min) {
            store.filter.price.max = val
        }
    }
})

/**
 * Handler for changing the minimum range slider thumb
 * Ensures min does not exceed max
 */
function onMinRangeChange(event: Event) {
    const input = event.target as HTMLInputElement;
    const value = Number(input.value);

    if (value <= max.value) {
        // Update min if it's less than or equal to max
        min.value = value;
    } else {
        // Otherwise, reset thumb position to current min value
        input.value = String(min.value);
    }
}

/**
 * Handler for changing the maximum range slider thumb
 * Ensures max does not go below min
 */
function onMaxRangeChange(event: Event) {
    const input = event.target as HTMLInputElement;
    const value = Number(input.value);

    if (value >= min.value) {
        // Update max if it's greater than or equal to min
        max.value = value;
    } else {
        // Otherwise, reset thumb position to current max value
        input.value = String(max.value);
    }
}

/**
 * Handler for changing the minimum numeric input
 * Ensures min is between 0 and current max
 */
function onMinInputChange(event: Event) {
    const input = event.target as HTMLInputElement;
    const value = Number(input.value);

    if (value >= 0 && value <= max.value) {
        min.value = value;
    }
}

// On blur (when user leaves input), enforce min <= max by resetting min to max if needed
function onMinInputBlur(event: Event) {
    const input = event.target as HTMLInputElement;
    const value = Number(input.value);

    if (value > max.value) {
        min.value = max.value;           // reset min to max
        input.value = String(max.value); // update input display
    }
}

/**
 * Handler for changing the maximum numeric input
 * Ensures max is between current min and 1000
 */
function onMaxInputChange(event: Event) {
    const input = event.target as HTMLInputElement;
    const value = Number(input.value);

    if (value <= 1000 && value >= min.value) {
        max.value = value;
    } else if (value > 100) {
        max.value = value;
        input.value = String(1000);
    }
}

// On blur (when user leaves input), enforce max >= min by resetting max to min if needed
function onMaxInputBlur(event: Event) {
    const input = event.target as HTMLInputElement;
    const value = Number(input.value);

    if (value < min.value) {
        max.value = min.value;           // reset max to min
        input.value = String(min.value); // update input display
    }
}

/**
 * Watchers to enforce constraints reactively in case
 * values change programmatically or from unexpected input
 */
watch(min, (val) => {
    if (val > max.value) min.value = max.value
    if (val < 0) min.value = 0
})

watch(max, (val) => {
    if (val < min.value) max.value = min.value
    if (val > 1000) max.value = 1000
})

/**
 * Resets the price filter values to their default states.
 * This method is exposed to parent components so they can
 * programmatically reset the price filter when needed (e.g., on form reset).
 */
function resetPrice() {
    min.value = 10   // Reset min to default
    max.value = 600  // Reset max to default
}

// Expose the resetPrice method to the parent component
// so it can be called via template ref (e.g., priceFilter.value.resetPrice())
defineExpose({ resetPrice })
</script>

<style lang="scss" scoped>
.price-filter {
    &__form {
        &__field {
            @apply flex flex-col;

            label {
                @apply text-md text-dark font-normal mb-4;
            }

            input {
                @apply bg-transparent outline-none w-32 h-10 border-2 px-4 ml-4 border-gray-200
                rounded-xl focus:border-dark;

                /* Hide number input arrows for Chrome, Safari, Edge, Opera */
                &::-webkit-outer-spin-button,
                &::-webkit-inner-spin-button {
                    -webkit-appearance: none;
                    margin: 0;
                }

                /* Hide number input arrows for Firefox */
                &[type=number] {
                    -moz-appearance: textfield;
                }
            }
        }

        &__field.range > div {
            @apply relative h-8;

            .highlighted-range {
                @apply absolute top-1/2 h-1.5 bg-dark rounded-sm z-10;
            }

            input[type='range'] {
                @apply cursor-pointer absolute top-0 left-0 w-full p-0 m-0 bg-transparent border-none;
                -webkit-appearance: none;

                &::-webkit-slider-thumb {
                    @apply appearance-none w-5 h-5 rounded-full cursor-pointer border-2 relative;
                    -webkit-appearance: none;
                }

                &::-moz-range-thumb {
                    @apply w-5 h-5 rounded-full bg-gray-200 cursor-pointer;
                }

                &::-webkit-slider-runnable-track, {
                    @apply bg-gray-200 h-1.5 rounded-sm;
                }

                &::-moz-range-track {
                    @apply bg-gray-200 h-1.5 rounded-sm;
                }
            }

            // Style for min range thumb
            #minRange::-webkit-slider-thumb {
                @apply z-30 -translate-y-1/2 top-1/2 w-5 h-5 rounded-full cursor-pointer border-2;
                background: radial-gradient(circle, white 30%, black 31%);
                -webkit-appearance: none;
            }

            #minRange::-moz-range-thumb {
                @apply z-30 -translate-y-1/2 top-1/2 w-5 h-5 rounded-full cursor-pointer border-2;
                background: radial-gradient(circle, white 30%, black 31%);
            }

            // Style for max range thumb
            #maxRange::-webkit-slider-thumb {
                @apply z-30 -translate-y-1/2 top-1/2 w-5 h-5 rounded-full cursor-pointer border-2;
                background: radial-gradient(circle, white 30%, black 31%);
                -webkit-appearance: none;
            }

            #maxRange::-moz-range-thumb {
                @apply z-30 -translate-y-1/2 top-1/2 w-5 h-5 rounded-full cursor-pointer border-2;
                background: radial-gradient(circle, white 30%, black 31%);
            }
        }

        & > * {
            @apply mb-4;

            &:last-child {
                @apply mb-0;
            }
        }
    }
}
</style>