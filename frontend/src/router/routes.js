import { createRouter, createWebHistory, START_LOCATION } from 'vue-router'
import Home from '@/views/Home.vue'
import Login from '@/views/auth/Login.vue'
import Register from '@/views/auth/Register.vue';
import Logout from '@/views/auth/Logout.vue';
import Profile from '@/views/user/Profile.vue';
import ProfileSettings from '@/views/user/ProfileSettings.vue';
import {useUserStore} from '@/stores/user';
import CreateEvent from "@/views/event/CreateEvent.vue";
import EventDetails from "@/views/event/EventDetails.vue";
import Events from "@/views/event/Events.vue";

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
      meta: { guest: true }
    },
    {
      path: '/register',
      name: 'register',
      component: Register,
      meta: { guest: true }
    },
    {
      path: '/logout',
      name: 'logout',
      component: Logout,
      meta: { auth: true },
    },
    {
      path: '/u/:username',
      name: 'profile',
      component: Profile,
    },
    {
      path: "/profile/settings",
      name: 'profile-settings',
      component: ProfileSettings,
      meta: { auth: true },
    },
    {
      path: '/events',
      name: 'event-list',
      component: Events,
    },
    {
      path: '/events/create',
      name: 'create-event',
      component: CreateEvent,
      meta: { auth: true },
    },
    {
      path: '/events/:id/:slug',
      name: 'event-details',
      component: EventDetails,
    }
  ],
})

router.beforeEach(async (to, from) => {
  const userStore = useUserStore();

  if (from === START_LOCATION) {
    const accessToken = localStorage.getItem('accessToken');
    if (accessToken) {
      await userStore.fetchCurrentUser();
    }
  }

  if (to.meta.auth && !userStore.isAuthenticated) {
    return { name: 'login' }
  }

  if (to.meta.guest && userStore.isAuthenticated) {
    return { name: 'home' };
  }

  return true;
});

export default router
