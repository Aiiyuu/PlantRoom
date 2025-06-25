<template>
    <div class="modal-overlay">
        <div class="modal-content login">
            <div class="auth-image"></div>

            <form class="auth" @submit.prevent="handleLoginForm">
                <div>
                    <h1 class="auth-title">Welcome back to PlantRoom!</h1>
                    <p class="auth-text">
                        We’re glad you’re back. Let’s pick up where you left off and keep your green journey thriving.
                    </p>
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
                        New here?
                        <router-link :to="{ name: 'signup' }">Create an account</router-link>
                        and start your PlantRoom journey.
                    </p>
                </div>

                <BaseButton
                    class="auth-submit-btn"
                    text="Login"
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

// Represents a login object
interface LoginFormData {
    email: string
    password: string
}

// Form data
const formData = reactive<LoginFormData>({
    email: '',
    password: '',
})

function handleLoginForm() {
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