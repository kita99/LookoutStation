import axios from 'axios'

export function getAsset ({ commit, state }, uuid) {
  axios({
    url: process.env.API + '/assets/' + uuid,
    method: 'GET'
  }).then(response => {
    if (response.data) {
      commit('SET_ASSET', response.data.asset)
    }
  })
}

export function getAssets ({ commit, state }) {
  axios({
    url: process.env.API + '/assets',
    method: 'GET'
  }).then(response => {
    if (response.data) {
      commit('SET_ASSETS', response.data.assets)
    }
  })
}
