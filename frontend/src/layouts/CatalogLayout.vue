<template>
    <div class="font-outfit">
        <AppNavbar />

        <div class="main-content max-w-screen-w mx-auto">
            <FilterBar class="filter-bar" />

            <main class="w-full">
                <slot />
            </main>
        </div>

        <AppFooter />
    </div>
</template>

<script setup lang="ts">
import { onMounted, onBeforeUnmount, ref } from 'vue'
import AppNavbar from "@/components/ui/AppNavbar.vue"
import AppFooter from "@/components/ui/AppFooter.vue"
import FilterBar from "@/pages/Catalog/FilterBar.vue"
</script>

<style lang="scss" scoped>
.main-content {
    @apply w-full flex flex-col lg:flex-row justify-between px-8 md:px-16 py-16;

    .filter-bar {
        @apply top-12 left-0 h-full w-full mb-10 lg:sticky lg:w-[350px] lg:mb-0;
    }
}

@media (min-width: 1024px) {
    .filter-bar {
        height: calc(100vh - 3rem * 2) !important;
    }
}
</style>