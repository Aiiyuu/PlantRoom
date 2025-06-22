<template>
    <div>
        <HeaderBlock />

        <AboutUsBlock />

        <TrendingProductsBlock />

        <LocationMap />
    </div>
</template>

<script lang="ts" setup>
import LocationMap from "@/pages/Home/LocationMap.vue"
import HeaderBlock from "@/pages/Home/HeaderBlock.vue"
import AboutUsBlock from "@/pages/Home/AboutUsBlock.vue"
import TrendingProductsBlock from "@/pages/Home/TrendingProductsBlock.vue"
</script>