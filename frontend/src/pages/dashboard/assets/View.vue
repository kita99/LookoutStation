<template>
  <p> View single asset</p>
</template>

<script>
import { mapActions, mapState } from 'vuex'
export default {
  created () {
    this.getAsset(this.$router.currentRoute.params.pathMatch)
  },

  method: {
    ...mapActions('assets', ['getAsset'])
  },

  computed: {
    ...mapState({
      asset: state => state.assets.asset
    })
  }
}
</script>

<style scoped>
</style>
