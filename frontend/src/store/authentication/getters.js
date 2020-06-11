import Vue from 'Vue'
import axios from 'axios'

export function isLoggedIn () {
  var token = Vue.prototype.$cookies.get('token')

  if (token !== null) {
    axios.defaults.headers.common['Authorization'] = token
    return true
  }

  return false
}
