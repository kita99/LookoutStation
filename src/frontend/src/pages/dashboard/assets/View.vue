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
          <q-table
            title="Vulnerabilities"
            :data="asset.vulnerabilities"
            :columns="vulnerabilitiesColumns"
            row-key="name"
            :filter="filter"
            grid
            hide-header
          >
            <template v-slot:top-right>
              <q-input borderless dense debounce="300" v-model="filter" placeholder="Search">
                <template v-slot:append>
                  <q-icon name="search" />
                </template>
              </q-input>
            </template>

            <template v-slot:item="props">
              <div
                class="q-pa-xs col-xs-12 col-sm-6 col-md-4 col-lg-3 grid-style-transition"
                :style="props.selected ? 'transform: scale(0.95);' : ''"
              >
                <q-card bordered class="shadow-8">
                  <q-card-section>
                    <div class="text-h6">{{ props.cols[0].value }}</div>
                  </q-card-section>

                  <q-card-section class="q-pt-none">
                    {{ props.cols[1].value }}
                  </q-card-section>

                  <q-separator inset />

                  <q-card-section>
                    <template v-for="col in props.cols">

                      <template v-if="col.name == 'attack_complexity'">
                        <div class="row" :key="col.name">
                          <div class="col-7">
                            Attack Complexity
                          </div>
                          <div class="col-4 offset-1" style="text-align: center">
                            {{ col.value }}
                          </div>
                        </div>
                      </template>

                      <template v-if="col.name == 'availability_impact'">
                        <div class="row" :key="col.name">
                          <div class="col-7">
                            Availability Impact
                          </div>
                          <div class="col-4 offset-1" style="text-align: center">
                            {{ col.value }}
                          </div>
                        </div>
                      </template>

                      <template v-if="col.name == 'confidentiality_impact'">
                        <div class="row" :key="col.name">
                          <div class="col-7">
                            Confidentiality Impact
                          </div>
                          <div class="col-4 offset-1" style="text-align: center">
                            {{ col.value }}
                          </div>
                        </div>
                      </template>

                      <template v-if="col.name == 'privileges_required'">
                        <div class="row" :key="col.name">
                          <div class="col-7">
                            Privileges Required
                          </div>
                          <div class="col-4 offset-1" style="text-align: center">
                            {{ col.value }}
                          </div>
                        </div>
                      </template>
                    </template>
                  </q-card-section>

                  <q-separator inset />

                  <q-card-section>
                    <template v-for="col in props.cols">

                      <template v-if="col.name == 'base_score_v2'">
                        <template v-if="col.value">
                          <div class="row" :key="col.name">
                            <div class="col-5">
                              Score V2
                            </div>
                            <div class="col-7 vulnerability-card-progress">
                              <q-linear-progress
                                size="lg"
                                :value="parseFloat(col.value.base_score) / 10"
                                color="primary"
                              />
                            </div>
                          </div>
                        </template>
                      </template>

                      <template v-if="col.name == 'base_score_v3'">
                        <template v-if="col.value">
                          <div class="row" :key="col.name">
                            <div class="col-5">
                              Score V3
                            </div>
                            <div class="col-7 vulnerability-card-progress">
                              <q-linear-progress
                                size="lg"
                                :value="parseFloat(col.value.base_score) / 10"
                                color="primary"
                              />
                            </div>
                          </div>
                        </template>
                      </template>
                    </template>
                  </q-card-section>
                </q-card>
              </div>
            </template>

          </q-table>
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
      filter: '',
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
      ],
      vulnerabilitiesColumns: [
        {
          name: 'name',
          required: true,
          align: 'left',
          field: row => row.name,
          format: val => `${val}`,
          sortable: true
        },
        { name: 'description', field: 'description' },
        { name: 'assigner', field: 'assigner' },
        { name: 'publication', field: 'cve_publication_date' },
        { name: 'attack_complexity', field: row => row.baseMetricV2.attack_complexity },
        { name: 'confidentiality_impact', field: row => row.baseMetricV2.confidentiality_impact },
        { name: 'availability_impact', field: row => row.baseMetricV2.availability_impact },
        { name: 'base_score_v2', field: row => row.baseMetricV2 },
        { name: 'base_score_v3', field: row => row.baseMetricV3 }
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
