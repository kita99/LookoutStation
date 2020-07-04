<template>
  <div class="row q-pa-md">
    <div class="col-10 offset-1">
      <q-table
        title="Assets"
        :data="assets"
        :columns="columns"
        row-key="name"
        @row-click="viewAsset"
      >
        <template v-slot:no-data>
          <div class="full-width row flex-center text-accent q-gutter-sm">
            <q-icon size="2em" name="sentiment_dissatisfied" />
            <span>
              No assets found... time to run some scripts!
            </span>
          </div>
        </template>
      </q-table>
    </div>
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
        { name: 'private_ip', label: 'Private IP', field: 'private_ip', sortable: true },
        { name: 'public_ip', label: 'Public IP', field: 'public_ip' },
        { name: 'operating_system', label: 'OS', field: 'operating_system' },
        { name: 'cves', label: 'CVEs', field: 'cve_count' },
        { name: 'open_ports', label: 'Open Ports', field: 'open_port_count' }
      ]
    }
  },

  methods: {
    ...mapActions('assets', ['getAssets']),

    viewAsset: function (e, row) {
      this.$router.push('/dashboard/assets/' + row.uuid)
    }
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
