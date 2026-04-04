<script setup>
import { ref, onMounted } from 'vue'
import router from "@/router/routes"
import {useUserStore} from '@/stores/user';

const userStore = useUserStore()

const countdownSeconds = ref(2)

onMounted(async () => {
  try {
    await userStore.logout()
  } catch (error) {
  }

  startCountdown()
})

const startCountdown = () => {
  const interval = setInterval(() => {
    countdownSeconds.value--;

    if (countdownSeconds.value <= 0) {
      clearInterval(interval);
      router.push('/');
    }
  }, 1000);
};
</script>

<template>
  <div class="flex items-center justify-center">
    <div class="w-120 py-8">

      <div class="flex items-center w-full gap-3 mb-9">
        <div class="flex-1 h-px bg-gray-300"></div>

        <div>
          <svg class="w-22 h-22 text-green-600" fill="currentColor" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400">
            <path d="M199.996,0C89.713,0,0,89.72,0,200s89.713,200,199.996,200S400,310.28,400,200S310.279,0,199.996,0z M199.996,373.77 C104.18,373.77,26.23,295.816,26.23,200c0-95.817,77.949-173.769,173.766-173.769c95.817,0,173.771,77.953,173.771,173.769 C373.768,295.816,295.812,373.77,199.996,373.77z"/>
            <path d="M272.406,134.526L169.275,237.652l-41.689-41.68c-5.123-5.117-13.422-5.12-18.545,0.003 c-5.125,5.125-5.125,13.425,0,18.548l50.963,50.955c2.561,2.558,5.916,3.838,9.271,3.838s6.719-1.28,9.279-3.842 c0.008-0.011,0.014-0.022,0.027-0.035L290.95,153.071c5.125-5.12,5.125-13.426,0-18.546 C285.828,129.402,277.523,129.402,272.406,134.526z"/>
          </svg>
        </div>

        <div class="flex-1 h-px bg-gray-300"></div>
      </div>

      <div class="text-center">
        <h3 class="text-xl font-semibold text-gray-700">You have been logged out</h3>
        <p class="text-sm mt-2 text-gray-400">
          Thank you for using our application.
        </p>
      </div>
    </div>
  </div>
</template>