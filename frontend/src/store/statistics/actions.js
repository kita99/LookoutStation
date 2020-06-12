import axios from 'axios'

export function getOverviewStatistics ({ commit }) {
  axios({
    url: process.env.API + '/statistics/overview',
    method: 'GET'
  }).then(response => {
    commit('SET_LOADING_STATUS', false)

    if (response.data) {
      commit('SET_OVERVIEW_STATISTICS', response.data)
    }
  })
}
