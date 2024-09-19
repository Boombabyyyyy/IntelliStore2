import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ShopView from '../views/ShopView.vue'
import AdminView from '../views/AdminView.vue'
import CartView from '../views/CartView.vue'
import LoginView from '../views/LoginView.vue'
import OrdersView from '../views/OrdersView.vue'
import ProfileView from '../views/ProfileView.vue'
import RegisterView from '../views/RegisterView.vue'
import ShopSingle from '../views/ShopSingle.vue'
import ShopByCat from '../views/ShopByCat.vue'
import ManagerView from '../views/ManagerView.vue'
import EditProduct from '../views/EditProduct.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/shopsingle',
      name: 'shopsingle',
      component: ShopSingle
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    },
    {
      path: '/shopbycategory',
      name: 'shopbycategory',
      component: ShopByCat
    },
    {
      path: '/shop',
      name: 'shop',
      component: ShopView
    },
    {
      path: '/admin',
      name: 'admin',
      component: AdminView
    },
    {
      path: '/manager',
      name: 'manager',
      component: ManagerView
    },
    {
      path: '/editproduct',
      name: 'editproduct',
      component: EditProduct
    },
    {
      path: '/cart',
      name: 'cart',
      component: CartView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/orders',
      name: 'orders',
      component: OrdersView
    },
    {
      path: '/profile',
      name: 'profile',
      component: ProfileView
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView
    },

  ]
})

export default router
