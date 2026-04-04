<script setup>
import { onMounted } from 'vue'
import {RouterView } from 'vue-router'
import Header from './components/Header.vue'
import { useUserStore } from '@/stores/user'


const userStore = useUserStore()

onMounted(async () => {
  await userStore.fetchCurrentUser()
})
</script>

<template>
  <Header/>
  <main class="grow flex items-center justify-center p-8">
    <RouterView/>
  </main>
</template>



