<template>
    <div class="advantages-block" id="our-advantages">
        <div class="advantages-block__sub-block">
            <img src="@/assets/images/young-man-portrait.png" alt="image">
        </div>

        <div class="advantages-block__sub-block">
            <h1 class="advantages-block__sub-block__title">Find natural note</h1>
            <p class="advantages-block__sub-block__text">
                AtPlantRoom, we’re all about making plant care simple, joyful, and stress-free. Enjoy free shipping on
                every order and shop with peace of mind thanks to our 14-day money-back guarantee. Our secure online
                payments and flexible checkout options make your experience smooth from start to finish. Each plant
                is hand-picked with care and thoughtfully packed to arrive fresh, healthy, and ready to thrive. And if
                you ever need help, our friendly support team is always here to guide you—because at PlantRoom, growing
                green should feel good.
            </p>

            <ul class="advantages-block__sub-block__advantages-list">
                <li class="advantages-block__sub-block__advantages-list__item">
                    <img src="@/assets/icons/free-shipping.svg" alt="free shipping">
                    <h4>free shipping</h4>
                </li>

                <li class="advantages-block__sub-block__advantages-list__item">
                    <img src="@/assets/icons/money-back.svg" alt="free shipping">
                    <h4>Money back</h4>
                </li>

                <li class="advantages-block__sub-block__advantages-list__item">
                    <img src="@/assets/icons/online-payment.svg" alt="free shipping">
                    <h4>Online payment</h4>
                </li>
            </ul>

            <BaseButton
                class="advantages-block__sub-block__button"
                text="Shop now"
                color="#FFBF78"
                textColor="#FFFDF6"
                rotate="0deg"
            />
        </div>
    </div>
</template>

<script setup>
import BaseButton from "@/components/ui/BaseButton.vue"
</script>

<style lang="scss" scoped>
.advantages-block {
    @apply relative w-full min-h-screen py-8 px-8 md:px-16 bg-dark-cream flex items-center
        justify-between flex-col lg:flex-row;

    &__sub-block {
        @apply relative;

        &:first-child {
            @apply lg:mr-16 mb-10 lg:mb-0 ;

            img {
                @apply max-w-[360px]  shadow-lg;
            }
        }

        &__title {
            @apply text-4xl font-medium;
        }

        &__text {
            @apply text-sm font-normal max-w-[700px];
        }

        &__advantages-list {
            @apply flex items-start justify-center sm:justify-start;

            &__item {
                @apply flex flex-col items-center justify-center mr-10;

                &:last-child {
                    @apply mr-0;
                }

                img {
                    @apply w-24 h-24 mb-2;
                }

                h4 {
                    @apply text-sm font-light;
                }
            }
        }

        &__button {
            @apply lg:w-48 h-10;
        }

        & > * {
            @apply mb-10;

            &:last-child {
                @apply mb-0;
            }
        }
    }
}
</style>
<script setup lang="ts">
</script>