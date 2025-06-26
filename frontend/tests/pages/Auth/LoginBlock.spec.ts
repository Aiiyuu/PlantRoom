/**
 * @file Login.spec.ts
 * @description
 * Unit tests for the `Login.vue` component using Vitest and Vue Test Utils.
 *
 * The `Login` component provides a login form for returning users.
 *
 * The tests cover the following functionalities:
 * 1. Rendering of email and password input fields.
 * 2. Binding of input values to the component’s reactive formData.
 * 3. Toggling password visibility via button.
 * 4. Handling form submission, calling the login action and redirecting on success.
 * 5. Displaying error messages from the auth store.
 */

import { describe, vi, it, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import LoginBlock from "@/pages/Auth/LoginBlock.vue"
import { useAuthStore } from "@/stores/auth"
import { createPinia, setActivePinia } from 'pinia'


// Mock vue-router before importing component
const pushMock = vi.fn()
vi.mock('vue-router', () => ({
    useRouter: () => ({
        push: pushMock
    })
}))

describe('LoginBlock.vue', (): void => {
    let wrapper: any
    let store: any

    // Setup before each test
    beforeEach((): void => {
        setActivePinia(createPinia())

        // Use real auth store and mock signup method
        store = useAuthStore()
        vi.spyOn(store, 'login').mockResolvedValue(undefined)
        store.errors = []

        // Clear router push mock call history before each test
        pushMock.mockClear()

        wrapper = mount(LoginBlock)
    })

    // ----------- Verify that all form input fields (email, password) are rendered correctly -----------
    it('renders all form input fields', () => {
        // Find all input elements in the component
        const inputs = wrapper.findAll('.input-field input')

        // Check that there are exactly 2 inputs and they have the correct name attributes
        expect(inputs).toHaveLength(2)
        expect(inputs[0].attributes('name')).toBe('email')
        expect(inputs[1].attributes('name')).toBe('password')
    })

    // ----------- Verify that input values are correctly bound to formData -----------
    it('binds input values to formData', async () => {
        // Find all input fields
        const emailInput = wrapper.find('input[name="email"]')
        const passwordInput = wrapper.find('input[name="password"]')

        // Simulate user typing an email, name and password
        emailInput.setValue('test@example.com')
        passwordInput.setValue('password')

        // Assert that the formData.[inputName] value is updated accordingly
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

    // ----------- Verify that login is called and navigation to home occurs when there are no errors -----------
    it('calls login and navigates to home if no errors', async () => {
        // Populate formData to simulate form submission
        wrapper.vm.formData.email = 'user@example.com'
        wrapper.vm.formData.password = 'mypassword'

        // Make sure no errors
        store.errors = []

        // Simulate successful login by setting accessToken to a non-null string
        store.accessToken = 'fake-access-token'

        // Call the login handler method on the component instance
        await wrapper.vm.handleLoginForm()

        // Verify that the login method on the store was called exactly once
        expect(store.login).toHaveBeenCalledOnce()

        // Verify navigation to home was triggered
        expect(pushMock).toHaveBeenCalledWith({name: 'home'})
    })

    // ----------- Verify that error messages from the auth store are displayed correctly in the login form -----------
    it('displays generic error if no specific errors returned', async () => {
        store.accessToken = null  // simulate unauthenticated user
        store.errors = []

        // Populate form data with valid email but incorrect password to simulate login attempt
        wrapper.vm.formData.email = 'user@example.com'
        wrapper.vm.formData.password = 'wrongpassword'

        // Call the form submission handler, which triggers the login process
        await wrapper.vm.handleLoginForm()
        await wrapper.vm.$nextTick() // Wait for DOM updates after async action

        // Find all error messages displayed in the form error list
        const errors = wrapper.findAll('.form-errors li')

        // Assert that exactly one error message is shown
        expect(errors).toHaveLength(1)

        // Assert that the displayed error message is the generic fallback message
        expect(errors[0].text()).toBe('Something went wrong during login.')
    })
})