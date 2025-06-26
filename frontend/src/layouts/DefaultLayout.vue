<template>
    <div class="default-layout font-outfit">
        <AppNavbar />

        <main class="max-w-screen-w mx-auto">
            <slot />
        </main>

        <AppFooter class="max-w-screen-w mx-auto" />
    </div>
</template>

<script setup lang="ts">
import AppNavbar from "@/components/ui/AppNavbar.vue";
import AppFooter from "@/components/ui/AppFooter.vue";
</script>
