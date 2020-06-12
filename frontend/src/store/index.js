import Vue from 'vue'
import Vuex from 'vuex'

import authentication from './authentication'
import assets from './assets'

Vue.use(Vuex)

const store = new Vuex.Store({
  modules: {
    authentication,
    assets
  },

  // enable strict mode (adds overhead!)
  // for dev mode only
  strict: process.env.DEV
})

export default store
