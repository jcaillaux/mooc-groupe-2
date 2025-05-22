import { createRouter, createWebHistory } from 'vue-router'
import TrouverReponse from '../views/TrouverReponseView.vue' // Importation de la vue Home
import FilDeDiscussion from '../views/FilDeDiscussionView.vue'
import LandingPageView from '../views/LandingPageView.vue'
import ThredsClustsViews from '../views/ThredsClustsViews.vue'
import SentimentView from '@/views/SentimentView.vue'
import { useCounterStore } from '../stores/data.js' // Importation du store Pinia

const routes = [
  {
    path: '/',
    name: 'home',
    component: TrouverReponse,
    meta: { requiresAuth: true }
  },
  {
    path: '/fil-de-discussion/:id',
    name: 'fil-de-discussion',
    component: FilDeDiscussion,
    meta: { requiresAuth: true }
  },
  {
    path: '/threds-clusts',
    name: 'threds-clusts',
    component: ThredsClustsViews,
    meta: { requiresAuth: true }
  },
  {
    path: '/landing-page',
    name: 'landing-page',
    component: LandingPageView
  },
  {
    path: '/sentiment',
    name: 'sentiment',
    component: SentimentView,
    meta: { requiresAuth: true }
  }
  
]

const router = createRouter({
  history: createWebHistory(), // Utilisation de l'historique pour les pages dans le navigateur
  routes
})

router.beforeEach((to, from, next) => {
  const store = useCounterStore()
  // Si l'utilisateur n'est pas connecté et qu'il va vers une page protégée
  if (to.meta.requiresAuth && !store.connected) {
    next('/landing-page')
  }
  // Si l'utilisateur est connecté et qu'il essaie d'aller sur la landing page
  else if (to.path === '/landing-page' && store.connected) {
    next('/')
  }
  else {
    next()
  }
})


export default router
