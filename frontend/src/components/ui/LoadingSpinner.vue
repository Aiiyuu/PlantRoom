<template>
    <div class="spinner"></div>
</template>

<style>
.spinner {
    @apply w-16 h-16 border-solid border-8 border-olive-grove border-r-white rounded-full;
    animation: spinner 1s linear infinite;
}

@keyframes spinner {
    from {
        transform: rotate(0);
    }
    to {
        transform: rotate(360deg);
    }
}
</style>