import Vue from 'vue'
import axios from 'axios'

export function login ({ state }, payload) {
  axios({
    url: state.url + '/login',
    method: 'POST',
    data: {
      username: payload.username,
      password: payload.password
    }
  }).then(response => {
    state.isLoggedIn = true
    Vue.prototype.$cookies.set('token', response.data.token)
    axios.defaults.headers.common.authorization = response.data.token
  }).catch(error => {
    console.log(error)
  })
}

export function register ({ state }, payload) {
  axios({
    url: state.url + '/register',
    method: 'POST',
    data: {
      username: payload.username,
      password: payload.password
    }
  }).then(response => {
    state.isPreRegistered = true
  }).catch(error => {
    console.log(error)
  })
}
