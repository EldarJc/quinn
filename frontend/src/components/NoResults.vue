<script setup>
defineEmits(['reset']);
</script>

<template>
  <div class="flex flex-col items-center justify-center py-16 px-4 text-center">
    <div class="w-20 h-20 mb-6 text-gray-300">
      <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
      </svg>
    </div>
    <h3 class="text-xl font-bold text-gray-900 mb-2">No results found</h3>
    <p class="text-gray-500 max-w-md mx-auto mb-8">
      We couldn't find anything matching your current filters. Try adjusting your search criteria or clearing filters to see more.
    </p>
  </div>
</template>