<template>
  <div class="q-pa-md login-background fullscreen">
        <q-card class="login-card absolute-center">
          <q-card-section>
            <img src="~assets/logo-black.svg" class="login-logo">
          </q-card-section>

          <q-separator />

          <q-card-section class="login-card-inner">
            <q-form
              @submit="onSubmit"
              @reset="onReset"
              class="q-gutter-md"
            >
              <q-input
                filled
                v-model="name"
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
                v-model="age"
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
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex'

export default {
  data: () => ({
    username: '',
    password: '',
    accept: false
  }),

  watch: {
    isLoggedIn: {
      handler: 'redirect'
    }
  },

  methods: {
    ...mapActions('authentication', ['login']),

    submit: function () {
      this.login({ username: this.username, password: this.password })
    },

    redirect: function () {
      this.$router.push('dashboard/overview')
    }
  },

  computed: {
    ...mapState({
      isLoggedIn: state => state.authentication.isLoggedIn
    })
  }
}
</script>
