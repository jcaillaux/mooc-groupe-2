import { createRouter, createWebHistory } from 'vue-router'
import TrouverReponse from '../views/TrouverReponseView.vue' // Importation de la vue Home
import FilDeDiscussion from '../views/FilDeDiscussionView.vue'


const routes = [
  {
    path: '/',
    name: 'home',
    component: TrouverReponse
  },
  {
    path: '/fil-de-discussion',
    name: 'fil-de-discussion',
    component: FilDeDiscussion
  }
]

const router = createRouter({
  history: createWebHistory(), // Utilisation de l'historique pour les pages dans le navigateur
  routes
})

export default router
