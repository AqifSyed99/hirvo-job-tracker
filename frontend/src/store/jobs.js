import { defineStore } from 'pinia'
import axios from 'axios'

export const useJobsStore = defineStore('jobs', {
  state: () => ({
    entries: [],
    selected: null,
    stats: null,
    loading: false,
    error: null,
  }),

  actions: {
    async fetchAll() {
      this.loading = true
      this.error = null
      try {
        const response = await axios.get('/api/jobs/')
        this.entries = response.data
        this.loading = false
      } catch (error) {
        this.error = error.response?.data?.error || error.message
        this.loading = false
        throw error
      }
    },

    async create(data) {
      this.loading = true
      this.error = null
      try {
        const payload = new FormData()
        const { files, removedAttachmentIds, ...rest } = data
        // Append scalar fields
        Object.entries(rest).forEach(([key, val]) => {
          if (val !== null && val !== undefined) payload.append(key, val)
        })
        // Append multiple files
        if (files && files.length) {
          files.forEach(f => payload.append('files', f))
        }
        const response = await axios.post('/api/jobs/', payload)
        this.entries.unshift(response.data)
        this.loading = false
        return response.data
      } catch (error) {
        this.error = error.response?.data?.error || error.message
        this.loading = false
        throw error
      }
    },

    async update(id, data) {
      this.loading = true
      this.error = null
      try {
        const { files, removedAttachmentIds, ...rest } = data

        // Delete removed attachments first
        if (removedAttachmentIds && removedAttachmentIds.length) {
          for (const attId of removedAttachmentIds) {
            await axios.delete(`/api/jobs/${id}/attachments/${attId}`)
          }
        }

        const payload = new FormData()
        Object.entries(rest).forEach(([key, val]) => {
          if (val !== null && val !== undefined) payload.append(key, val)
        })
        if (files && files.length) {
          files.forEach(f => payload.append('files', f))
        }

        const response = await axios.put(`/api/jobs/${id}`, payload)
        const updated = response.data
        this.entries = this.entries.map((entry) => (entry.id === id ? updated : entry))
        if (this.selected?.id === id) {
          this.selected = updated
        }
        this.loading = false
        return updated
      } catch (error) {
        this.error = error.response?.data?.error || error.message
        this.loading = false
        throw error
      }
    },

    async remove(id) {
      this.loading = true
      this.error = null
      try {
        await axios.delete(`/api/jobs/${id}`)
        this.entries = this.entries.filter((entry) => entry.id !== id)
        if (this.selected?.id === id) {
          this.selected = null
        }
        this.loading = false
      } catch (error) {
        this.error = error.response?.data?.error || error.message
        this.loading = false
        throw error
      }
    },

    async fetchStats() {
      this.loading = true
      this.error = null
      try {
        const response = await axios.get('/api/stats/')
        this.stats = response.data
        this.loading = false
      } catch (error) {
        this.error = error.response?.data?.error || error.message
        this.loading = false
        throw error
      }
    },

    selectEntry(entry) {
      this.selected = entry
    },

    clearSelected() {
      this.selected = null
    },

    clearError() {
      this.error = null
    },
  },
})
