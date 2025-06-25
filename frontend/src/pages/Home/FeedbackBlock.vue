<template>
    <div class="feedback" id="feedbacks">
        <h1 class="feedback__title">
            Our happy customers
        </h1>

        <!-- Show loading skeleton when loading -->
        <div v-if="feedbackStore.isLoading" class="feedback__list" ref="container">
            <div class="feedback__list__track">
                <FeedbackCard
                    v-for="n in 5"
                    :key="n"
                    :is-loading="true"
                    class="card"
                />
            </div>
        </div>

        <!-- Show feedbacks when loaded -->
        <div v-else-if="feedbackStore.feedbacks?.length" class="feedback__list" ref="container">
            <div
                class="feedback__list__track"
                :style="{ transform: `translateX(-${offset}px)` }"
            >
                <!-- Duplicate feedbacks for seamless loop -->
                <FeedbackCard
                    v-for="(feedback, index) in duplicatedFeedbacks"
                    :feedback="feedback"
                    :is-loading="false"
                    :key="index"
                    class="card"
                />
            </div>
        </div>

        <!-- No feedbacks message -->
        <div v-else>
            <h1>No feedbacks available</h1>
        </div>
    </div>
</template>


<script lang="ts" setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import { useFeedbackStore } from "@/store/feedbackStore"
import FeedbackCard from "@/components/ui/FeedbackCard.vue"
import Feedback from '@/types/FeedbackInterface'

const feedbackStore = useFeedbackStore();
const duplicatedFeedbacks = ref<Feedback[]>([]) // It is used for auto scroll carousel

onMounted(() => {
    // Fetch date from the feedback API endpoint
    feedbackStore.fetchFeedbacks().then(() => {
        duplicatedFeedbacks.value = [...feedbackStore.feedbacks, ...feedbackStore.feedbacks];
    })

})
</script>


<style lang="scss" scoped>
.feedback {
    @apply relative w-full py-8 px-8 md:px-16 bg-white flex flex-col items-center;

    &__title {
        @apply text-4xl font-medium;
    }

    &__list {
        @apply flex  items-start w-full overflow-hidden;

        &__track {
            @apply flex;
            animation: scroll 40s linear infinite;

            .card {
                @apply mr-10;

                &:last-child {
                    @apply mr-0;
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

@keyframes scroll {
    from {
        transform: translateX(0);
    }
    to {
        transform: translateX(-50%);
    }
}
</style>