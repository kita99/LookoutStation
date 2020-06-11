const routes = [
  {
    path: '/dashboard',
    component: () => import('layouts/Dashboard.vue'),
    children: [
      { path: 'overview', component: () => import('pages/dashboard/Overview.vue') },
      { path: 'assets', component: () => import('pages/dashboard/Assets.vue') }
    ]
  },
  {
    path: '/login',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/Login.vue') }
    ]
  },
  {
    path: '/register',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/Register.vue') }
    ]
  }
]

// Always leave this as last one
if (process.env.MODE !== 'ssr') {
  routes.push({
    path: '*',
    component: () => import('pages/Error404.vue')
  })
}

export default routes
