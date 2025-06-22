<template>
    <div class="header" id="home">
        <div class="header__decoration">
            <img src="@/assets/images/header-decoration.svg" alt="">
        </div>
        <div class="header__content">
            <h1 class="header__content__title">Plant<br><span>Room</span></h1>
            <p class="header__content__text">

                Welcome to Plant Room – your personal gateway to a greener, calmer space, where thoughtfully selected
                indoor plants don’t just decorate your home, but transform it into a living sanctuary of peace, beauty,
                and connection to nature.
            </p>

            <BaseButton
                class="header__content__button"
                text="Shop now"
                color="#FFBF78"
                textColor="#FFFDF6"
                rotate="0deg"
            />

        </div>

        <div class="header__gear-decoration">
            <span></span>
        </div>
    </div>
</template>

<script setup>
import BaseButton from "@/components/ui/BaseButton.vue"
</script>


<style lang="scss" scoped>
.header {
    @apply min-h-screen min-w-full bg-cream relative text-dark grid grid-cols-12 items-center overflow-hidden;

    &__decoration {
        @apply col-span-12 md:col-span-6 lg:col-span-7 order-2 md:order-1;

        img {
            @apply w-full;
        }
    }

    &__content {
        @apply flex flex-col items-start md:items-end w-auto mt-16 md:mt-0 mx-8 sm:mx-16 md:ml-0 col-span-12
               md:col-span-6 lg:col-span-5 order-1 md:order-2 ;

        &__title {
            @apply flex flex-col items-start md:items-end font-roboto text-[100px] leading-[80px] font-semibold;

            span {
                @apply text-[120px] font-bold;
            }
        }

        &__text {
            @apply text-start md:text-end text-sm my-8 font-normal;
        }

        &__button {
            @apply w-32 h-10 ;
        }

    }

    &__gear-decoration {
        @apply absolute bottom-0 right-0 w-64 h-64 translate-x-1/4 scale-150  translate-y-1/2
            hidden md:block;

        span {
            @apply relative block w-64 h-64 border-[25px] border-solid border-peach-orange rounded-full;

            &::before {
                content: "";
                @apply absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-44 h-44 border-[20px] border-solid
                    border-pale-yellow rounded-full;
            }
        }
    }
}
</style>