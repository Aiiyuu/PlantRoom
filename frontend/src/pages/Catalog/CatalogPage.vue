<template>
    <div class="catalog">
        <FilterBar />


    </div>
</template>

<script lang="ts" setup>
import { useInventoryStore } from "@/stores/inventory"
import Plant from '@/types/PlantInterface'
import FilterBar from "@/pages/Catalog/FilterBar.vue"
</script>

<style lang="scss" scoped>
    .catalog {
        @apply w-full min-h-screen p-8 md:px-16 flex justify-between;
    }
</style>