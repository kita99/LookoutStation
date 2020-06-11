import axios from 'axios'

export function getAssets ({ commit, state }, payload) {
  axios({
    url: state.url + '/assets',
    method: 'GET',
  }).then(response => {
    if (response.data.status == '200') {
      commit('')
    }
  }).catch(error => {
    console.log(error)
  })
}
