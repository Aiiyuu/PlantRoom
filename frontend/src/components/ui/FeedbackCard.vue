<template>
    <div class="card" :class="{ loading: isLoading }">
        <div class="card__header">
            <h1 v-if="!isLoading" class="card__header__title">{{ feedback.user.name }}</h1>
            <div v-else class="card__header__title w-full flex">
                <div class="w-[25%] h-4 loading bg-white mr-4"></div>
                <div class="w-[15%] h-4 loading bg-white"></div>
            </div>

            <span v-if="!isLoading" class="card__header__date">{{ feedback.added_at }}</span>
            <div v-else class="card__header__date w-[30%] h-4 loading bg-white"></div>

        </div>

        <div v-if="!isLoading" class="card__content">
            <p>{{ feedback.content }}</p>
        </div>
        <div v-else>
            <div class="flex w-full mb-2">
                <div class="w-[25%] h-4 loading bg-white mr-4"></div>
                <div class="w-[10%] h-4 loading bg-white mr-4"></div>
                <div class="w-[15%] h-4 loading bg-white mr-4"></div>
                <div class="w-[20%] h-4 loading bg-white"></div>
            </div>
            <div class="flex w-full mb-2">
                <div class="w-[20%] h-4 loading bg-white mr-4"></div>
                <div class="w-[35%] h-4 loading bg-white mr-4"></div>
                <div class="w-[25%] h-4 loading bg-white"></div>
            </div>
            <div class="flex w-full">
                <div class="w-[35%] h-4 loading bg-white mr-4"></div>
                <div class="w-[15%] h-4 loading bg-white"></div>
            </div>
        </div>

        <div v-if="!isLoading" class="card__rating">
            <!-- Loop through 5 stars -->
            <span
                v-for="i in 5"
                :key="i"
                :class="[
                    'star',
                    i <= feedback.rating ? 'star--active' : 'star--inactive'
                ]"
            ></span>
        </div>
        <div v-else class="card__rating w-[40%] min-h-4 loading bg-white"></div>
    </div>
</template>

<script lang="ts" setup>
import Feedback from '@/types/FeedbackInterface'

const props = defineProps<{
    feedback: Feedback,
    isLoading: boolean,
}>()
</script>

<style lang="scss" scoped>
    .card {
        @apply relative w-[380px] h-[200px] bg-snow-vei rounded-xl p-4 flex flex-col justify-between;

        .card__header {
            @apply flex items-center justify-between;

            &__title {
                @apply text-sm font-semibold;
            }

            &__date {
                @apply text-sm font-normal;
            }
        }

        &__content {
            @apply h-full overflow-y-auto;

            p {
                @apply text-sm font-normal;
            }
        }

        &__rating {
            @apply flex  items-center;

            .star {
                @apply w-5 h-5 bg-no-repeat bg-center inline-block mr-2;
                background-image: url('@/assets/icons/star.svg');

                &:last-child {
                    @apply mr-0;
                }
            }

            .star--inactive {
                background-image: url('@/assets/icons/star-disabled.svg');
                filter: brightness(0) saturate(100%) invert(100%) sepia(7%) saturate(4887%) hue-rotate(247deg) brightness(105%) contrast(103%);
            }
        }

        & > * {
            @apply mb-4;

            &:last-child {
                @apply mb-0;
            }
        }
    }
</style>