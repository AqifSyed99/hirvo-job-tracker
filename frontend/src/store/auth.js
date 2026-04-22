import { defineStore } from 'pinia'
import axios from 'axios'
import router from '../router'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: JSON.parse(localStorage.getItem('user') || 'null'),
  }),

  getters: {
    isAuthenticated: (state) => {
      if (!state.token) return false
      // Check token expiry by decoding the JWT payload
      try {
        const payload = JSON.parse(atob(state.token.split('.')[1]))
        return payload.exp * 1000 > Date.now()
      } catch {
        return false
      }
    },
  },

  actions: {
    async register(email, password, fullName = '') {
      try {
        const response = await axios.post('/api/auth/register', { email, password, full_name: fullName })
        return response.data
      } catch (error) {
        throw error
      }
    },

    async login(email, password) {
      try {
        const response = await axios.post('/api/auth/login', { email, password })
        const { token, user } = response.data
        this.token = token
        this.user = user
        localStorage.setItem('token', token)
        localStorage.setItem('user', JSON.stringify(user))
        router.push('/dashboard')
      } catch (error) {
        throw error
      }
    },

    logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      router.push('/login')
    },
  },
})
