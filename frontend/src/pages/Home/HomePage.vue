<template>
    <div>
        <HeaderBlock />

        <AboutUsBlock />

        <TrendingProductsBlock />

        <AdvantagesBlock />

        <FeedbackBlock />

        <LocationMap />
    </div>
</template>

<script lang="ts" setup>
import LocationMap from "@/pages/Home/LocationMap.vue"
import HeaderBlock from "@/pages/Home/HeaderBlock.vue"
import AboutUsBlock from "@/pages/Home/AboutUsBlock.vue"
import TrendingProductsBlock from "@/pages/Home/TrendingProductsBlock.vue"
import AdvantagesBlock from "@/pages/Home/AdvantagesBlock.vue"
import FeedbackBlock from "@/pages/Home/FeedbackBlock.vue"
</script>