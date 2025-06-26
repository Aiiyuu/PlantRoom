/**
 * @file Signup.spec.ts
 * @description
 * This file contains unit tests for the `Signup.vue` component using Vitest and Vue Test Utils.
 *
 * The `Signup` component provides a signup form for new users to create an account.
 *
 * The tests cover the following functionalities:
 * 1. Rendering of form fields based on `formData`.
 * 2. Binding of input values to the component's state.
 * 3. Toggling password visibility.
 * 4. Submission behavior and error display.
 * 5. Navigation to the login page upon successful signup.
 *
 * The tests use mocked Pinia store and Vue Router to simulate and observe component behavior.
 */


import { describe, vi, it, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import SignupBlock from '@/pages/Auth/SignupBlock.vue'
import { useAuthStore } from "@/stores/auth"
import { createPinia, setActivePinia } from 'pinia'


// Mock vue-router before importing component
const pushMock = vi.fn()
vi.mock('vue-router', () => ({
    useRouter: () => ({
        push: pushMock
    })
}))


describe('SignupBlock.vue', (): void => {
    let wrapper: any
    let store: any

    // Setup before each test
    beforeEach((): void => {
        setActivePinia(createPinia())

        // Use real auth store and mock signup method
        store = useAuthStore()
        vi.spyOn(store, 'signup').mockResolvedValue(undefined)
        store.errors = []

        // Clear router push mock call history before each test
        pushMock.mockClear()

        wrapper = mount(SignupBlock)
    })

    // ----------- Verify that all form input fields (name, email, password) are rendered correctly -----------
    it('renders all form input fields', () => {
        // Find all input elements in the component
        const inputs = wrapper.findAll('.input-field input')

        // Check that there are exactly 3 inputs and they have the correct name attributes
        expect(inputs).toHaveLength(3)
        expect(inputs[0].attributes('name')).toBe('name')
        expect(inputs[1].attributes('name')).toBe('email')
        expect(inputs[2].attributes('name')).toBe('password')
    })

    // ----------- Verify that input values are correctly bound to formData -----------
    it('binds input values to formData', async () => {
        // Find all input fields
        const nameInput = wrapper.find('input[name="name"]')
        const emailInput = wrapper.find('input[name="email"]')
        const passwordInput = wrapper.find('input[name="password"]')

        // Simulate user typing an email, name and password
        nameInput.setValue('test')
        emailInput.setValue('test@example.com')
        passwordInput.setValue('password')

        // Assert that the formData.[inputName] value is updated accordingly
        expect(wrapper.vm.formData.name).toBe('test')
        expect(wrapper.vm.formData.email).toBe('test@example.com')
        expect(wrapper.vm.formData.password).toBe('password')
    })

    // ----------- Verify that clicking the toggle button changes password visibility state -----------
    it('toggles password visibility', async () => {
        // Find the element responsible for toggling password visibility
        const toggle = wrapper.find('.toggle-password')

        // Initially, password should be hidden
        expect(wrapper.vm.showPassword).toBe(false)

        // Simulate clicking the toggle to show the password
        await toggle.trigger('click')
        expect(wrapper.vm.showPassword).toBe(true)

        // Simulate clicking the toggle again to hide the password
        await toggle.trigger('click')
        expect(wrapper.vm.showPassword).toBe(false)
    })

    // ----------- Verify that signup is called and navigation to login occurs when there are no errors -----------
    it('calls signup and navigates to login if no errors', async () => {
        // Make sure no errors
        store.errors = []

        // Call the signup handler method on the component instance
        await wrapper.vm.handleSignupForm()

        // Verify that the signup method on the store was called exactly once
        expect(store.signup).toHaveBeenCalledOnce()
        expect(pushMock).toHaveBeenCalledWith({ name: 'login' })
    })

    // ----------- Verify that error messages from the auth store are displayed correctly in the signup form -----------
    it('displays error messages from auth store', async () => {
        // Simulate error messages returned from the auth store
        store.errors = ['Invalid email', 'Password too short']

        // Trigger the signup form submission handler, which should process these errors
        await wrapper.vm.handleSignupForm()

        // Find all list items inside the element with class 'form-errors' that display errors
        const errors = wrapper.findAll('.form-errors li')

        // Verify that the correct number of error messages are displayed and their text content is accurate
        expect(errors).toHaveLength(2)
        expect(errors[0].text()).toBe('Invalid email')
        expect(errors[1].text()).toBe('Password too short')
    })
})