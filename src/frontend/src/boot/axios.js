import Vue from 'vue'
import axios from 'axios'
import router from '../router'

axios.interceptors.response.use(response => {
  return response
}, error => {
  if (error.response.status === 401) {
    router.push('/login')
  }
  return error
})

Vue.prototype.$axios = axios
