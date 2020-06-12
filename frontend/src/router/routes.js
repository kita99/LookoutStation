const routes = [
  {
    path: '/dashboard',
    component: () => import('layouts/Dashboard.vue'),
    children: [
      {
        path: 'overview',
        component: () => import('pages/dashboard/Overview.vue'),
        meta: {
          requiresAuth: true
        }
      },
      {
        path: 'assets',
        component: () => import('pages/dashboard/assets/List.vue'),
        meta: {
          requiresAuth: true
        }
      },
      {
        path: 'assets/*',
        component: () => import('pages/dashboard/assets/View.vue'),
        meta: {
          requiresAuth: true
        }
      }
    ]
  },
  {
    path: '/login',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', name: 'Login', component: () => import('pages/Login.vue') }
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
