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


/* --------- Form management --------- */

// Represents a signup object
interface SignupFormData {
    name: string
    email: string
    password: string
}

// Form data
const formData = reactive<SignupFormData>({
    name: '',
    email: '',
    password: '',
})

function handleSignupForm() {
    return
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