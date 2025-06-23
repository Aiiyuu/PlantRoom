<template>
    <div class="card">
        <div class="card__header">
            <h1 class="card__header__title">{{ feedback.user.name }}</h1>
            <span class="card__header__date">{{ feedback.added_at }}</span>

        </div>

        <div class="card__content">
            <p>{{ feedback.content }}</p>
        </div>

        <div class="card__rating">
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
        @apply relative w-[380px] h-[200px] bg-dark-cream rounded-xl p-4 flex flex-col justify-between;

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