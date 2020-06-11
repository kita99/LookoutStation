<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="leftDrawerOpen = !leftDrawerOpen"
        />

        <q-toolbar-title>
          <img src="~assets/logo.svg" class="toolbar-logo vertical-middle">
        </q-toolbar-title>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
      content-class="bg-grey-1"
    >
      <q-list>
        <q-item-label
          header
          class="text-grey-8"
        >
          Menu
        </q-item-label>
        <MenuItem
          v-for="link in essentialLinks"
          :key="link.title"
          v-bind="link"
        />
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import MenuItem from 'components/MenuItem'

export default {
  name: 'MainLayout',

  components: {
    MenuItem
  },

  data () {
    return {
      leftDrawerOpen: false,
      essentialLinks: [
        {
          title: 'Overview',
          caption: 'Glance over important data',
          icon: 'dashboard',
          route: '/dashboard/overview'
        },
        {
          title: 'Assets',
          caption: 'All associated devices',
          icon: 'desktop_windows',
          route: '/dashboard/assets'
        }
      ]
    }
  }
}
</script>
