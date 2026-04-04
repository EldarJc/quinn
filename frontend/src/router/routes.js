import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'
import Login from '@/views/auth/Login.vue'
import Register from '@/views/auth/Register.vue';
import Logout from '@/views/auth/Logout.vue';
import Profile from '@/views/user/Profile.vue';
import ProfileSettings from '@/views/user/ProfileSettings.vue';
import {useUserStore} from '@/stores/user';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home,
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
      meta: { requiresGuest: true }
    },
    {
      path: '/register',
      name: 'register',
      component: Register,
      meta: { requiresGuest: true }
    },
    {
      path: '/logout',
      name: 'logout',
      component: Logout,
      meta: { requiresAuth: true },
    },
    {
      path: '/profile',
      name: 'profile',
      component: Profile,
    },
    {
      path: "/profile/settings",
      name: 'profile-settings',
      component: ProfileSettings,
      meta: { requiresAuth: true },
    },
  ],
})

router.beforeEach((to, from) => {
  const userStore = useUserStore();

  if (to.meta.requiresAuth && !userStore.isAuthenticated) {
    return { path: "/login" };
  }

  if (to.meta.requiresGuest && userStore.isAuthenticated) {
    return { path: "/" };
  }

  return true;
});

export default router
