<template>
  <div>
    <div class="row q-mt-md">
      <div class="col-3 offset-1 dashboard-status-grid">
        <StatusCard title="Assets" icon="computer" value="30" />
      </div>

      <div class="col-3 dashboard-status-grid">
        <StatusCard title="Vulnerabilities" icon="bug_report" value="5" />
      </div>

      <div class="col-3 dashboard-status-grid">
        <StatusCard title="Open Ports" icon="security" value="8" />
      </div>
    </div>

    <div class="row">
      <div class="col-10 offset-1">
        <q-table
          title="Ongoing Scans"
          :data="ongoingScans"
          :columns="columns"
          row-key="public_ip"
        >
          <template v-slot:body="props">
            <q-tr :props="props">
              <q-td key="public_ip" :props="props">
                {{ props.row.public_ip }}
              </q-td>
              <q-td key="flags" :props="props">
                {{ props.row.flags }}
              </q-td>
              <q-td key="ports" :props="props">
                {{ props.row.ports }}
              </q-td>
              <q-td key="progress" :props="props">
                <q-linear-progress stripe size="25px" :value="parseFloat(props.row.progress)" color="primary">
                  <div class="absolute-full flex flex-center">
                    <q-badge color="teal" text-color="white" :label="(props.row.progress * 100).toFixed(1) + '%'" />
                  </div>
                </q-linear-progress>
              </q-td>
              <q-td key="started_at" :props="props">
                {{ props.row.started_at }}
              </q-td>
              <q-td key="eta" :props="props">
                {{ props.row.eta }}
              </q-td>
            </q-tr>
          </template>
        </q-table>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex'
import StatusCard from 'components/StatusCard'

export default {
  components: {
    StatusCard
  },

  data () {
    return {
      columns: [
        {
          name: 'public_ip',
          required: true,
          label: 'IP Address',
          align: 'left',
          field: row => row.public_ip,
          format: val => `${val}`,
          sortable: true
        },
        { name: 'flags', label: 'Flags', field: 'flags' },
        { name: 'ports', label: 'Ports', field: 'ports' },
        { name: 'progress', align: 'center', label: 'Progress', field: 'progress', sortable: true },
        { name: 'started_at', label: 'Started At', field: 'started_at' },
        { name: 'eta', label: 'ETA', field: 'eta' }
      ]
    }
  },

  methods: {
    ...mapActions('scans', ['getOngoingScans'])
  },

  mounted () {
    this.getOngoingScans()
  },

  computed: {
    ...mapState({
      ongoingScans: state => state.scans.ongoingScans
    })
  }

}
</script>

<style scoped>
</style>
