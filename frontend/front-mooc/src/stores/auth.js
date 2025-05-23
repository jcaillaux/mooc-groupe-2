// stores/auth.js
import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: null,
    isAuthenticated: false
  }),

  actions: {
    async login(username, password) {
        console.log(username)
      try {
        const response = await axios.post('/api/login', {
          'username' : username,
          'password' : password
        },{
        headers: {
          'Content-Type': 'application/json'
        }
      })
        console.log('store', response.data)
        
        this.token = response.data.access_token
        this.isAuthenticated = true
        
        localStorage.setItem('token', this.token)
        axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`
        
        return true
      } catch (error) {
        console.error('Login failed:', error)
        return false
      }
    },

    logout() {
      this.token = null
      this.user = null
      this.isAuthenticated = false
      
      localStorage.removeItem('token')
      localStorage.removeItem('auth')
      delete axios.defaults.headers.common['Authorization']
    },

    initializeAuth() {
      if (this.token) {
        this.isAuthenticated = true
        axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`
      }
    }
  },
  persist: true // <-- C'est ça la magie !
})