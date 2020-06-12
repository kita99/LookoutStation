import axios from 'axios'

export function getAssets ({ commit, state }, payload) {
  axios({
    url: process.env.API + '/assets',
    method: 'GET'
  }).then(response => {
    if (response.data) {
      commit('SET_ASSETS', response.data.assets)
    }
  })
}
