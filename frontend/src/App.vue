<script setup>
import {RouterView } from 'vue-router'
import Header from './components/Header.vue'

</script>

<template>
  <Header/>
  <main class="grow flex items-center justify-center p-8">
    <RouterView/>
  </main>
</template>



