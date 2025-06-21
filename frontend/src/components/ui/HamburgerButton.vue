<template>
    <!-- Hamburger button container -->
    <div
        class="hamburger-button"
        @mouseenter="onMouseEnter($event)"
        @mouseleave="onMouseLeave"
        ref="buttonRef">

    <div class="hamburger-button__wrapper">
        <!-- Hamburger lines with individual refs -->
        <span class="hamburger-button__wrapper__line" ref="line1Ref"></span>
        <span class="hamburger-button__wrapper__line" ref="line2Ref"></span>
        <span class="hamburger-button__wrapper__line" ref="line3Ref"></span>
    </div>
    </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

// Refs to each line
const line1Ref = ref<HTMLSpanElement | null>(null)
const line2Ref = ref<HTMLSpanElement | null>(null)
const line3Ref = ref<HTMLSpanElement | null>(null)

// Arrays to store timeouts for add/remove actions
let enterTimeouts: number[] = []
let leaveTimeouts: number[] = []

/**
 * Handle mouseenter:
 * Add 'offset' class to each line with a delay
 */
function onMouseEnter(event: Event) {
    clearAllTimeouts() // Prevent overlapping effects

    // Make sure the button does not contain the 'active' class
    if(event.target.classList.contains('active')) return

    enterTimeouts.push(
        window.setTimeout(() => {
            line1Ref.value?.classList.add('offset')
        }, 100),
        window.setTimeout(() => {
            line2Ref.value?.classList.add('offset')
        }, 300),
        window.setTimeout(() => {
            line3Ref.value?.classList.add('offset')
        }, 600)
    )
}

/**
 * Handle mouseleave:
 * Remove 'offset' class from each line with a delay
 */
function onMouseLeave() {
    clearAllTimeouts() // Cancel any add timeouts

    leaveTimeouts.push(
        window.setTimeout(() => {
            line1Ref.value?.classList.remove('offset')
        }, 100),
        window.setTimeout(() => {
            line2Ref.value?.classList.remove('offset')
        }, 300),
        window.setTimeout(() => {
            line3Ref.value?.classList.remove('offset')
        }, 600)
    )
}

/**
 * Clear all pending timeouts
 */
function clearAllTimeouts() {
    [...enterTimeouts, ...leaveTimeouts].forEach(id => clearTimeout(id))
    enterTimeouts = []
    leaveTimeouts = []
}
</script>



<style lang="scss" scoped>
.hamburger-button {
    @apply relative w-6 h-6 cursor-pointer rotate-45 overflow-hidden;

    &::before {
        content: "";
        @apply w-6 h-6 absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2
        border-solid border border-dark -rotate-90 ease-in-out duration-700;
    }

    &__wrapper {
        @apply relative w-4 h-3 m-auto translate-y-1/2 -rotate-45;

        &__line {
            @apply absolute w-full left-0 h-0.5 bg-dark ease-in-out duration-500;

            &::before {
                content: "";

                @apply absolute w-full h-0.5 bg-dark -left-full -translate-x-full
                       ease-in-out duration-500;
            }

            &:nth-child(1), &:nth-child(1)::before {
                @apply top-0;
            }

            &:nth-child(2), &:nth-child(2)::before {
                @apply top-1/2 -translate-y-1/2;
            }

            &:nth-child(3), &:nth-child(3)::before {
                @apply bottom-0;
            }

            &.offset {
                @apply translate-x-full left-full;
            }
        }
    }

    &.active {
        .hamburger-button__wrapper {
            .hamburger-button__wrapper__line {
                @apply delay-0 origin-center absolute;

                top: 50% !important;
                left: 50% !important;
                right: auto !important;
                bottom: auto !important;
                transform-origin: center center !important;
                transform: translate(-50%, -50%) !important;

                &:nth-child(1) {
                    transform: translate(-50%, -50%) rotate(45deg)!important;
                }
                &:nth-child(2) {
                    opacity: 0;
                }
                &:nth-child(3) {
                    transform: translate(-50%, -50%) rotate(-45deg)!important;
                }
            }
        }
    }
}
</style>