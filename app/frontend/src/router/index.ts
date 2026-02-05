// router.index.ts
import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SellerView from '../views/SellerView.vue'
import EachEstate from '../views/EachEstate.vue'
import BuyView from '../views/BuyView.vue'
import RentView from '../views/RentView.vue'
import AboutView from '../views/AboutView.vue'
import ContactView from '../views/ContactView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/buy',
      name: 'buy',
      component: BuyView,
    },
    {
      path: '/seller',
      name: 'seller',
      component: SellerView,
    },
    {
      path: '/estate/:id',
      name: 'each-estate',
      component: EachEstate,
    },
    {
      path: '/rent',
      name: 'rent',
      component: RentView,
    },
    {
      path: '/about',
      name: 'about',
      component: AboutView,
    },
    {
      path: '/contact',
      name: 'contact',
      component: ContactView,
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'NotFound',
      component: HomeView,
    }
  ],
})

export default router
