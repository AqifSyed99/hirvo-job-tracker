import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    component: () => import('../layouts/AuthenticatedLayout.vue'),
    children: [
      { path: 'dashboard', component: () => import('../views/DashboardView.vue') },
      { path: 'jobs', component: () => import('../views/JobListView.vue') },
      { path: 'profile', component: () => import('../views/ProfileView.vue') },
      { path: '', redirect: '/dashboard' },
    ],
  },
  {
    path: '/login',
    component: () => import('../views/LoginView.vue'),
    meta: { public: true },
  },
  {
    path: '/register',
    component: () => import('../views/RegisterView.vue'),
    meta: { public: true },
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/dashboard',
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  if (!to.meta.public) {
    const token = localStorage.getItem('token')
    if (!token) {
      return next('/login')
    }
  }
  next()
})

export default router
