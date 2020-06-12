import Vue from 'vue'
import axios from 'axios'
import router from '../../router'

export function login ({ commit }, payload) {
  axios({
    url: process.env.API + '/login',
    method: 'POST',
    data: {
      username: payload.username,
      password: payload.password
    }
  }).then(response => {
    Vue.prototype.$cookies.set('token', response.data.token)
    axios.defaults.headers.common.authorization = response.data.token
    router.push('/dashboard/overview')
  }).catch(error => {
    console.log(error)
    commit('SET_LOADING_STATUS', false)
  })
}

export function register ({ state }, payload) {
  axios({
    url: process.env.API + '/register',
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
