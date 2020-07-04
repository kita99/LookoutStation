<template>
    <q-card class="status-card-inner">
      <q-card-section class="status-card-section-top">
        <q-card class="status-icon-outer shadow-18">
          <q-icon :name="icon" class="status-icon text-black"/>
        </q-card>
        <p class="text-center text-weight-bolder text-h4">{{ nFormatter(value, 1) }}</p>
      </q-card-section>

      <q-separator/>

      <q-card-section class="status-card-section-bottom text-weight-thin">
        <p class="text-center text-weight-regular">{{ title }}</p>
      </q-card-section>
    </q-card>
</template>

<script>
export default {
  name: 'StatusCard',
  props: {
    title: {
      type: String,
      required: true
    },
    icon: {
      type: String,
      required: true
    },
    value: {
      type: String,
      required: true
    }
  },

  methods: {
    nFormatter: function (num, digits) {
      if (num > 999 && num < 1000000) {
        return (num / 1000).toFixed(0) + 'K'
      } else if (num > 1000000) {
        return (num / 1000000).toFixed(1) + 'M'
      } else if (num < 900) {
        return num
      }
    }
  }
}
</script>
