<template>
    <div class="modal-overlay">
        <div class="modal-content signup">
            <div class="auth-image"></div>

            <form class="auth" @submit.prevent="handleSignupForm">
                <div>
                    <h1 class="auth-title">Welcome to PlantRoom!</h1>
                    <p class="auth-text">
                        Discover your perfect plant companions and turn your space into a green oasis. Let’s grow together — create your account to get started!                    </p>
                </div>

                <div v-for="(value, key) in formData" :key="key" class="input-field">
                    <input
                        v-model="formData[key]"
                        :name="key"
                        :id="key"
                        :type="getInputType(key)"
                        :class="{
                            filled: formData[key].trim() !== ''
                        }"
                    />
                    <label :for="key">{{ key }}</label>

                    <button
                        v-if="key === 'password'"
                        class="toggle-password"
                        :class="{ 'eye-show': showPassword, 'eye-off': !showPassword }"
                        type="button"
                        @click="togglePasswordVisibility"
                    >
                    </button>
                </div>

                <div>
                    <p class="auth-text">
                        Already have an account?
                        <router-link :to="{ name: 'login' }">Log in</router-link>
                        and reconnect with your plants.
                    </p>
                </div>

                <!-- Error Messages -->
                <div v-if="formErrors.length" class="form-errors">
                    <ul>
                        <li v-for="(error, index) in formErrors" :key="index">{{ error }}</li>
                    </ul>
                </div>

                <BaseButton
                    class="auth-submit-btn"
                    text="Sign up"
                    color="#2CA165"
                    textColor="#F2F2F2"
                    rotate="0deg"
                    type="submit"
                />
            </form>

            <router-link :to="{ name: 'home' }" class="go-home-button">
                <span></span>
            </router-link>
        </div>
    </div>
</template>

<script lang="ts" setup>
import BaseButton from "@/components/ui/BaseButton.vue"
import {reactive, ref} from 'vue'
import SignupPayload from "@/types/SignupInterface"
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

// Pinia store instance
const auth = useAuthStore()

// Vue Router instance (for redirection after signup)
const router = useRouter()


/* --------- Form management --------- */

// Form data
const formData = reactive<SignupPayload>({
    name: '',
    email: '',
    password: '',
})

// Error state
const formErrors = ref<string[]>([])

async function handleSignupForm() {
    formErrors.value = [] // Clear previous errors

    // Try calling the signup action from the store
    const response = await auth.signup({
        name: formData.name,
        email: formData.email,
        password: formData.password,
    })

    // If successful, redirect to login or home
    if (!auth.errors.length) {
        router.push({ name: 'login' })
    } else {
        auth.errors.forEach(error => {
            if (!formErrors.value.includes(error)) {
                formErrors.value.push(error);
            }
        });
    }
}


/* --------- Password toggle button --------- */

// Reactive ref to control password visibility
const showPassword = ref(false)

// Computed type for the password input
const getInputType = (key: string) => {
    if (key === 'password') {
        return showPassword.value ? 'text' : 'password'
    }

    return 'text'
}

// Toggle function
const togglePasswordVisibility = () => {
    showPassword.value = !showPassword.value
}
</script>