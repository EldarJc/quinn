<script setup>
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import {useUserStore} from '@/stores/user.js'

const route = useRoute()
const userStore = useUserStore()

const user = ref(null)
const error = ref(null)

watch(() => route.params.username, fetchUser, { immediate: true })

async function fetchUser(username) {
  error.value = user.value = null

  try {
    if (username === userStore.user?.username){
      user.value = userStore.user
    }

    else {
      user.value = await userStore.fetchUser(username)
    }
  } catch (err) {
    error.value = err
  }
}
</script>

<template>
  <div class="w-6xl font-sans">
    <div class="p-5 border-b-2 border-b-gray-200">
      <div class="container mx-auto">
        <div class="flex justify-between items-center py-4 px-16">
          <div class="flex items-center">
            <img class="w-24 h-24 rounded-full" :src="user.image_url" alt="channel_logo">
            <div class="ml-6">
              <div class="text-2xl font-normal flex flex-col justify-center">
                <p class="text-lg text-gray-800 truncate">{{user.first_name}} {{user.last_name}}</p>
                <div class="flex items-center">
                  <svg class="mr-1 fill-gray-400/80" xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24">
                    <path d="M12,15C12.81,15 13.5,14.7 14.11,14.11C14.7,13.5 15,12.81 15,12C15,11.19 14.7,10.5 14.11,9.89C13.5,9.3 12.81,9 12,9C11.19,9 10.5,9.3 9.89,9.89C9.3,10.5 9,11.19 9,12C9,12.81 9.3,13.5 9.89,14.11C10.5,14.7 11.19,15 12,15M12,2C14.75,2 17.1,3 19.05,4.95C21,6.9 22,9.25 22,12V13.45C22,14.45 21.65,15.3 21,16C20.3,16.67 19.5,17 18.5,17C17.3,17 16.31,16.5 15.56,15.5C14.56,16.5 13.38,17 12,17C10.63,17 9.45,16.5 8.46,15.54C7.5,14.55 7,13.38 7,12C7,10.63 7.5,9.45 8.46,8.46C9.45,7.5 10.63,7 12,7C13.38,7 14.55,7.5 15.54,8.46C16.5,9.45 17,10.63 17,12V13.45C17,13.86 17.16,14.22 17.46,14.53C17.76,14.84 18.11,15 18.5,15C18.92,15 19.27,14.84 19.57,14.53C19.87,14.22 20,13.86 20,13.45V12C20,9.81 19.23,7.93 17.65,6.35C16.07,4.77 14.19,4 12,4C9.81,4 7.93,4.77 6.35,6.35C4.77,7.93 4,9.81 4,12C4,14.19 4.77,16.07 6.35,17.65C7.93,19.23 9.81,20 12,20H17V22H12C9.25,22 6.9,21 4.95,19.05C3,17.1 2,14.75 2,12C2,9.25 3,6.9 4.95,4.95C6.9,3 9.25,2 12,2Z" />
                  </svg>

                  <span class="text-sm text-gray-500 truncate">{{user.username}}</span>
                </div>
                <div class="mt-4">
                  <p class="text-sm text-gray-600">{{user.bio}}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="px-16">
          <ul class="list-reset flex">
            <li class="text-center py-3 px-8 border-b-2 border-solid border-grey-dark"><a href="#" class="text-black">Overview</a></li>
            <li class="text-center py-3 px-8"><a href="#" class="hover:text-black">Events</a></li>
            <li class="text-center py-3 px-8"><a href="#" class="hover:text-black">Groups</a></li>
            <li class="text-center py-3 px-8"><i class="fa fa-search fa-lg text-grey-dark"></i></li>
          </ul>
        </div>
      </div>
    </div>
    <div class="container mx-auto flex">
      <div class="w-3/4 mx-16 py-6">
      </div>
      <div class="w-60 border-l-2 border-l-gray-200 p-5">
        <p class="text-grey-darker uppercase text-sm mb-6">ABOUT</p>
        <div class="flex flex-col items-center justify-center">
          <div class="flex h-20 w-35 flex-col items-center justify-center mt-3 rounded-md border border-dashed border-gray-200 transition-colors duration-100 ease-in-out hover:border-gray-400/80">
            <span class="font-bold text-gray-600">  {{ new Date(user.created_at).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' }) }} </span>
            <div class="mt-2 text-sm text-gray-400">Joined On</div>
          </div>
          <div class="flex h-20 w-35 flex-col items-center justify-center mt-3 rounded-md border border-dashed border-gray-200 transition-colors duration-100 ease-in-out hover:border-gray-400/80">
            <div class="flex flex-row items-center justify-center">
              <svg class="mr-2 fill-black" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
                <path d="M12 17.27L18.18 21 16.54 13.97 22 9.24 14.81 8.63 12 2 9.19 8.63 2 9.24 7.46 13.97 5.82 21z"/>
              </svg>
              <span class="font-bold text-gray-600">321</span>
            </div>
            <span class="mt-1 text-sm text-gray-400">Organizer score</span>
          </div>
          <div class="flex h-20 w-35 flex-col items-center justify-center mt-3 rounded-md border border-dashed border-gray-200 transition-colors duration-100 ease-in-out hover:border-gray-400/80">
            <div class="flex flex-row items-center justify-center">
              <svg class="mr-2 fill-gray-500/95" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
                <path d="M2.5 19.6L3.8 20.2V11.2L1.4 17C1 18.1 1.5 19.2 2.5 19.6M15.2 4.8L20.2 16.8L12.9 19.8L7.9 7.9V7.8L15.2 4.8M15.3 2.8C15 2.8 14.8 2.8 14.5 2.9L7.1 6C6.4 6.3 5.9 7 5.9 7.8C5.9 8 5.9 8.3 6 8.6L11 20.5C11.3 21.3 12 21.7 12.8 21.7C13.1 21.7 13.3 21.7 13.6 21.6L21 18.5C22 18.1 22.5 16.9 22.1 15.9L17.1 4C16.8 3.2 16 2.8 15.3 2.8M10.5 9.9C9.9 9.9 9.5 9.5 9.5 8.9S9.9 7.9 10.5 7.9C11.1 7.9 11.5 8.4 11.5 8.9S11.1 9.9 10.5 9.9M5.9 19.8C5.9 20.9 6.8 21.8 7.9 21.8H9.3L5.9 13.5V19.8Z" />
              </svg>

              <span class="font-bold text-gray-600"> 102 </span>
            </div>
            <div class="mt-2 text-sm text-gray-400">Events organized</div>
          </div>
          <div class="flex h-20 w-35 flex-col items-center justify-center mt-3 rounded-md border border-dashed border-gray-200 transition-colors duration-100 ease-in-out hover:border-gray-400/80">
            <div class="flex flex-row items-center justify-center">
              <svg class="mr-2 fill-gray-500/95" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
                <path d="M5.68,19.74C7.16,20.95 9,21.75 11,21.95V19.93C9.54,19.75 8.21,19.17 7.1,18.31M13,19.93V21.95C15,21.75 16.84,20.95 18.32,19.74L16.89,18.31C15.79,19.17 14.46,19.75 13,19.93M18.31,16.9L19.74,18.33C20.95,16.85 21.75,15 21.95,13H19.93C19.75,14.46 19.17,15.79 18.31,16.9M15,12A3,3 0 0,0 12,9A3,3 0 0,0 9,12A3,3 0 0,0 12,15A3,3 0 0,0 15,12M4.07,13H2.05C2.25,15 3.05,16.84 4.26,18.32L5.69,16.89C4.83,15.79 4.25,14.46 4.07,13M5.69,7.1L4.26,5.68C3.05,7.16 2.25,9 2.05,11H4.07C4.25,9.54 4.83,8.21 5.69,7.1M19.93,11H21.95C21.75,9 20.95,7.16 19.74,5.68L18.31,7.1C19.17,8.21 19.75,9.54 19.93,11M18.32,4.26C16.84,3.05 15,2.25 13,2.05V4.07C14.46,4.25 15.79,4.83 16.9,5.69M11,4.07V2.05C9,2.25 7.16,3.05 5.68,4.26L7.1,5.69C8.21,4.83 9.54,4.25 11,4.07Z" />
              </svg>
              <span class="font-bold text-gray-600"> 135 </span>
            </div>

            <div class="mt-2 text-sm text-gray-400">Events attended</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>