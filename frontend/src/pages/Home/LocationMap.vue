<template>
    <div id="location">
        <!-- Spinner -->
        <div class="w-full h-[450px] flex justify-center items-center" v-if="isLoading">
            <LoadingSpinner />
        </div>

        <!-- Google Maps iframe -->
        <iframe
            src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d4548.2015316000625!2d-0.12267802560681239!3d51.50593439442126!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x487605ebbdc4135f%3A0xa3d9c919fcf48887!2sThe%20Parlour!5e0!3m2!1sen!2suk!4v1750550308846!5m2!1sen!2suk"
            class="location-map"
            @load="isLoading = false"
            width="600"
            height="450"
            style="border:0;"
            allowfullscreen=""
            loading="lazy"
            referrerpolicy="no-referrer-when-downgrade"
        ></iframe>
    </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import LoadingSpinner from "@/components/ui/LoadingSpinner.vue"

const isLoading = ref(true)
</script>

<style scoped>
.location-map {
    @apply w-full h-[400px];
}
</style>