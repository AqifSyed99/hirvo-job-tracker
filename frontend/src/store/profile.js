import { defineStore } from 'pinia'
import axios from 'axios'

export const useProfileStore = defineStore('profile', {
  state: () => ({
    profile: null,
    loading: false,
    error: null,
  }),

  actions: {
    async fetchProfile() {
      this.loading = true
      this.error = null
      try {
        const response = await axios.get('/api/profile/')
        this.profile = response.data
      } catch (err) {
        this.error = err.response?.data?.error || err.message
      } finally {
        this.loading = false
      }
    },

    async updateProfile(data) {
      this.loading = true
      this.error = null
      try {
        let payload
        if (data.avatar instanceof File) {
          payload = new FormData()
          Object.entries(data).forEach(([key, val]) => {
            if (val !== null && val !== undefined) payload.append(key, val)
          })
        } else {
          payload = data
        }
        const response = await axios.put('/api/profile/', payload)
        this.profile = response.data
        return response.data
      } catch (err) {
        this.error = err.response?.data?.error || err.message
        throw err
      } finally {
        this.loading = false
      }
    },

    clearError() {
      this.error = null
    },
  },
})
