<template>
    <button
        class="button-53"
        :type="type"
        :style="{ background: color, color: textColor, rotate: rotate }"
        role="button"
    >
        {{ text }}
    </button>
</template>

<script setup lang="ts">
const props = withDefaults(
    defineProps<{
        text: string;
        color?: string;
        textColor?: string;
        rotate?: number;
        size?: 'sm' | 'md' | 'lg';
        type?: 'submit' | 'reset' | 'button';
    }>(),
    {
        color: '#2CA165',
        textColor: '#FFFDF6',
        rotate: 0,
        type: 'button',
    }
)
</script>

<style lang="scss" scoped>
.button-53 {
    @apply bg-cyan-400 flex items-center justify-center font-bold w-full cursor-pointer
        ease-in-out duration-200 relative whitespace-nowrap text-sm flex items-center justify-center;

    line-height: 1.75rem;
}

.button-53:focus {
    outline: 0;
}

.button-53:after {
    content: '';
    width: calc(100% - 1px);
    height: calc(100% - 1px);

    @apply absolute ease-in-out duration-200 border-dark border-[1px] bottom-[4px] left-[4px];
}

.button-53:hover:after {
    @apply bottom-[2px] left-[2px];
}
</style>
