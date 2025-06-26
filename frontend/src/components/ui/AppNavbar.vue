<template>
    <nav class="navbar flex justify-between items-center">
        <router-link class="flex items-center" :to="{ name: 'home' }">
            <img src="@/assets/icons/logo-icon.svg" alt="">
            <h1 class="navbar__logo">PlantRoom</h1>
        </router-link>

        <ul class="navbar__menu-list hidden sm:flex">
            <li class="navbar__menu-list__item">
                <router-link :to="{ name: 'home' }">Home</router-link>
            </li>
            <li class="navbar__menu-list__item">
                <router-link :to="{ name: 'catalog' }">Catalog</router-link>
            </li>
            <li class="navbar__menu-list__item">
                <router-link>Gallery</router-link>
            </li>
            <li class="navbar__menu-list__item">
                <router-link>Cart</router-link>
            </li>
        </ul>

        <HamburgerButton class="sm:hidden" @click="activateMenu($event)"/>

        <div class="navbar__adaptive-block sm:hidden" ref="ADAPTIVE_MENU">
            <ul class="navbar__adaptive-block__menu-list">
                <li class="navbar__adaptive-block__menu-list__item">
                    <router-link :to="{ name: 'home' }">Home</router-link>
                </li>
                <li class="navbar__adaptive-block__menu-list__item">
                    <router-link :to="{ name: 'catalog' }">Catalog</router-link>
                </li>
                <li class="navbar__adaptive-block__menu-list__item">
                    <router-link>Gallery</router-link>
                </li>
                <li class="navbar__adaptive-block__menu-list__item">
                    <router-link>Cart</router-link>
                </li>
            </ul>
        </div>
    </nav>
</template>

<script lang="ts" setup>
import HamburgerButton from '@/components/ui/HamburgerButton.vue'
import { ref } from 'vue'

const ADAPTIVE_MENU = ref(null)

/**
 * Toggles the 'active' class on the hamburger button when clicked.
 *
 * This function accounts for clicks on child elements (like <span>)
 * inside the button by traversing up the DOM tree until it finds
 * the actual <button> element, then toggles the 'active' class on it.
 *
 * This ensures consistent behavior regardless of which part of the
 * button was clicked.
 */
function activateMenu(e: Event) {
    if (!e.currentTarget) return
    (e.currentTarget as HTMLElement).classList.toggle('active')

    // Make sure the ADAPTIVE_MENU exists (is not null)
    if (!ADAPTIVE_MENU.value) return
    (ADAPTIVE_MENU.value as HTMLElement).classList.toggle('active')
}
</script>

<style lang="scss">
.navbar {
    @apply w-full h-12 bg-white px-8 sm:px-16 py-4 text-dark fixed top-0 left-0 z-10;

    &__logo {
        @apply ml-4 tracking-[14%] uppercase font-bold font-roboto;
    }

    &__menu-list {
        &__item {
            @apply font-medium mr-10 relative text-sm;

            &:last-child {
                @apply mr-0;
            }

            &::before {
                content: "";
                position: absolute;
                bottom: 0;
                transform: translateY(100%);
                height: 2px;
                width: 0;
                background-color: currentColor;
                transition: width 300ms ease, left 300ms ease, right 300ms ease;
            }

            &:hover::before {
                width: 100%;
                left: 0;
                right: auto;
            }

            /* When mouse leaves, shrink from right to left */
            &:not(:hover)::before {
                width: 0;
                right: 0;
                left: auto;
            }


            &:hover {
                &::before {
                    content: "";
                    animation: navbar-link-hover 300ms linear;
                }
            }
        }
    }

    // adaptive menu
    &__adaptive-block {
        height: calc(100vh - 3rem);
        @apply fixed top-12 right-0 w-screen bg-white flex justify-center items-center
               translate-x-full ease-in-out duration-300;

        &.active {
            @apply translate-x-0;
        }

        &__menu-list {
            &__item {
                @apply text-4xl mr-0 mb-10 text-center;

                &:last-child {
                    @apply mb-0;
                }
            }
        }
    }
}
</style>