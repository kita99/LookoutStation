import Vue from 'vue'
import Vuex from 'vuex'

import authentication from './authentication'
import statistics from './statistics'
import reports from './reports'
import assets from './assets'
import scans from './scans'

Vue.use(Vuex)

const store = new Vuex.Store({
  modules: {
    authentication,
    statistics,
    reports,
    scans,
    assets
  },

  // enable strict mode (adds overhead!)
  // for dev mode only
  strict: process.env.DEV
})

export default store
