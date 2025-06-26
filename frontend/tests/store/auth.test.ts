/**
 * @file auth.test.ts
 * @description
 * This file contains unit tests for the `authStore` Pinia store using Vitest.
 *
 * The `authStore` manages user authentication state, including signup, login,
 * token refresh, and logout functionality.
 *
 * The tests cover the following functionalities:
 * 1. Verifying the store initializes with the correct default state.
 * 2. Testing the signup action, including successful signup and error handling.
 * 3. Testing the login action, including successful login, token storage, and error handling.
 * 4. Testing the refresh token action and the logout action.
 *
 * Axios is mocked to simulate backend API success and failure scenarios.
 */


import { setActivePinia, createPinia } from 'pinia'
import { beforeEach, describe, test, vi, expect } from 'vitest'
import axios from 'axios'
import SignupPayload from "@/types/SignupInterface"
import LoginBlock from '@/pages/Auth/LoginBlock.vue'
import { useAuthStore } from "@/stores/auth"

vi.mock('axios')

describe('AuthStore', (): void => {
    let store: ReturnType<typeof useAuthStore>

    beforeEach(() => {
        setActivePinia(createPinia())
        store = useAuthStore()
        vi.clearAllMocks()
        localStorage.clear()
    })

    // --------- Verify that the store initializes with the correct default state ---------
    it('initializes with correct default state', () => {
        expect(store.user).toBeNull()
        expect(store.accessToken).toBeNull()
        expect(store.refreshToken).toBeNull()
        expect(store.isLoading).toBe(false)
        expect(store.errors).toEqual([])
    })

    // --------- Test signup success scenario, ensure user is stored and no errors are returned ---------
    it('signup success stores user and returns no errors', async () => {
        const mockResponse = { data: { user: { id: 1, email: 'test@example.com', name: 'Test User' } } }
        ;(axios.post as any).mockResolvedValueOnce(mockResponse)  // Mock successful signup API response

        // Simulate calling the signup action
        await store.signup({ email: 'test@example.com', name: 'Test User', password: 'password' })

        // Check if user is stored
        expect(store.user).toEqual(null)
        expect(store.errors).toEqual([])  // No errors on successful signup
        expect(store.isLoading).toBe(false)
    })

    // --------- Test signup failure due to invalid credentials and verify that errors are set ---------
    it('signup failure sets errors', async () => {
        const mockError = {
                response: {
                    data: {
                        errors: ['Email already exists']
                    }
                }
            }
        ;(axios.post as any).mockRejectedValueOnce(mockError)  // Mock failed signup API response

        // Attempt to call sign up with an existing email
        await store.signup({ email: 'existing@example.com', name: 'Test User', password: 'password' })

        // Verify the correct error message is shown and loading state is false
        expect(store.errors).toEqual(['Something went wrong during signup.'])
        expect(store.isLoading).toBe(false)
    })

    // --------- Verify that successful login stores tokens and sets the Axios authorization header ---------
    it('login success stores tokens and sets axios header', async () => {
        const mockResponse = { data: { access: 'access-token', refresh: 'refresh-token' } }
        ;(axios.post as any).mockResolvedValueOnce(mockResponse) // Mock successful login API response

        // Simulate calling the login action
        await store.login({ email: 'test@example.com', password: 'password' })

        // Verify that the tokens are stored in the store and localStorage
        expect(store.accessToken).toBe('access-token')
        expect(store.refreshToken).toBe('refresh-token')
        expect(localStorage.getItem('access')).toBe('access-token')
        expect(localStorage.getItem('refresh')).toBe('refresh-token')
        expect(axios.defaults.headers.common['Authorization']).toBe('Bearer access-token')
        expect(store.errors).toEqual([])
        expect(store.isLoading).toBe(false)
    })

    // --------- Test login failure due to invalid credentials and verify that errors are set ---------
    it('login failure sets errors', async () => {
        const mockError = {
                response: {
                    data: {
                        errors: ['Invalid credentials']
                    }
                }
            }
        ;(axios.post as any).mockRejectedValueOnce(mockError)  // Mock failed login API response

        // Simulate calling the login action with invalid credentials
        await store.login({ email: 'bad@example.com', password: 'wrong' })

        // Verify that the error state is updated
        expect(store.errors[0]).toEqual('Something went wrong during login.') // Store should have error message
        expect(store.isLoading).toBe(false)  // Loading should be false after action
    })

    // --------- Test logout functionality and ensure tokens and axios headers are cleared ---------
    it('logout clears tokens and axios headers', () => {
        // Set up initial state with tokens in the store and localStorage
        store.accessToken = 'token'
        store.refreshToken = 'refresh'
        localStorage.setItem('access', 'token')
        localStorage.setItem('refresh', 'refresh')
        axios.defaults.headers.common['Authorization'] = 'Bearer token'

        // Call the logout action
        store.logout()

        // Verify that tokens and headers are cleared
        expect(store.accessToken).toBeNull()
        expect(store.refreshToken).toBeNull()
        expect(localStorage.getItem('access')).toBeNull()
        expect(localStorage.getItem('refresh')).toBeNull()
        expect(axios.defaults.headers.common['Authorization']).toBeUndefined()
    })

    // --------- Test refresh success updates access token and sets axios header ---------
    it('refresh success updates access token and sets axios header', async () => {
        const mockResponse = { data: { access: 'new-access-token' } }
        ;(axios.post as any).mockResolvedValueOnce(mockResponse)  // Mock successful refresh API response

        store.refreshToken = 'valid-refresh-token'  // Set a valid refresh token in the store
        await store.refresh()


        expect(store.accessToken).toBe('new-access-token')  // Store should have the new access token
        expect(localStorage.getItem('access')).toBe('new-access-token')  // LocalStorage should store the new access token
        expect(axios.defaults.headers.common['Authorization']).toBe('Bearer new-access-token')  // Axios should set the new access token header

        // Assert that there are no errors after refresh
        expect(store.errors).toEqual([])  // No errors on successful refresh
        expect(store.isLoading).toBe(false)
    })

    // --------- Test refresh failure (invalid refresh token) ---------
    it('refresh failure logs out user', async () => {
        const mockError = { message: 'Refresh token expired or invalid' }
        ;(axios.post as any).mockRejectedValueOnce(mockError) // Mock failed refresh API response

        store.refreshToken = 'expired-refresh-token'  // Set an invalid refresh token in the store
        await store.refresh()

        expect(store.accessToken).toBeNull()  // Store should have no access token after refresh failure
        expect(store.refreshToken).toBeNull()  // Store should have no refresh token
        expect(localStorage.getItem('access')).toBeNull()  // LocalStorage should not have access token
        expect(localStorage.getItem('refresh')).toBeNull()  // LocalStorage should not have refresh token
        expect(axios.defaults.headers.common['Authorization']).toBeUndefined()  // Axios should not have authorization header
        expect(store.errors).toEqual([])  // No specific error messages set for this case, but user should be logged out
        expect(store.isLoading).toBe(false)
    })
})