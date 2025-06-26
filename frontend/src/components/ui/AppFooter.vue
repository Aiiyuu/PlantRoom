<template>
    <footer class="footer">
        <div class="footer__sub-block">
            <div>
                <router-link class="flex justify-center" to="/">
                    <img src="@/assets/icons/logo-icon.svg" alt="">
                    <h1 class="navbar__logo">PlantRoom</h1>
                </router-link>

                <p class="footer__sub-block__text">
                    Bringing nature closer to your home with beautiful, healthy plants. At PlantRoom, we’re passionate
                    about helping you grow a greener life. Thank you for choosing us as your plant partner.
                </p>
            </div>


        </div>

        <div class="footer__sub-block">
            <div class="footer__sub-block__social-networks">
                <a href="#"><img src="@/assets/icons/facebook.svg" alt="facebook"></a>
                <a href="#"><img src="@/assets/icons/twitter.svg" alt="twitter"></a>
                <a href="#"><img src="@/assets/icons/wi-fi.svg" alt="wi-fi"></a>
                <a href="#"><img src="@/assets/icons/google-plus.svg" alt="google-plus"></a>
                <a href="#"><img src="@/assets/icons/instagram.svg" alt="instagram"></a>
            </div>
        </div>

        <div class="footer__sub-block">
            <div class="footer__sub-block__navigation flex">
                <div class="footer__sub-block__navigation__block">
                    <h1 class="footer__sub-block__navigation__block_title">Navigation</h1>
                    <ul class="footer__sub-block__navigation__block__list">
                        <li class="footer__sub-block__navigation__block__list__item">
                            <a href="#home">Home</a>
                        </li>
                        <li class="footer__sub-block__navigation__block__list__item">
                            <a href="#about-us">About us</a>
                        </li>
                        <li class="footer__sub-block__navigation__block__list__item">
                            <a href="#trending-products">Trending Products</a>
                        </li>
                        <li class="footer__sub-block__navigation__block__list__item">
                            <a href="#our-advantages">Our Advantages</a>
                        </li>
                        <li class="footer__sub-block__navigation__block__list__item">
                            <a href="#feedbacks">Feedbacks</a>
                        </li>
                        <li class="footer__sub-block__navigation__block__list__item">
                            <a href="#location">Locations</a>
                        </li>
                    </ul>
                </div>

                <div class="footer__sub-block__navigation__block">
                    <h1 class="footer__sub-block__navigation__block_title">My Account</h1>
                    <ul class="footer__sub-block__navigation__block__list">
                        <li class="footer__sub-block__navigation__block__list__item">
                            <router-link :to="{ name: 'auth' }">My Account</router-link>
                        </li>
                        <li class="footer__sub-block__navigation__block__list__item">
                            <router-link to="#">Cart</router-link>
                        </li>
                        <li class="footer__sub-block__navigation__block__list__item">
                            <router-link to="#">Gallery</router-link>
                        </li>
                    </ul>
                </div>

                <div class="footer__sub-block__navigation__block">
                    <h1 class="footer__sub-block__navigation__block_title">Store Information</h1>
                    <ul class="footer__sub-block__navigation__block__list">
                        <li class="footer__sub-block__navigation__block__list__item">
                            <div class="flex items-center">
                                <img class="contact-image" src="@/assets/icons/location.svg" alt="">
                                <router-link to="#">Demo Store<br>United States</router-link>
                            </div>
                        </li>
                        <li class="footer__sub-block__navigation__block__list__item">
                            <div class="flex items-center">
                                <img class="contact-image" src="@/assets/icons/phone.svg" alt="">
                                <router-link to="#">(555) 018-2746</router-link>
                            </div>
                        </li>
                        <li class="footer__sub-block__navigation__block__list__item">
                            <div class="flex items-center">
                                <img class="contact-image" src="@/assets/icons/email.svg" alt="">
                                <router-link to="#">plant.room@gmail.com</router-link>
                            </div>
                        </li>
                    </ul>
                </div>

                <div class="footer__sub-block__navigation__block">
                    <h1 class="footer__sub-block__navigation__block_title">My Account</h1>
                    <ul class="footer__sub-block__navigation__block__list">
                        <li class="footer__sub-block__navigation__block__list__item">
                            <a href="#">
                                <img src="@/assets/icons/payment-icon.svg" class="cursor-pointer" alt="PayPal">
                            </a>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    </footer>
</template>

<style lang="scss" scoped>
.footer {
    @apply w-full h-[360px] grid grid-cols-12;

    &__sub-block {
        @apply h-full w-full flex justify-center items-center p-8;

        &__text {
            @apply text-center mt-4 text-sm;
        }

        &__social-networks {
            @apply flex justify-center items-center md:flex-col;

            a {
                @apply mr-8 md:mr-0 md:mb-8 ;

                &:last-child {
                    @apply mb-0 mr-0;
                }

                img {
                    @apply duration-300 ease-out;
                }

                &:hover  img {
                    @apply scale-125;
                }
            }
        }

        &__navigation {
            @apply flex justify-between flex-wrap;

            &__block {
                @apply p-4;

                &__title {
                    @apply text-base font-medium w-full;
                }

                &__list {
                    @apply mt-4;

                    &__item {
                        @apply text-base font-extralight mb-2 hover:underline;
                        &:last-child {
                            @apply mb-0;
                        }

                        .contact-image {
                            @apply mr-4;
                        }
                    }
                }
            }
        }

        &:nth-child(1) {
            @apply col-span-12 md:col-span-4 bg-snow-vei text-dark;
        }

        &:nth-child(2) {
            @apply col-span-12 md:col-span-2 lg:col-span-1 bg-olive-grove text-dark;
        }

        &:nth-child(3) {
            @apply col-span-12 md:col-span-6 lg:col-span-7 bg-dark;

            * {
                @apply text-white;
            }
        }
    }
}
</style>
<script setup lang="ts">
</script>