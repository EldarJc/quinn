<script setup>
import { storeToRefs } from 'pinia'
import { useUserStore } from '@/stores/user.js'
import { ref } from 'vue'
import DragDrop from "@/components/DragDrop.vue"

const userStore = useUserStore()
const { user, error } = storeToRefs(userStore)

const isModalOpen = ref(false)
const currentField = ref(null)
const newValue = ref('')
const fieldName = ref(null)
const imageFile = ref(null)
const isLoading = ref(false)

const openModal = (name, field) => {
  newValue.value = ''
  fieldName.value = name
  currentField.value = field
  isModalOpen.value = true
  imageFile.value = null
}

const closeModal = () => {
  isModalOpen.value = false
}

async function removeImage() {
  try {
    isLoading.value = true
    await userStore.removeUserImage()
  } catch (err) {
    console.error('Error removing image:', err)
  } finally {
    isLoading.value = false
  }
}

async function updateField() {
  try {
    isLoading.value = true

    if (fieldName.value === 'Image') {
      const formData = new FormData()
      formData.append('image', imageFile.value)
      await userStore.updateUserImage(formData)
    } else {
      const payload = {
        [currentField.value]: newValue.value
      }
      await userStore.updateCurrentUser(payload)
    }

    closeModal()
  } catch (err) {
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="w-[55%]">
    <Teleport to="body" v-if="isModalOpen">
      <div class="fixed inset-0 z-50 flex items-center justify-center">
        <div class="fixed inset-0 bg-black/50" @click="closeModal"></div>
        <div class="relative w-full max-w-md p-6 bg-white rounded-lg shadow-xl">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-semibold text-gray-900">Update {{ fieldName }}</h3>
            <button
                @click="closeModal"
                type="button"
                aria-label="Close modal"
                class="text-gray-500 hover:text-gray-700"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </button>
          </div>

          <div v-if="error?.[currentField]" class="mb-4 p-3 text-center">
            <p class="text-sm text-red-700">{{ error[currentField][0]}}</p>
          </div>

          <div class="space-y-4">
            <div v-if="fieldName === 'Image'">
              <DragDrop v-model="imageFile" />
            </div>
            <div v-else>
              <input
                  v-model.trim="newValue"
                  type="text"
                  class="w-full p-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white text-gray-900"
                  :disabled="isLoading"
              />
            </div>

            <div class="flex justify-end gap-3 pt-4">
              <button
                  @click="closeModal"
                  type="button"
                  :disabled="isLoading"
                  class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 border border-gray-300 rounded-md hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed transition"
              >
                Cancel
              </button>
              <button
                  @click="updateField"
                  type="button"
                  :disabled="isLoading"
                  class="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition"
              >
                {{ isLoading ? 'Saving...' : 'Save' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </Teleport>

    <div class="w-full max-w-4xl mx-auto">
      <h1 class="text-3xl font-bold text-gray-900 mb-8">General Settings</h1>

      <div class="bg-white rounded-lg shadow-sm border border-gray-200">
        <div class="border-b border-gray-200 px-6 py-4">
          <h2 class="text-xl font-semibold text-gray-900">Profile</h2>
          <p class="text-sm text-gray-600 mt-1">This information will be displayed publicly so be careful what you share.</p>
        </div>

        <div class="p-6 space-y-6">
          <div class="flex items-center justify-between border-b border-gray-200 pb-6">
            <div>
              <span class="text-sm font-semibold text-gray-900">Image</span>
              <p class="text-sm text-gray-500 mt-1">Upload an image</p>
            </div>
            <div class="flex gap-2">
              <button
                  @click="removeImage"
                  :disabled="!user?.image_url || isLoading"
                  type="button"
                  class="px-3 py-2 text-sm font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-100 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed transition"
              >
                Remove
              </button>
              <button
                  @click="openModal('Image', 'image_url')"
                  :disabled="isLoading"
                  type="button"
                  class="px-3 py-2 text-sm font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-100 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed transition"
              >
                Update
              </button>
            </div>
          </div>

          <div class="flex items-center justify-between border-b border-gray-200 pb-6">
            <div>
              <span class="text-sm font-semibold text-gray-900">Username</span>
              <p class="text-sm text-gray-500 mt-1">{{ user?.username }}</p>
            </div>
            <button
                @click="openModal('Username', 'username')"
                :disabled="isLoading"
                type="button"
                class="px-3 py-2 text-sm font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-100 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed transition"
            >
              Update
            </button>
          </div>

          <div class="flex items-center justify-between border-b border-gray-200 pb-6">
            <div>
              <span class="text-sm font-semibold text-gray-900">First Name</span>
              <p class="text-sm text-gray-500 mt-1">{{ user?.first_name }}</p>
            </div>
            <button
                @click="openModal('First Name', 'first_name')"
                :disabled="isLoading"
                type="button"
                class="px-3 py-2 text-sm font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-100 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed transition"
            >
              Update
            </button>
          </div>

          <div class="flex items-center justify-between border-b border-gray-200 pb-6">
            <div>
              <span class="text-sm font-semibold text-gray-900">Last Name</span>
              <p class="text-sm text-gray-500 mt-1">{{ user?.last_name }}</p>
            </div>
            <button
                @click="openModal('Last Name', 'last_name')"
                :disabled="isLoading"
                type="button"
                class="px-3 py-2 text-sm font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-100 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed transition"
            >
              Update
            </button>
          </div>

          <div class="flex items-center justify-between border-b border-gray-200 pb-6">
            <div>
              <span class="text-sm font-semibold text-gray-900">Email address</span>
              <p class="text-sm text-gray-500 mt-1">{{ user?.email }}</p>
            </div>
            <button
                @click="openModal('Email Address', 'email')"
                :disabled="isLoading"
                type="button"
                class="px-3 py-2 text-sm font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-100 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed transition"
            >
              Update
            </button>
          </div>

          <div class="flex items-center justify-between">
            <div>
              <span class="text-sm font-semibold text-gray-900">Bio</span>
              <p class="text-sm text-gray-500 mt-1">{{ user?.bio }}</p>
            </div>
            <button
                @click="openModal('Bio', 'bio')"
                :disabled="isLoading"
                type="button"
                class="px-3 py-2 text-sm font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-100 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed transition"
            >
              Update
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>