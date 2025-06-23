<template>
    <div class="card" :class="{ loading: isLoading }">
        <div v-if="!isLoading" class="card__image">
            <img :src="fullImageUrl" :alt="plant.name">
        </div>
        <div v-else class="card__image loading bg-dark-cream"></div>

        <div v-if="!isLoading" class="card__rating">
            <!-- Loop through 5 stars -->
            <span
                v-for="i in 5"
                :key="i"
                :class="[
                    'star',
                    i <= plant.rating ? 'star--active' : 'star--inactive'
                ]"
            ></span>
        </div>
        <div v-else class="card__rating w-full h-4 loading bg-dark-cream"></div>

        <h2 v-if="!isLoading" class="card__name">{{ plant.name }}</h2>
        <div v-else class="card__name w-full flex">
            <div class="w-[45%] h-4 loading bg-dark-cream mr-4"></div>
            <div class="w-[25%] h-4 loading bg-dark-cream mr-auto"></div>
        </div>

        <div v-if="!isLoading" class="card__price">
            <span v-if="!plant.discount_percentage" >${{ plant.price }}</span>
            <div v-else>
                <span>${{ plant.discounted_price }}</span>
                <span class="line-through ml-2">${{ plant.price }}</span>
            </div>
        </div>
        <div v-else class="card__price w-[25%] h-4 loading bg-dark-cream mr-auto"></div>

    </div>
</template>

<script lang="ts" setup>
import { computed, inject } from 'vue'
import Plant from '@/types/PlantInterface'

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

        .star {
            @apply w-5 h-5 bg-no-repeat bg-center inline-block mr-2;
            background-image: url('@/assets/icons/star.svg');

            &:last-child {
                @apply mr-0;
            }
        }

        .star--inactive {
            background-image: url('@/assets/icons/star-disabled.svg');
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