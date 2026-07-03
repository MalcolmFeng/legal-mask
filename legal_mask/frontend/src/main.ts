import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import Workspace from './views/Workspace.vue'
import Review from './views/Review.vue'
import Settings from './views/Settings.vue'

const routes = [
  { path: '/', component: Workspace },
  { path: '/review/:id', component: Review },
  { path: '/settings', component: Settings },
]

const router = createRouter({ history: createWebHistory(), routes })
const app = createApp(App)
app.use(createPinia())
app.use(router)
app.mount('#app')
