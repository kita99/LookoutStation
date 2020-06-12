import axios from 'axios'

export function getAssets ({ commit, state }, payload) {
  axios({
    url: process.env.API + '/assets',
    method: 'GET'
  }).then(response => {
    commit('SET_ASSETS', response.data.assets)
  }).catch(error => {
    console.log(error)
  })
}
