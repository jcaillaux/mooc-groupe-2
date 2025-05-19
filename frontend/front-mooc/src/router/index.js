import { createRouter, createWebHistory } from 'vue-router'
import TrouverReponse from '../views/TrouverReponseView.vue' // Importation de la vue Home
import FilDeDiscussion from '../views/FilDeDiscussionView.vue'
import LandingPageView from '../views/LandingPageView.vue'
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
    path: '/landing-page',
    name: 'landing-page',
    component: LandingPageView
  }
]

const router = createRouter({
  history: createWebHistory(), // Utilisation de l'historique pour les pages dans le navigateur
  routes
})

router.beforeEach((to, from, next) => {
  const store = useCounterStore()
  if (to.meta.requiresAuth && !store.connected) next('/landing-page') // redirige si pas connecté
  else next()
})

export default router
