<template>
    <DefaultLayout>
        <router-view/>
    </DefaultLayout>
</template>

<script lang="ts" setup>
import DefaultLayout from "@/layouts/DefaultLayout.vue";
</script>

<style lang="scss">
* {
    @apply font-outfit;
}
//nav {
//  a {
//    font-weight: bold;
//    color: #2c3e50;
//
//    &.router-link-exact-active {
//      color: #42b983;
//    }
//  }
//}
</style>