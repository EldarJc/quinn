<script setup>
import {RouterLink} from 'vue-router';

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  errorMessage: {
    type: String,
    default: 'An error occurred.'
  }
})

</script>

<template>
  <Transition name="slide-fade">
    <div
        v-if="show"
        class="fixed top-25 left-1/2 transform -translate-x-1/2 z-50 w-md bg-gray-100 shadow-xl rounded-lg p-6 flex flex-col items-center text-center"
    >
      <div class="flex items-center justify-center gap-2">
        <svg class="w-7 h-7 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
        </svg>
        <h3 class="text-xl font-semibold text-gray-800 mb-1">Oops! An error occurred</h3>
      </div>
      <p class="text-lg text-gray-600 mb-4">{{ errorMessage }}</p>
      <div class="flex space-x-4">
        <RouterLink
            :to="{ name: 'home' }"
            class="px-5 py-2 bg-red-200 text-white text-sm font-medium rounded-md hover:bg-red-700 transition-colors duration-300 shadow-sm hover:shadow"
        >
          Go Home
        </RouterLink>
      </div>
    </div>
  </Transition>
</template>