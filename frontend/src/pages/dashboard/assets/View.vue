<template>
  <q-splitter
    class="asset-container"
    v-model="splitterModel"
  >

    <template v-slot:before>
      <q-tabs
        v-model="tab"
        vertical
        class="text-black"
      >
        <q-tab name="general" icon="bar_chart" label="General" />
        <q-tab name="software" icon="apps" label="Software" />
        <q-tab name="security" icon="security" label="Security" />
      </q-tabs>
    </template>

    <template v-slot:after>
      <q-tab-panels
        v-model="tab"
        animated
        swipeable
        vertical
        transition-prev="jump-up"
        transition-next="jump-up"
      >
        <q-tab-panel name="general">
          <q-table
            :data="general"
            :columns="generalColumns"
            row-key="name"
            hide-header
            hide-bottom
            separator="vertical"
          >
            <template v-slot:body="props">
              <q-tr :props="props">
                <q-td key="name" :props="props" class="text-center" style="width: 20%">
                  {{ props.row.name }}
                </q-td>
                <q-td key="value" class="text-center" :props="props">
                  {{ props.row.value }}
                </q-td>
              </q-tr>
            </template>
          </q-table>
        </q-tab-panel>

        <q-tab-panel name="software">
          <q-table
            :data="asset.software"
            :columns="softwareColumns"
            row-key="name"
          />
        </q-tab-panel>

        <q-tab-panel name="security">
          <p>asdfffffffffffasdfasdfadsf</p>
        </q-tab-panel>
      </q-tab-panels>
    </template>

    </q-splitter>
</template>

<script>
import { mapActions, mapState } from 'vuex'

export default {
  data () {
    return {
      tab: 'general',
      splitterModel: 5,
      generalColumns: [
        {
          name: 'name',
          required: true,
          align: 'left',
          field: row => row.name
        },
        { name: 'value', align: 'left', field: 'value' }
      ],
      softwareColumns: [
        {
          name: 'name',
          required: true,
          align: 'left',
          field: row => row.name
        },
        { name: 'version', align: 'left', field: 'version' }
      ]
    }
  },

  methods: {
    ...mapActions('assets', ['getAsset'])
  },

  created () {
    this.getAsset(this.$router.currentRoute.params.pathMatch)
  },

  computed: {
    ...mapState({
      asset: state => state.assets.asset
    }),

    general: function () {
      return [
        {
          name: 'Hostname',
          value: this.asset.hostname
        },
        {
          name: 'Private IP',
          value: this.asset.private_ip
        },
        {
          name: 'Public IP',
          value: this.asset.public_ip
        },
        {
          name: 'Operating System',
          value: this.asset.operating_system
        }
      ]
    }
  }
}
</script>

<style scoped>
</style>
