<template>
  <div class="q-pa-md">
    <q-table
      title="Assets"
      :data="assets"
      :columns="columns"
      row-key="name"
    />
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex'

export default {
  data () {
    return {
      columns: [
        {
          name: 'hostname',
          required: true,
          label: 'Hostname',
          align: 'left',
          field: row => row.uuid,
          format: val => `${val}`,
          sortable: true
        },
        { name: 'private_ip', align: 'center', label: 'Private IP', field: 'private_ip', sortable: true },
        { name: 'public_ip', label: 'Public IP', field: 'public_ip' },
        { name: 'operating_system', label: 'Operating System', field: 'operating_system' },
        { name: 'software', label: 'Software (count)', field: 'software' },
        { name: 'last_update', label: 'Last Update', field: 'last_update' }
      ]
    }
  },

  methods: {
    ...mapActions('assets', ['getAssets'])
  },

  created () {
    this.getAssets()
  },

  mounted () {
    this.getAssets()
  },

  computed: {
    ...mapState({
      assets: state => state.assets.assets
    })
  }

}
</script>
