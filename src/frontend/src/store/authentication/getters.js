import Vue from 'vue'
import axios from 'axios'

export function isLoggedIn () {
  var token = Vue.prototype.$cookies.get('token')

  if (token !== 'undefined') {
    axios.defaults.headers.common.authorization = token
    return true
  }

  return false
}
