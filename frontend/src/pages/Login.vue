<template>
  <div class="q-pa-md login-background fullscreen">
    <q-card class="login-card absolute-center">
      <q-card-section>
        <img src="~assets/logo-black.svg" class="login-logo">
      </q-card-section>

      <q-separator />

      <q-card-section class="login-card-inner">
        <q-form
          @submit="submit"
          @keydown.enter.prevent="submit"
          class="q-gutter-md"
        >
          <q-input
            filled
            v-model="username"
            label="Username"
            lazy-rules
            :rules="[ val => val && val.length > 0 || 'Please type something']"
          >
            <template v-slot:prepend>
              <q-icon name="account_circle" />
            </template>
          </q-input>

          <q-input
            filled
            type="password"
            v-model="password"
            label="Password"
            lazy-rules
            :rules="[
              val => val !== null && val !== '' || 'Please type your password',
              val => val > 5 && val < 100 || 'Invalid password'
            ]"
          >
            <template v-slot:prepend>
              <q-icon name="vpn_key" />
            </template>
          </q-input>
        </q-form>
      </q-card-section>

      <q-separator />

      <q-card-actions align="right">
        <q-btn label="Submit" type="submit" color="primary"/>
      </q-card-actions>
    </q-card>

    <q-overlay v-model="loading" no-scroll z-index="5000">
      <template v-slot:body>
        <div class="fullscreen row justify-center items-center">
          <q-spinner v-if="loading" color="black" size="3em"></q-spinner>
        </div>
      </template>
    </q-overlay>
  </div>
</template>

<script>
import { mapActions, mapMutations, mapState } from 'vuex'

export default {
  data: () => ({
    username: '',
    password: ''
  }),

  watch: {
    loading: {
      handler: 'clearPassword'
    }
  },

  methods: {
    ...mapActions('authentication', ['login']),
    ...mapMutations('authentication', ['SET_LOADING_STATUS']),

    submit: function () {
      this.SET_LOADING_STATUS(true)
      this.login({ username: this.username, password: this.password })
    },

    clearPassword: function (loading) {
      if (loading === false) {
        this.password = ''
      }
    }
  },

  computed: {
    ...mapState({
      loading: state => state.authentication.loading
    })
  }
}
</script>
