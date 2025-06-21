/**
 * Tests for the AppNavbar component.
 * - Verifies that the component renders correctly.
 * - Ensures the adaptive menu toggles visibility with the hamburger button.
 * - Stubs router-link since it's provided by Vue Router.
 */

import { describe, it, expect } from "vitest";
import { mount } from "@vue/test-utils";
import AppNavbar from "@/components/ui/AppNavbar.vue";

describe("AppNavbar", (): void => {
    // ----------- Render Tests -----------
    it("renders without crashing", (): void => {
        const wrapper = mount(AppNavbar, {
            global: {
                stubs: {
                    'router-link': true,
                },
            },
        });
        expect(wrapper.exists()).toBe(true);
    });

    // ----------- Adaptive Menu Tests -----------
    it("toggles the adaptive menu visibility when hamburger button is clicked", async (): Promise<void> => {
        const wrapper = mount(AppNavbar, {
            global: {
                stubs: { 'router-link': true },
            },
        });

        // Find adaptation menu components
        const toggleButton = wrapper.find('.hamburger-button');
        const adaptiveMenu = wrapper.find(".navbar__adaptive-block");

        // Initially inactive
        expect(toggleButton.classes()).not.toContain('active');
        expect(adaptiveMenu.classes()).not.toContain('active');

        // First click: activate
        await toggleButton.trigger('click');
        expect(toggleButton.classes()).toContain('active');
        expect(adaptiveMenu.classes()).toContain('active');

        // Second click: deactivate
        await toggleButton.trigger('click');
        expect(toggleButton.classes()).not.toContain('active');
        expect(adaptiveMenu.classes()).not.toContain('active');
    });
});
