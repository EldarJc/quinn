<script setup>
import {RouterLink} from 'vue-router';
import { ref, onMounted, onBeforeUnmount } from 'vue'
import {useUserStore} from '@/stores/user.js';
import defaultAvatar from '@/assets/user-logo.svg'

const userStore = useUserStore()

const isOpen = ref(false)

const toggleDropdown = () => {
  isOpen.value = !isOpen.value
}

const handleClickOutside = (e) => {
  if (!e.target.closest('.dropdown')) {
    isOpen.value = false
  }
}

onMounted(() => {
  window.addEventListener('click', handleClickOutside)
})

onBeforeUnmount(() => {
  window.removeEventListener('click', handleClickOutside)
})
</script>


<template>
  <header class="bg-[#2c3e50] w-full sticky top-0 z-50">
    <nav class="mx-auto flex max-w-7xl items-center justify-between h-16 px-8">
      <div class="flex lg:flex-1">
        <RouterLink to="/" class="flex items-center group">
            <img
                src="@/assets/logo.png"
                alt="Quinn Logo"
                class="h-8 w-auto"
            />
        </RouterLink>
      </div>
      <div class="flex gap-x-3">
        <RouterLink to="/" class="text-white font-semibold hover:text-[#608a89] px-4 py-2 flex items-center rounded-xl hover:bg-blue-50 transition-colors duration-200">
          <svg class="mr-3" fill="currentColor" height="20" viewBox="0 0 20 20" width="20" xmlns="http://www.w3.org/2000/svg">
            <svg class="mr-3" fill="currentColor" height="20" viewBox="0 0 20 20" width="20" xmlns="http://www.w3.org/2000/svg"><path d="M17.875 8.525a1.584 1.584 0 00-.35-.52L11.13 1.653a1.602 1.602 0 00-2.264 0L2.47 8.005a1.604 1.604 0 00-.473 1.135v6.374a3.3 3.3 0 003.3 3.3h3.7V12h2v6.814h3.7a3.3 3.3 0 003.3-3.3V9.14c0-.211-.042-.42-.123-.615h.001z"></path></svg>
          </svg>
          Home
        </RouterLink>
        <RouterLink to="/events" class="text-white font-semibold hover:text-[#608a89] px-4 py-2 flex items-center rounded-lg hover:bg-blue-50 transition-colors duration-200">
          <svg class="mr-3" fill="currentColor" height="20" viewBox="0 0 20 20" width="20" xmlns="http://www.w3.org/2000/svg">
            <path d="M15 12.05c1.08 0 1.95.87 1.95 1.95s-.87 1.95-1.95 1.95-1.95-.87-1.95-1.95.87-1.95 1.95-1.95zm0-1.8c-2.07 0-3.75 1.68-3.75 3.75 0 2.07 1.68 3.75 3.75 3.75 2.07 0 3.75-1.68 3.75-3.75 0-2.07-1.68-3.75-3.75-3.75zM5 12.05c1.08 0 1.95.87 1.95 1.95S6.08 15.95 5 15.95 3.05 15.08 3.05 14s.87-1.95 1.95-1.95zm0-1.8c-2.07 0-3.75 1.68-3.75 3.75 0 2.07 1.68 3.75 3.75 3.75 2.07 0 3.75-1.68 3.75-3.75 0-2.07-1.68-3.75-3.75-3.75zM10 4.05c1.08 0 1.95.87 1.95 1.95S11.08 7.95 10 7.95 8.05 7.08 8.05 6 8.92 4.05 10 4.05zm0-1.8C7.93 2.25 6.25 3.93 6.25 6c0 2.07 1.68 3.75 3.75 3.75 2.07 0 3.75-1.68 3.75-3.75 0-2.07-1.68-3.75-3.75-3.75z"></path>
          </svg>
          Explore Events
        </RouterLink>
        <RouterLink to="/communities" class="text-white font-semibold hover:text-[#608a89] px-4 py-2 flex items-center rounded-lg hover:bg-blue-50 transition-colors duration-200">
          <svg class="mr-3" fill="currentColor"  height="20" viewBox="0 0 20 20" width="20" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm6 2c-1.33 0-4 0.67-4 2v2h8v-2c0-1.33-2.67-2-4-2zm-12 0c-1.33 0-4 0.67-4 2v2h8v-2c0-1.33-2.67-2-4-2z"/>
          </svg>
          Communities
        </RouterLink>
        <RouterLink to="/" class="text-white font-semibold hover:text-[#608a89] px-4 py-2 flex items-center rounded-lg hover:bg-blue-50 transition-colors duration-200">
          <svg class="mr-3" fill="currentColor" height="20" viewBox="0 0 20 20" width="20" xmlns="http://www.w3.org/2000/svg">
            <path d="M18.278 2.632a2.265 2.265 0 00-1.698-.627c-2.95.165-4.67.827-6.58 1.987-1.91-1.16-3.63-1.822-6.581-1.987a2.273 2.273 0 00-1.697.627A2.327 2.327 0 001 4.312v9.428c0 1.23.966 2.241 2.198 2.302 2.724.136 4.175.715 5.761 1.67a2.019 2.019 0 002.082 0c1.586-.955 3.037-1.534 5.761-1.67a2.308 2.308 0 002.199-2.302V4.312c0-.632-.264-1.244-.723-1.68zM3.288 14.238a.507.507 0 01-.488-.498V4.312c0-.189.1-.312.16-.368a.487.487 0 01.333-.136h.027c2.625.147 4.043.692 5.78 1.752v10.158c-1.535-.819-3.177-1.348-5.813-1.48h.001zM17.2 13.74a.505.505 0 01-.488.498c-2.635.132-4.277.661-5.812 1.48V5.56c1.736-1.06 3.155-1.606 5.779-1.752a.47.47 0 01.361.136c.06.056.16.18.16.368v9.427zM12 6.95c1.131-.469 2.385-.765 4-.9v1.794c-1.678.152-2.842.5-4 1.081V6.95zm0 4.064c1.131-.469 2.385-.765 4-.9v1.794c-1.678.152-2.842.5-4 1.081v-1.975z"></path>
          </svg>
          Blog
        </RouterLink>
      </div>
      <div class="flex flex-1 justify-end">
        <div v-if="userStore.user" class="flex items-center space-x-3">
          <RouterLink to="/" class="text-white relative group p-2 hover:text-[#608a89] rounded-full hover:bg-gray-100 transition-colors duration-200">
            <svg fill="currentColor" height="24" viewBox="0 0 20 20" width="20" xmlns="http://www.w3.org/2000/svg">
              <path d="M14.7 2H5.3C3.481 2 2 3.48 2 5.3v9.4C2 16.519 3.48 18 5.3 18h9.4c1.819 0 3.3-1.48 3.3-3.3V5.3C18 3.481 16.52 2 14.7 2zm1.499 12.7a1.5 1.5 0 01-1.499 1.499H5.3A1.5 1.5 0 013.801 14.7V5.3A1.5 1.5 0 015.3 3.801h9.4A1.5 1.5 0 0116.199 5.3v9.4zM14 10.9h-3.1V14H9.1v-3.1H6V9.1h3.1V6h1.8v3.1H14v1.8z"></path>
            </svg>

            <span class="absolute left-1/2 mt-2 -translate-x-1/2 bg-gray-800 text-white text-xs rounded px-2 py-1 opacity-0 group-hover:opacity-100 pointer-events-none whitespace-nowrap transition-opacity duration-200">
              Create Post
            </span>
          </RouterLink>

          <div class="h-6 w-px bg-white"></div>

          <div class="dropdown relative">
            <button
                @click.stop="toggleDropdown"
                class="flex items-center space-x-2 focus:outline-none group ml-2"
            >
              <div class="h-9 w-9 rounded-full overflow-hidden ring-2 ring-white">
                <img
                    :src="userStore.user.image_url || defaultAvatar"
                    class="h-full w-full"
                    alt="Avatar"
                />
              </div>
            </button>

            <div
                v-show="isOpen"
                class="absolute right-0 mt-4 w-64 bg-white rounded-lg shadow-xl py-1 border border-gray-100"
            >
              <RouterLink :to="{ name: 'profile', params: { username: userStore.user.username } }" class="px-4 py-3 border-b border-gray-100 flex items-center">
                <div class="bg-gray-700 h-10 w-10 rounded-full overflow-hidden mr-3 ring-1 ring-[#608a89]">
                  <img
                      :src="userStore.user.image_url || defaultAvatar"
                      class="h-full w-full"
                      alt="Avatar"
                  />
                </div>
                <div>
                  <p class="font-medium text-gray-900">View Profile</p>
                  <p class="text-sm text-gray-500">{{userStore.user.username}}</p>
                </div>
              </RouterLink>

              <RouterLink :to="{ name: 'profile-settings' }" class="flex items-center px-4 py-2.5 text-gray-700 hover:bg-blue-50 hover:text-[#608a89] transition-colors">
                <svg class="mr-3" fill="currentColor" height="20"  viewBox="0 0 20 20" width="20" xmlns="http://www.w3.org/2000/svg">
                  <path d="M11.145 18.995h-2.29a1.56 1.56 0 01-1.501-1.134l-.051-.18a2.161 2.161 0 00-2.604-1.504l-.185.046a1.561 1.561 0 01-1.731-.734l-1.146-1.985a1.561 1.561 0 01.229-1.864l.132-.137a2.163 2.163 0 000-3.007l-.13-.135a1.561 1.561 0 01-.23-1.866L2.783 4.51a1.56 1.56 0 011.73-.734l.186.046a2.161 2.161 0 002.603-1.504l.05-.18a1.562 1.562 0 011.503-1.134h2.29c.697 0 1.31.463 1.5 1.133l.053.183a2.157 2.157 0 002.599 1.502l.189-.047a1.561 1.561 0 011.73.734l1.147 1.985a1.561 1.561 0 01-.23 1.864l-.133.14a2.162 2.162 0 000 3.004l.132.137c.485.5.578 1.262.23 1.866l-1.145 1.984a1.56 1.56 0 01-1.731.734l-.187-.047a2.16 2.16 0 00-2.601 1.503l-.052.182a1.562 1.562 0 01-1.502 1.134zm-2.11-1.8l1.933-.01a3.947 3.947 0 014.77-2.754l.01.002.967-1.672-.008-.007a3.943 3.943 0 010-5.508l.007-.007-.966-1.672-.01.002a3.945 3.945 0 01-4.771-2.754l-.003-.01-1.933.009A3.946 3.946 0 014.26 5.569l-.01-.002-.966 1.672.008.007a3.943 3.943 0 010 5.508l-.007.007.966 1.672.01-.002a3.947 3.947 0 014.77 2.754l.004.01zM10 13c-1.654 0-3-1.346-3-3s1.346-3 3-3 3 1.346 3 3-1.346 3-3 3zm0-4.2c-.661 0-1.2.539-1.2 1.2 0 .66.539 1.2 1.2 1.2.66 0 1.199-.54 1.199-1.2 0-.661-.538-1.2-1.2-1.2z"></path>
                </svg>
                Account Settings
              </RouterLink>

              <div class="border-t border-gray-100 my-1"></div>

              <RouterLink :to="{ name: 'logout' }" class="flex items-center px-4 py-2.5 text-gray-700 hover:bg-blue-50 hover:text-[#608a89] transition-colors">
                <svg class="mr-3" fill="currentColor" height="20" viewBox="0 0 20 20" width="20" xmlns="http://www.w3.org/2000/svg">
                  <path d="M13.701 1H6.298a3.299 3.299 0 00-3.299 3.299v8.402A3.299 3.299 0 006.298 16h.701v.858a2.26 2.26 0 002.255 2.259c.293 0 .594-.058.889-.184l5.487-2.347a2.257 2.257 0 001.369-2.075V4.299A3.298 3.298 0 0013.701 1zM7 6.767V14.2h-.701A1.5 1.5 0 014.8 12.701V4.299A1.5 1.5 0 016.299 2.8h6.494L8.37 4.692A2.257 2.257 0 007 6.767zm8.2 7.744a.457.457 0 01-.277.42l-5.487 2.347a.461.461 0 01-.181.039.46.46 0 01-.455-.459V6.767c0-.183.109-.348.277-.42L14.564 4a.461.461 0 01.181-.039.46.46 0 01.455.459v10.091zM10.3 9.7h1.8v2.585h-1.8V9.7z"></path>
                </svg>
                Log Out
              </RouterLink>
            </div>
          </div>
        </div>
        <div v-else class="flex items-center justify-center gap-x-3">
          <RouterLink :to="{ name: 'login' }" class="text-white font-semibold px-4 py-2 transition-all duration-200 hover:text-opacity-50 hover:bg-[#608a89] rounded-xl"> Log In </RouterLink>

          <RouterLink  :to="{ name: 'register' }"  class="text-white font-semibold px-4 py-2 transition-all duration-200 bg-transparent border-2 border-[#608a89] hover:bg-[#608a89] hover:text-white rounded-xl">
            Join community
          </RouterLink>
        </div>
      </div>
    </nav>
  </header>
</template>