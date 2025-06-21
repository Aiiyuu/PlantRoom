<template>
    <div class="default-layout">
        <AppNavbar />

        <main>
            <slot />
        </main>

        <AppFooter />
    </div>
</template>

<script setup lang="ts">
import AppNavbar from "@/components/ui/AppNavbar.vue";
import AppFooter from "@/components/ui/AppFooter.vue";
</script>