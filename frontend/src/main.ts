import { createApp } from 'vue'
import App from './App.vue'
import { createPinia } from 'pinia'
import router from './router'
import axios from 'axios'

// Import styles
import './assets/styles/tailwind.css'

// Set the default baseURL for all Axios requests
axios.defaults.baseURL = 'http://127.0.0.1:8000/api/v1/'

const app = createApp(App)

// Set the global image base URL
app.config.globalProperties.$imageBaseUrl = 'http://127.0.0.1:8000/'

// Create Pinia instance
const pinia = createPinia()

app.use(pinia)    // <-- register Pinia
app.use(router)   // <-- register router

// Inject the $imageBaseUrl globally
app.provide('$imageBaseUrl', 'http://127.0.0.1:8000/')

app.mount('#app')
