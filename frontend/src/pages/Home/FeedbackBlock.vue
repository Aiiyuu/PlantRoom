<template>
    <div class="feedback" id="feedbacks">
        <h1 class="feedback__title">
            Our happy customers
        </h1>
    </div>
</template>

<script lang="ts" setup>
import Feedback from '@/types/FeedbackInterface'

</script>


<style lang="scss" scoped>
.feedback {
    @apply relative w-full py-8 px-8 md:px-16 bg-cream;

    &__title {
        @apply text-4xl font-medium;
    }
}
</style>