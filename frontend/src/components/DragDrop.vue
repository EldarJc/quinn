<script setup>
import { ref, watch, onBeforeUnmount } from 'vue'

const props = defineProps({
  preview: String,
  maxSize: {
    type: Number,
    default: 2 * 1024 * 1024
  }
})

const emit = defineEmits(['error'])
const fileModel = defineModel()

const imagePreview = ref(props.preview || null)
const isDragging = ref(false)
const error = ref(null)

watch(() => props.preview, (val) => {
  imagePreview.value = val || null
})

const handleDrop = (file) => {
  isDragging.value = false
  error.value = null

  if (!file) return

  if (!file.type.startsWith('image/')) {
    error.value = 'Please select an image'
    emit('error', error.value)
    return
  }

  if (file.size > props.maxSize) {
    error.value = 'Image is too large. Maximum size is 2MB'
    emit('error', error.value)
    return
  }

  fileModel.value = file

  if (imagePreview.value?.startsWith('blob:')) {
    URL.revokeObjectURL(imagePreview.value)
  }

  imagePreview.value = URL.createObjectURL(file)
}

onBeforeUnmount(() => {
  if (imagePreview.value?.startsWith('blob:')) {
    URL.revokeObjectURL(imagePreview.value)
  }
})
</script>

<template>
  <div>
    <input
        type="file"
        id="file"
        class="sr-only"
        accept="image/*"
        aria-hidden="true"
        @change="handleDrop($event.target.files?.[0])"
    />

    <label
        for="file"
        class="relative flex flex-col items-center justify-center min-h-50 rounded-md border-2 border-dashed transition-all cursor-pointer"
        :class="{
        'border-[#e0e0e0] bg-white hover:border-[#07074D]': !isDragging && !error,
        'border-[#07074D] bg-blue-50': isDragging && !error,
        'border-red-400 bg-red-50': error
      }"
        @dragover.prevent="isDragging = true"
        @dragleave.prevent="isDragging = false"
        @drop.prevent="handleDrop($event.dataTransfer.files?.[0])"
        role="button"
    >
      <template v-if="imagePreview">
        <img
            :src="imagePreview"
            class="w-full max-h-48 object-contain rounded-md mb-4 p-2"
        />
        <span class="inline-flex rounded border border-[#e0e0e0] py-2 px-7 mb-2 text-base font-medium text-[#07074D] hover:bg-gray-50 transition">
          Browse
        </span>
      </template>

      <template v-else>
        <span class="mb-2 block text-xl font-semibold text-[#07074D]">
          Drop image here
        </span>
        <span class="mb-2 block text-base font-medium text-[#6B7280]">
          Or
        </span>
        <span class="inline-flex rounded border border-[#e0e0e0] py-2 px-7 text-base font-medium text-[#07074D] hover:bg-gray-50 transition">
          Browse
        </span>
      </template>
    </label>

    <div v-if="error" class="mt-2 text-sm text-red-600" role="alert">
      {{ error }}
    </div>
  </div>
</template>