// router.index.ts
import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/Home.vue'
import AboutView from '../views/About.vue'
import ContactView from '../views/Contact.vue'
import BuyView from '../views/properties/Buy.vue'
import RentView from '../views/properties/Rent.vue'
import PropertyDetailView from '../views/properties/Detail.vue'
import LoginView from '../views/user/Login.vue'
import RegisterView from '../views/user/Register.vue'
import ProfileView from '../views/user/Profile.vue'
import FavoritesView from '../views/user/Favorites.vue'
import SellerView from '../views/seller/Seller.vue'
import AddPropertyView from '../views/seller/AddProp.vue'
import EditPropertyView from '../views/seller/EditProp.vue'
import AdminDashboardView from '../views/admin/AdminDashboard.vue'
import NotFoundView from '../views/NotFound.vue'
import MyListingsView from '../views/seller/MyList.vue'
import { useAuthStore } from '../stores/auth.js'
// router/index.js
const routes = [
  { path: '/', name: 'home', component: HomeView },
  { path: '/about', name: 'about', component: AboutView },
  { path: '/contact', name: 'contact', component: ContactView },

  // Properties
  { path: '/buy', name: 'buy', component: BuyView },
  { path: '/rent', name: 'rent', component: RentView },
  { path: '/property/:id', name: 'property-detail', component: PropertyDetailView },

  // User
  { path: '/login', name: 'login', component: LoginView },
  { path: '/register', name: 'register', component: RegisterView },
  { path: '/profile', name: 'profile', component: ProfileView, meta: { requiresAuth: true } },
  { path: '/favorites', name: 'favorites', component: FavoritesView, meta: { requiresAuth: true } },

  // Seller
  { path: '/seller', name: 'seller-dashboard', component: SellerView, meta: { requiresAuth: true, role: 'seller' } },
  { path: '/seller/add', name: 'add-property', component: AddPropertyView, meta: { requiresAuth: true, role: 'seller' } },
  { path: '/seller/my-listings', name: 'my-listings', component: MyListingsView, meta: { requiresAuth: true, role: 'seller' } },
  { path: '/seller/edit/:id', name: 'edit-property', component: EditPropertyView, meta: { requiresAuth: true, role: 'seller' } },

  // Admin
  { path: '/admin', name: 'admin-dashboard', component: AdminDashboardView, meta: { requiresAuth: true, role: 'admin' } },

  // 404
  { path: '/:pathMatch(.*)*', name: 'not-found', component: NotFoundView }
]
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: routes
})

router.beforeEach((to) => {
  const auth = useAuthStore()

  if (to.meta.requiresAuth && !auth.isLoggedIn) {
    return { path: '/login', query: { redirect: to.fullPath } }
  }
})

export default router
