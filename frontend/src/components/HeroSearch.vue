<script setup>
defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  title: {
    type: String,
    required: true
  },
  description: {
    type: String,
    required: true
  },
  placeholder: {
    type: String,
    default: 'Search...'
  },
  backgroundImage: {
    type: String,
    default: 'https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&q=80'
  }
});

defineEmits(['update:modelValue']);
</script>

<template>
  <div class="relative overflow-hidden rounded-3xl mx-4 mt-4 shadow-sm border border-gray-200">
    <div class="absolute inset-0">
      <div class="absolute inset-0 bg-slate-800/60 mix-blend-multiply"></div>
      <img
          :src="backgroundImage"
          alt="Background"
          class="w-full h-full object-cover"
      />
    </div>
    <div class="relative w-7xl py-16 px-8 flex flex-col items-center text-center">
      <h1 class="text-6xl font-extrabold tracking-tight text-white">
        {{ title }}
      </h1>
      <p class="mt-6 max-w-2xl text-xl text-slate-100 font-light">
        {{ description }}
      </p>
      <div class="mt-10 w-full max-w-2xl flex relative">
        <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
          <svg class="h-6 w-6 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd" />
          </svg>
        </div>
        <input
            :value="modelValue"
            @input="$emit('update:modelValue', $event.target.value)"
            type="text"
            class="block w-full pl-12 pr-4 py-4 border-0 rounded-2xl leading-5 bg-white text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-teal-500 shadow-lg"
            :placeholder="placeholder"
        />
      </div>
    </div>
  </div>
</template>