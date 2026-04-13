<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  modelValue: [File, String],
  preview: String,
  maxSize: {
    type: Number,
    default: 2 * 1024 * 1024
  }
})

const emit = defineEmits(['update:modelValue', 'error'])

const imagePreview = ref(props.preview || null)
const isDragging = ref(false)
const isLoading = ref(false)
const error = ref(null)

watch(() => props.preview, (val) => {
  if (val && !imagePreview.value) {
    imagePreview.value = val
  }
})

const validateFile = (file) => {
  error.value = null

  if (!file) return false

  if (!file.type.startsWith('image/')) {
    error.value = 'Please select an image'
    emit('error', error.value)
    return false
  }

  if (file.size > props.maxSize) {
    error.value = 'Image is too large. Maximum size is 2MB'
    emit('error', error.value)
    return false
  }

  return true
}

const handleFile = (file) => {
  if (!validateFile(file)) return

  isLoading.value = true

  emit('update:modelValue', file)

  const reader = new FileReader()

  reader.onload = (e) => {
    imagePreview.value = e.target.result
    isLoading.value = false
  }

  reader.onerror = () => {
    error.value = 'Error reading file'
    emit('error', error.value)
    isLoading.value = false
  }

  reader.readAsDataURL(file)
}

const onChange = (e) => {
  handleFile(e.target.files?.[0])
}

const onDrop = (e) => {
  isDragging.value = false
  handleFile(e.dataTransfer.files?.[0])
}

const onDragOver = (e) => {
  e.preventDefault()
  isDragging.value = true
}

const onDragLeave = () => {
  isDragging.value = false
}
</script>

<template>
  <div>
    <input
        type="file"
        id="file"
        class="sr-only"
        @change="onChange"
        accept="image/*"
        aria-hidden="true"
    />

    <label
        for="file"
        class="relative flex flex-col items-center justify-center min-h-50 rounded-md border-2 border-dashed transition-all cursor-pointer"
        :class="{
        'border-[#e0e0e0] bg-white hover:border-[#07074D]': !isDragging && !error,
        'border-[#07074D] bg-blue-50': isDragging && !error,
        'border-red-400 bg-red-50': error
      }"
        @dragover.prevent="onDragOver"
        @dragleave.prevent="onDragLeave"
        @drop.prevent="onDrop"
        role="button"
    >
      <div v-if="isLoading" class="flex flex-col items-center">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-[#07074D]"></div>
        <span class="mt-2 text-sm text-[#6B7280]">Uploading...</span>
      </div>

      <template v-else-if="imagePreview">
        <img
            :src="imagePreview"
            class="w-32 h-32 object-cover rounded-full mb-4"
        />
        <span class="inline-flex rounded border border-[#e0e0e0] py-2 px-7 text-base font-medium text-[#07074D] hover:bg-gray-50 transition">
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