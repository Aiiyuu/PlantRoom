
import { defineStore } from 'pinia'
import User from '@/types/UserInterface'
import SignupPayload from '@/types/SignupInterface'
import LoginPayload from '@/types/LoginInterface'
import axios, { AxiosResponse } from 'axios'

export const useAuthStore = defineStore('auth', {
    state: () => ({
        user: null, // Can be used to store user info later
        accessToken: localStorage.getItem('accessToken') || null, // JWT access token
        refreshToken: localStorage.getItem('refreshToken') || null, // JWT refresh token
        isLoading: false,
        errors: [] as string[]
    }),

    getters: {
        // Returns true if the user is authenticated (access token exists)
        isAuthenticated: state => !!state.accessToken
    },

    actions: {
        // Handle user signup (registration)
        async signup(payload: SignupPayload): Promise<void>  {
            this.isLoading = true
            this.errors = []

            try {
                // Send POST request to backend signup endpoint
                const response = await axios.post('user/signup/', {
                    email: payload.email,
                    name: payload.name,
                    password1: payload.password,
                    password2: payload.password,
                })

            } catch (error: unknown) {
                // Handle and store validation errors from backend
                if (axios.isAxiosError(error)) {
                    // Now error is typed as AxiosError
                    if (error.response?.data?.errors) {
                        this.errors = error.response.data.errors
                    }
                } else {
                    this.errors = ['Something went wrong during signup.']
                }
            } finally {
                this.isLoading = false
            }
        },

        // Handle login using email and password
        async login(payload: LoginPayload): Promise<void>  {
            this.isLoading = true
            this.errors = []

            try {
                // Send POST request to backend JWT login endpoint
                const response = await axios.post('user/login/', {
                    email: payload.email,
                    password: payload.password,
                })

                // Extract tokens from response
                const { access, refresh } = response.data

                // Save tokens to state
                this.accessToken = access
                this.refreshToken = refresh

                // Persist tokens in local storage for session persistence
                localStorage.setItem('access', access)
                localStorage.setItem('refresh', refresh)

                // Set default Authorization header for future requests
                axios.defaults.headers.common['Authorization'] = `Bearer ${access}`

            } catch (error: unknown) {
                // Handle and store validation errors from backend
                if (axios.isAxiosError(error)) {
                    // Now error is typed as AxiosError
                    if (error.response?.data?.errors) {
                        this.errors = error.response.data.errors
                    }
                } else {
                    this.errors = ['Something went wrong during login.']
                }
            } finally {
                this.isLoading = false
            }
        },

        // Refresh the access token using the refresh token
        async refresh(): Promise<void>  {
            try {
                const response = await axios.post('user/refresh/', {
                    refresh: this.refreshToken,
                })

                // Update access token in state and local storage
                this.accessToken = response.data.access
                if (this.accessToken) {
                    localStorage.setItem('access', this.accessToken)
                }

                // Update the default Authorization header
                axios.defaults.headers.common['Authorization'] = `Bearer ${this.accessToken}`

            } catch (error) {
                // If refresh fails (e.g. token expired), log out the user
                this.logout()
            }
        },

        // Log out the user by clearing tokens and headers
        logout(): void {
            this.user = null
            this.accessToken = null
            this.refreshToken = null

            // Remove tokens from local storage
            localStorage.removeItem('access')
            localStorage.removeItem('refresh')

            // Remove Authorization header from axios
            delete axios.defaults.headers.common['Authorization']
        }
    }
})