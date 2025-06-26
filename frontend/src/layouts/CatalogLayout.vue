<template>
    <div class="font-outfit">
        <AppNavbar />

        <div class="main-content max-w-screen-w">
            <FilterBar class="filter-bar" />

            <main>
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
    @apply w-full flex justify-between px-8 md:px-16 py-16;

    .filter-bar {
        @apply sticky top-12 left-0 h-full;
        height: calc(100vh - 3rem * 2);
    }
}
</style>