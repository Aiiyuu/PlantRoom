import { defineConfig } from 'vitest/config';
import vue from '@vitejs/plugin-vue';
import path from 'path';

export default defineConfig({
    plugins: [vue()],
    resolve: {
        alias: {
            '@': path.resolve(__dirname, './src'),
        },
    },
    test: {
        globals: true,
        environment: 'jsdom', // Simulates a browser environment
        // Mock static assets like SVGs
        assets: {
            mock: 'empty', // This tells Vitest to mock all assets as empty
        },
    },
});
