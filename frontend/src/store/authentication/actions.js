import Vue from 'Vue'
import axios from 'axios'

export function login ({ state }, payload) {
  axios({
    url: state.url + '/login',
    method: 'POST',
    data: {
      username: payload.username,
      password: payload.password,
    }
  }).then(response => {
    if (response.data.status == '200') {
      state.isLoggedIn = true
      Vue.prototype.$cookies.set('token', response.data.token)
      axios.defaults.headers.common['Authorization'] = response.data.token
    }
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
      password: payload.password,
    }
  }).then(response => {
    state.isPreRegistered = true
  }).catch(error => {
    console.log(error)
  })
}
