import './assets/main.css'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import axios from 'axios'
import App from './App.vue'
import router from './router'

// Configure axios base URL
axios.defaults.baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000'

// Request interceptor: attach JWT token if present
axios.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Response interceptor: handle 401 only for our own backend
axios.interceptors.response.use(
  (response) => response,
  (error) => {
    const requestUrl = error.config?.url || ''
    const baseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000'
    // Only auto-logout on 401s from our own backend, not external services like Cloudinary
    const isOwnBackend = requestUrl.startsWith('/api') || requestUrl.startsWith(baseUrl)
    if (error.response && error.response.status === 401 && isOwnBackend) {
      localStorage.removeItem('token')
      router.push('/login')
    }
    return Promise.reject(error)
  }
)

const app = createApp(App)

app.use(router)
app.use(createPinia())

app.mount('#app')
