import { createApp } from 'vue'
import App from './App.vue'
import VueApexCharts from "vue3-apexcharts";
import Chart from "./plugins/chart.js"
import router from './router'

createApp(App).use(router).use(Chart).use(VueApexCharts).mount('#app')