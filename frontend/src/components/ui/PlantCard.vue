<template>
    <div class="card">
        <div class="card__image">
            <img :src="fullImageUrl" :alt="plant.name">
        </div>

        <div class="card__rating">
            <!-- Loop through 5 stars -->
            <img
                v-for="i in 5"
                :key="i"
                :src="i <= plant.rating ? require('@/assets/icons/star.svg') : require('@/assets/icons/star-disabled.svg')"
            />
        </div>

        <h2 class="card__name">{{ plant.name }}</h2>
        <div class="card__price">
            <span v-if="!plant.discount_percentage" >${{ plant.price }}</span>
            <div v-else>
                <span>${{ plant.discounted_price }}</span>
                <span class="line-through ml-2">${{ plant.price }}</span>
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { computed, inject } from 'vue'
import Plant from '@/store/inventoryStore'

// Define props
const props = defineProps<{
    plant: Plant
    isLoading: boolean
}>()

// Inject the global image base URL
const imageBaseUrl = inject('$imageBaseUrl', '')

// Compute the full image URL by combining the base URL with the relative path
const fullImageUrl = computed(() => {
    return imageBaseUrl ? `${imageBaseUrl}${props.plant.image}` : ''
})
</script>

<style lang="scss" scoped>
.card {
    @apply flex flex-col items-center justify-center;

    &__image {
        @apply relative min-w-[230px] h-[320px] rounded-xl bg-dark-cream flex justify-center items-center;

        img {
            @apply static;
        }
    }

    &__rating {
        @apply flex justify-center items-center;

        img {
            @apply mr-3;

            &:last-child {
                @apply mr-0;
            }
        }
    }

    &__name {
        @apply text-sm font-normal;
    }

    &__price {
        @apply text-sm font-normal;
    }

    & > * {
        @apply mb-4;

        &:last-child {
            @apply mb-0;
        }
    }
}
</style>