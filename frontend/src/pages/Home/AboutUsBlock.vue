<template>
    <div class="about-us">
        <div class="about-us__sub-block">
            <img src="@/assets/images/about-us-image-set.png" alt="">
        </div>

        <div class="about-us__sub-block">
            <h1 class="about-us__sub-block__title">About us</h1>
            <p class="about-us__sub-block__text">
                At PlantRoom, we make it easy to bring nature indoors. From beautiful, healthy houseplants to modern
                planters and care essentials, we’re here to help your space thrive. Whether you’re a beginner or a plant
                pro, we’ve got everything you need to grow with confidence.
            </p>

            <div class="about-us__sub-block__advantages flex">
                <div class="about-us__sub-block__advantages__item">
                    <span><span>13</span></span>
                    <h4>Store locators</h4>
                </div>
                <div class="about-us__sub-block__advantages__item">
                    <span><span>328</span></span>
                    <h4>Plants</h4>
                </div>
                <div class="about-us__sub-block__advantages__item">
                    <span><span>96</span></span>
                    <h4>Customers</h4>
                </div>
            </div>

            <BaseButton
                class="about-us__sub-block__button"
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
.about-us {
    @apply min-w-full min-h-screen flex flex-col md:flex-row items-center justify-between
        p-8 md:px-16 bg-dark-cream;

    &__sub-block {
        &:first-child {
            @apply md:mr-16 mb-16 md:mb-0;
        }

        &__title {
            @apply font-medium text-4xl;
        }

        &__text {
            @apply font-normal text-sm max-w-[500px];
        }

        &__advantages {
            &__item {
                @apply flex flex-col items-center justify-between mr-12;

                &:last-child {
                    @apply mr-0;
                }

                & > span {
                  @apply relative block w-16 h-16 border-4 border-peach-orange rounded-full ease-out duration-500;

                    & > span {
                        @apply absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 text-peach-orange
                            ease-out duration-500;
                    }
                }

                h4 {
                    @apply text-sm font-normal whitespace-nowrap mt-2;
                }

                &:hover {
                    & > span {
                        @apply bg-peach-orange;
                        & > span {
                            @apply text-cream;
                        }
                    }
                }
            }
        }

        &__button {
            @apply md:w-56 h-10;
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