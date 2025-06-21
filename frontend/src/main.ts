import { createApp } from 'vue'
import App from './App.vue'
import { createPinia } from 'pinia'
import router from './router'
import axios from 'axios'

// Import styles
import './assets/styles/tailwind.css'

const app = createApp(App)

// Create Pinia instance
const pinia = createPinia()

app.use(pinia)    // <-- register Pinia
app.use(router)   // <-- register router

app.mount('#app')
