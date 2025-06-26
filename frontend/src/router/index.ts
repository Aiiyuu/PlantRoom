import {createRouter, createWebHistory, RouteRecordRaw} from 'vue-router'
import HomePage from '@/pages/Home/HomePage.vue'
import LoginBlock from "@/pages/Auth/LoginBlock.vue"
import SignupBlock from "@/pages/Auth/SignupBlock.vue"
import CatalogPage from "@/pages/Catalog/CatalogPage.vue"

const routes: Array<RouteRecordRaw> = [
    {
        path: '/',
        name: 'home',
        component: HomePage
    },
    {
        path: '/auth',
        name: 'auth',
        component: LoginBlock,
        redirect: '/auth/login', // Default to login if just /auth is visited
        meta: { layout: 'AuthLayout' },
        children: []
    },
    {
        path: '/auth/login',
        name: 'login',
        component: LoginBlock,
        meta: { layout: 'AuthLayout' }
    },
    {
        path: '/auth/signup',
        name: 'signup',
        component: SignupBlock,
        meta: { layout: 'AuthLayout' }
    },
    {
        path: '/catalog',
        name: 'catalog',
        component: CatalogPage,
        meta: { layout: 'DefaultLayout' },
    }
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

export default router
