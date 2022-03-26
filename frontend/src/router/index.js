import { createRouter, createWebHistory } from 'vue-router'
import Changes from '@/views/Changes.vue'

const routes = [
    {
        path: '/:ticker',
        name: 'Ticker',
        component: Changes,
        props: true
    },
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

export default router