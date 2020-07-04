import axios from 'axios'

export function getOngoingScans ({ commit }) {
  axios({
    url: process.env.API + '/scans/ongoing',
    method: 'GET'
  }).then(response => {
    commit('SET_LOADING_STATUS', false)

    if (response.data) {
      commit('SET_ONGOING_SCANS', response.data.ongoing_scans)
    }
  })
}
