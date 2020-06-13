import axios from 'axios'

export function getReport ({ commit, state }, id) {
  axios({
    url: process.env.API + '/reports/' + id,
    method: 'GET'
  }).then(response => {
    if (response.data) {
      commit('SET_REPORT', response.data.report)
    }
  })
}

export function getReports ({ commit, state }) {
  axios({
    url: process.env.API + '/reports',
    method: 'GET'
  }).then(response => {
    if (response.data) {
      commit('SET_REPORTS', response.data.reports)
    }
  })
}
