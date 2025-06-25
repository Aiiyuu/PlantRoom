<template>
    <!-- Dynamically render the layout -->
    <component :is="layout">
        <!-- The page content like HomePage, AuthPage, etc. will be injected here -->
        <router-view />
    </component>
</template>

<script lang="ts" setup>
import { ref, watchEffect } from 'vue'
import { useRoute } from 'vue-router' // Import useRoute from vue-router
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import AuthLayout from '@/layouts/AuthLayout.vue'

const route = useRoute() // Get current route object
const layout = ref(DefaultLayout) // Default layout is DefaultLayout

// Watch for route changes to update the layout
watchEffect(() => {
    // Ensure we're properly checking the route.meta.layout value
    const layoutMeta = route.meta.layout
    if (layoutMeta === 'AuthLayout') {
        layout.value = AuthLayout
    } else {
        layout.value = DefaultLayout
    }
})
</script>

<style lang="scss">
* {
    @apply font-outfit;
}

//    .router-link-exact-active {
//      color: #42b983;
//    }
</style>