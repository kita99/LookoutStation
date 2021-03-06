<template>
  <div>
    <div class="row q-mt-md">
      <div class="col-3 offset-1 dashboard-status-grid">
        <StatusCard title="Assets" icon="computer" :value="assetCount" />
      </div>

      <div class="col-3 dashboard-status-grid">
        <StatusCard title="Vulnerabilities Found" icon="bug_report" :value="vulnerabilityCount" />
      </div>

      <div class="col-3 dashboard-status-grid">
        <StatusCard title="Open Ports" icon="meeting_room" :value="openPortCount" />
      </div>
    </div>

    <div class="row q-mt-md">
      <div class="col-3 offset-1 dashboard-status-grid">
        <StatusCard title="CVE Feeds" icon="integration_instructions" :value="feedCount" />
      </div>

      <div class="col-3 dashboard-status-grid">
        <StatusCard title="CVEs" icon="security" :value="cveCount" />
      </div>

      <div class="col-3 dashboard-status-grid">
        <StatusCard title="CPEs" icon="widgets" :value="cpeCount" />
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
                <q-linear-progress stripe size="25px" :value="parseFloat(props.row.progress) / 100" color="primary">
                  <div class="absolute-full flex flex-center">
                    <q-badge color="teal" text-color="white" :label="(props.row.progress).toFixed(1) + '%'" />
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

          <template v-slot:no-data>
            <div class="full-width row flex-center text-accent q-gutter-sm">
              <q-icon size="2em" name="done_all" />
              <span>
                Currently there are no scans running
              </span>
            </div>
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
    ...mapActions('scans', ['getOngoingScans']),
    ...mapActions('statistics', ['getOverviewStatistics'])
  },

  mounted () {
    window.setInterval(() => {
      this.getOngoingScans()
    }, 3000)

    this.getOverviewStatistics()
  },

  computed: {
    ...mapState({
      ongoingScans: state => state.scans.ongoingScans,
      assetCount: state => state.statistics.assetCount,
      vulnerabilityCount: state => state.statistics.vulnerabilityCount,
      openPortCount: state => state.statistics.openPortCount,
      feedCount: state => state.statistics.feedCount,
      cveCount: state => state.statistics.cveCount,
      cpeCount: state => state.statistics.cpeCount
    })
  }

}
</script>

<style scoped>
</style>
